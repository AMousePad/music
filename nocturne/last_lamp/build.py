"""Build this new composition without accessing ../out.

python nocturne/last_lamp/build.py               # score, performance MIDI, WAV/FLAC/MP3
python nocturne/last_lamp/build.py --no-audio    # composition checks and both scores
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from collections import defaultdict

import piece
from score import chord_pcs
from perform import Performance
import theory

HERE = Path(__file__).resolve().parent
DEST = HERE / "recording"


def load_engraver():
    spec = importlib.util.spec_from_file_location("lamp_engraver", HERE / "engrave.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--no-engraving", action="store_true",
                    help="Reuse the existing score when changing only the performance")
    ap.add_argument("--seed", type=int, default=11112026)
    args = ap.parse_args()
    DEST.mkdir(parents=True, exist_ok=True)
    sc = piece.build()
    issues, stats = theory.check(sc, verbose=False)
    # The inherited checker hardcodes B minor for this one statistic.
    notes = sc.all_notes()
    f_minor = {0, 1, 3, 5, 7, 8, 10}
    stats["chromatic_share"] = round(100 * sum(n.pitch % 12 not in f_minor for n in notes) / len(notes), 1)
    # Audit the whole right hand, including held inner-voice notes.
    for b in sc.bars:
        rh = [n for n in b.notes if n.hand == "R" and n.grace is None]
        for s in sorted({n.s for n in rh}):
            sounding = [n.pitch for n in rh if n.s <= s + 1e-8 < n.s + n.dur - 1e-8]
            if sounding and max(sounding) - min(sounding) > 12:
                issues.append(f"bar {b.number}: combined right-hand reach exceeds an octave at {s:g}")
        for a in b.notes:
            for other in b.notes:
                if (a.hand == "R" and other.hand == "L" and a.pitch == other.pitch
                    and max(a.s, other.s) < min(a.s + a.dur, other.s + other.dur) - 1e-8):
                    issues.append(f"bar {b.number}: both hands require the same held key {a.name}")
                if (a.voice == "rh" and other.voice == "rh2" and a.pitch == other.pitch
                    and max(a.s, other.s) < min(a.s + a.dur, other.s + other.dur) - 1e-8):
                    issues.append(f"bar {b.number}: two right-hand voices require the same held key {a.name}")
    inner = sorted((n for n in notes if n.voice == "rh2"), key=lambda n: n.s)
    inner_dissonances = 0
    for a, nxt in zip(inner, inner[1:]):
        pcs = chord_pcs(sc.harmony_at(a.s))[0]
        end_pcs = chord_pcs(sc.harmony_at(a.s + a.dur - .001))[0]
        if a.pitch % 12 not in pcs | end_pcs:
            inner_dissonances += 1
            if not (1 <= abs(nxt.pitch - a.pitch) <= 2):
                issues.append(f"bar {a.bar}: inner-voice dissonance {a.name} does not resolve by step")
    stats["inner_voice_dissonances_resolving_by_step"] = inner_dissonances
    report = {"title": sc.title, "seed": args.seed, "composition": stats, "issues": issues,
              "read_boundary": "No files under the repository's out/ directory are inputs to this build."}
    print(json.dumps(report, indent=2), flush=True)
    (DEST / "validation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if issues:
        raise SystemExit("Resolve score findings before rendering.")
    perf = Performance(sc, piece, seed=args.seed,
                       opts={"async_sd": .020, "bass_gap": 22, "acc_gap": 24, "duet_gap": 12})
    events = perf.perform()
    # A repeated MIDI key must be released before being struck again; otherwise
    # its old note_off can cut the new note short on a standard MIDI piano.
    by_pitch = defaultdict(list)
    for event in events:
        by_pitch[event["pitch"]].append(event)
    release_corrections = 0
    for line in by_pitch.values():
        line.sort(key=lambda e: e["on"])
        for a, b in zip(line, line[1:]):
            if a["off"] >= b["on"]:
                a["off"] = b["on"] - .012
                release_corrections += 1
    assert all(0 <= e["on"] < e["off"] and 21 <= e["pitch"] <= 108 and 1 <= e["vel"] <= 127 for e in events)
    midi = DEST / f"{piece.STEM}_performance.mid"
    perf.write_midi(str(midi))
    report["performance"] = {"key_strokes": len(events), "note_end_seconds": max(e["off"] for e in events),
                             "velocities": [min(e["vel"] for e in events), max(e["vel"] for e in events)],
                             "repeated_key_release_corrections": release_corrections}
    groups = [n for n in notes if n.group and n.group[1] == 0]
    group_spans = sorted({(n.group[2], n.group[4]) for n in groups})
    poly_bars = [b.number for b in sc.bars if b.raw["rh2"]]
    double_bars = sorted({n.bar for n in notes if n.voice == "rh" and n.chord_size > 1})
    running_left = [b.number for b in sc.bars if len({n.s for n in b.notes if n.hand == "L"}) >= 20]
    report["difficulty"] = {"target": "Advanced concert level, approximately Henle 8; an editorial estimate, not an official grading",
                            "independent_right_hand_voice_bars": poly_bars,
                            "double_note_or_octave_bars": double_bars,
                            "running_sixteenth_accompaniment_bars": running_left,
                            "ornament_groups": [{"notes": count, "span_in_eighths": span} for count, span in group_spans],
                            "full_bar_melody_rests": [1],
                            "cadential_breaths_bars": [10, 18, 26, 40, 48, 52],
                            "major_sections": {"theme": [3, 18], "duet_and_development": [19, 34],
                                               "climax_and_cadenza": [35, 40], "return": [41, 48], "coda": [49, 60]}}
    (DEST / "performance_notes.json").write_text(json.dumps(events, indent=1), encoding="utf-8")
    if not args.no_engraving:
        load_engraver().engrave(sc, DEST)
    if not args.no_audio:
        from render_midi import render_events
        wav = DEST / f"{piece.STEM}.wav"
        _, info = render_events(perf.as_notes(), perf.sustain_for_render(), perf.soft, str(wav),
                                target_lufs=-20, wet_db=-16, stereo_width=.65,
                                master_kw={"limit_db": 1.5})
        report["master"] = info
        for ext, codec in (("flac", ["-c:a", "flac"]), ("mp3", ["-c:a", "libmp3lame", "-q:a", "0"])):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), *codec,
                            "-metadata", f"title={piece.TITLE} - Nocturne in F minor",
                            "-metadata", "artist=Codex", "-metadata", "genre=Classical",
                            "-metadata", "comment=Salamander Grand Piano by Alexander Holm, CC BY 3.0; original composition and programmed performance.",
                            str(DEST / f"{piece.STEM}.{ext}")], check=True)
    (DEST / "validation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Written to {DEST}", flush=True)


if __name__ == "__main__":
    main()
