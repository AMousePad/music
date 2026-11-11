"""Verify only this piece's newly created files. Never reads ../out.

python nocturne/last_lamp/verify.py
"""
from collections import Counter, defaultdict
import json
from pathlib import Path
import subprocess

import mido
import numpy as np
import soundfile as sf
from scipy.signal import stft, resample_poly
from pypdf import PdfReader

import piece

DEST = Path(__file__).resolve().parent / "recording"


def main():
    report = json.loads((DEST / "validation.json").read_text(encoding="utf-8"))
    events = json.loads((DEST / "performance_notes.json").read_text(encoding="utf-8"))
    sc = piece.build()
    # MIDI decoding, independently of the event writer.
    active, midi_count, now, midi_errors = Counter(), 0, 0., []
    pedal_cc = [(0., 0.)]
    for message in mido.MidiFile(DEST / f"{piece.STEM}_performance.mid"):
        now += message.time
        if message.type == "control_change" and message.control == 64:
            pedal_cc.append((now, message.value / 127))
        if message.type == "note_on" and message.velocity:
            if active[message.note]:
                midi_errors.append(f"Repeated held key {message.note} at {now:.4f}s")
            active[message.note] += 1
            midi_count += 1
        elif message.type == "note_off" or (message.type == "note_on" and not message.velocity):
            active[message.note] -= 1
            if active[message.note] < 0:
                midi_errors.append(f"Unmatched release {message.note}")
    assert not midi_errors and not any(active.values()), midi_errors
    assert midi_count == len(events)
    notated = Counter(n.pitch for n in sc.all_notes())
    engraved = Counter(m.note for m in mido.MidiFile(DEST / f"{piece.STEM}_score.mid")
                       if m.type == "note_on" and m.velocity)
    assert engraved == notated, {"extra": engraved - notated, "missing": notated - engraved}

    # Rebuild the time map from the authored score; only timing is needed here.
    from perform import Performance
    perf = Performance(sc, piece, seed=report["seed"])
    pedal_cc = np.array(pedal_cc)
    pedal_breaths = []
    for (bar, pos), (end_bar, end_pos) in piece.PEDAL_BREATHS:
        begin, end = perf.t(sc.s(bar, pos)), perf.t(sc.s(end_bar, end_pos))
        times = np.arange(begin + .01, end - .02, .005)
        depth = pedal_cc[np.maximum(0, np.searchsorted(pedal_cc[:, 0], times, side="right") - 1), 1]
        assert depth.min() >= .60, f"Pedal unexpectedly clears the breath in bar {bar}"
        pedal_breaths.append({"bar": bar, "minimum_pedal_depth": round(float(depth.min()), 4),
                             "damper_engagement_ms": round(float(np.sum(depth < .58) * 5), 1)})
    audio = sf.SoundFile(DEST / f"{piece.STEM}.wav")
    assert audio.samplerate == 48000 and audio.channels == 2 and audio.subtype == "PCM_24"
    peak, finite = 0., True
    for block in audio.blocks(blocksize=65536, dtype="float32"):
        peak = max(peak, float(np.abs(block).max()))
        finite = finite and bool(np.isfinite(block).all())
    assert finite and 0 < peak < 1

    # Each bar is compared with all 12 pitch transpositions. This is a coarse
    # spectral consistency check, not proof of every note or artistic quality.
    rows = []
    for b in sc.bars:
        begin = perf.t(sc.s(b.number)) + .4
        end = perf.t(sc.s(b.number, 12)) + .4
        audio.seek(int((begin + .15) * audio.samplerate))
        x = audio.read(int((end - begin - .15) * audio.samplerate), dtype="float32", always_2d=True).mean(axis=1)
        x = resample_poly(x, 1, 4)
        f, _, z = stft(x, 12000, nperseg=8192, noverlap=7168)
        keep = (f > 60) & (f < 2600)
        semitones = 69 + 12 * np.log2(f[keep] / 440)
        pc = np.rint(semitones).astype(int) % 12
        near = np.abs(semitones - np.rint(semitones)) < .38
        powers = np.abs(z[keep]) ** 2
        observed = np.array([powers[(pc == i) & near].sum() for i in range(12)])
        expected = np.zeros(12)
        for e in events:
            if e["bar"] == b.number:
                w = (e["vel"] / 64) ** 2 * max(.2, min(e["off"] - e["on"], 2))
                expected[e["pitch"] % 12] += w
                expected[(e["pitch"] + 7) % 12] += .18 * w
                expected[(e["pitch"] + 4) % 12] += .06 * w
        observed = np.sqrt(observed / (observed.sum() + 1e-20))
        expected = np.sqrt(expected / expected.sum())
        sims = [float(np.dot(observed, np.roll(expected, shift))) for shift in range(12)]
        rows.append({"bar": b.number, "similarity": round(sims[0], 4),
                     "best_transposition": int(np.argmax(sims))})
    wins = sum(r["best_transposition"] == 0 for r in rows)

    pdf = PdfReader(DEST / f"{piece.STEM}.pdf")
    log = (DEST / "engraving.log").read_text(encoding="utf-8")
    assert "warning:" not in log.lower() and "error:" not in log.lower()
    assert 1 <= len(pdf.pages) <= 6 and "The Last Lamp" in pdf.pages[0].extract_text()
    for ext in ("flac", "mp3"):
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(DEST / f"{piece.STEM}.{ext}"),
                        "-f", "null", "-"], check=True, capture_output=True)
    report["verification"] = {"midi_note_ons": midi_count, "unreleased_midi_notes": 0,
                              "engraved_score_pitch_counts_match": True,
                              "overlapping_midi_restrikes": 0, "pdf_pages": len(pdf.pages),
                              "engraving_warnings": 0, "audio_seconds": round(len(audio) / audio.samplerate, 3),
                              "sample_peak_dbfs": round(20 * np.log10(peak), 3),
                              "finite_unclipped_audio": finite and peak < 1,
                              "compressed_formats_decode": True,
                              "pedal_resonance_through_breaths": pedal_breaths,
                              "bars_matching_original_pitch": wins, "bars_checked": len(rows),
                              "pitch_check": rows,
                              "limits": "Automated musical and technical checks; not human-auditioned. The pitch-class check cannot detect every wrong note."}
    audio.close()
    (DEST / "validation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    summary = {k: v for k, v in report["verification"].items() if k != "pitch_check"}
    print(json.dumps(summary, indent=2))
    if wins != len(rows):
        print("Inspect pitch-check exceptions:", [r for r in rows if r["best_transposition"]])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
