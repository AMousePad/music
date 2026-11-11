"""Compose -> perform -> render Firethorn.

python build_etude.py [--tag final] [--no-audio]
Outputs go to ../../out/etude_<tag>/ : performance MIDI, WAV (24-bit), FLAC, MP3, a figure of
the interpretation, the proof-reading report.
"""
import argparse, json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "engine"))
import firethorn as piece
from perform_etude import Virtuoso
import etude_theory

BASE = "firethorn"


def figure(perf, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ev = perf.events
    fig, ax = plt.subplots(4, 1, figsize=(26, 14), gridspec_kw={"height_ratios": [4, 1.2, 1.3, 1]}, sharex=True)
    col = {"melody": "#d1495b", "rh_inner": "#edae49", "bass": "#00798c", "acc": "#66a182", "run": "#2e4057",
           "bell": "#c33c9e", "arp": "#8d96a3"}
    for e in ev:
        ax[0].plot([e["on"], e["off"]], [e["pitch"], e["pitch"]], color=col[e["role"]],
                   lw=0.6 + e["vel"] / 45.0, alpha=0.35 + 0.5 * e["vel"] / 127, solid_capstyle="butt")
    tb = np.array([perf.t(i * 8.0) for i in range(len(perf.sc.bars) + 1)])
    for i, (name, k) in enumerate(perf.sc.tags):
        if k == 1:
            for a in ax:
                a.axvline(tb[i], color="k", lw=0.8, alpha=0.6)
            ax[0].text(tb[i] + 0.3, 104, name, fontsize=11, weight="bold")
    ax[0].set_ylabel("MIDI pitch"); ax[0].set_ylim(22, 108); ax[0].set_title(f"{perf.sc.title} - performance")
    ax[1].step(tb[:-1], 120.0 / np.diff(tb), where="post", color="k", lw=0.8)
    ax[1].set_ylabel("quarter-note bpm (per bar)"); ax[1].grid(alpha=0.3)
    for role in ("melody", "run", "bell", "bass", "acc", "arp"):
        ax[2].scatter([e["on"] for e in ev if e["role"] == role], [e["vel"] for e in ev if e["role"] == role],
                      s=2, color=col[role], label=role)
    ax[2].set_ylabel("velocity"); ax[2].legend(loc="upper left", ncol=6, fontsize=8); ax[2].grid(alpha=0.3)
    ax[3].plot(perf.sustain[0], perf.sustain[1], lw=0.4, color="k")
    ax[3].set_ylabel("sustain pedal"); ax[3].set_xlabel("seconds")
    plt.tight_layout(); plt.savefig(path, dpi=70); plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="final"); ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--seed", type=int, default=1851)
    a = ap.parse_args()
    out = os.path.join(HERE, "..", "..", "out", f"etude_{a.tag}"); os.makedirs(out, exist_ok=True)
    sc = piece.build()
    issues, stats = etude_theory.check(sc, verbose=False)
    print(f"score: {stats['bars']} bars, {stats['notes']} notes, {len(issues)} proof-reading issues")
    for i in issues:
        print("   !", i)
    json.dump(dict(issues=issues, stats=stats), open(os.path.join(out, "score_proofreading.json"), "w"), indent=1)
    perf = Virtuoso(sc, piece.PLAN, seed=a.seed)
    ev = perf.perform()
    s = perf.summary()
    print(f"performance: {s['key_strokes']} key strokes, {s['seconds']:.1f} s ({int(s['seconds'] // 60)}:{s['seconds'] % 60:04.1f}), "
          f"{s['notes_per_second']:.1f} notes/s; velocity p05/50/95 {s['vel_p05']:.0f}/{s['vel_p50']:.0f}/{s['vel_p95']:.0f} "
          f"max {s['vel_max']}; pedal down {100 * s['pedal_share_down']:.0f}%")
    print("  sections:", "  ".join(f"{k} {v['seconds']:.0f}s" for k, v in s["sections"].items()))
    perf.write_midi(os.path.join(out, f"{BASE}_performance.mid"))
    figure(perf, os.path.join(out, "interpretation.png"))
    json.dump([{k: (float(v) if isinstance(v, (np.floating, float)) else v) for k, v in e.items()} for e in ev],
              open(os.path.join(out, "performance_notes.json"), "w"))
    json.dump(s, open(os.path.join(out, "performance_summary.json"), "w"), indent=1)
    if a.no_audio:
        return
    from render_midi import render_events
    wav = os.path.join(out, f"{BASE}.wav")
    render_events(perf.as_notes(), perf.sustain_for_render(), perf.soft, wav, resonance_db=-28.0, wet_db=-15.5,
                  target_lufs=-18.0, master_kw=dict(bass_shelf_db=-3.5, limit_db=3.0))
    for ext, args in (("flac", ["-c:a", "flac"]), ("mp3", ["-c:a", "libmp3lame", "-q:a", "0"])):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, *args, "-metadata", f"title={sc.title}",
                        "-metadata", "genre=Classical", os.path.join(out, f"{BASE}.{ext}")], check=True)
    print("written to", os.path.abspath(out))


if __name__ == "__main__":
    main()
