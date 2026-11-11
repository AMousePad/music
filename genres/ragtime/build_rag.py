"""Compose -> perform -> render the rag.

python build_rag.py [--tag final] [--no-audio]
Outputs go to ../../out/ragtime_<tag>/ : performance MIDI, WAV (24-bit), FLAC, MP3, a figure
of the interpretation.
"""
import argparse, json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "engine"))
import larkspur_rag as piece
from perform_rag import RagPerformance
import rag_theory

BASE = "larkspur_rag"


def figure(perf, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ev = perf.events
    fig, ax = plt.subplots(4, 1, figsize=(22, 13), gridspec_kw={"height_ratios": [4, 1.2, 1.3, 1]}, sharex=True)
    col = {"melody": "#d1495b", "rh_inner": "#edae49", "bass": "#00798c", "acc": "#66a182"}
    for e in ev:
        ax[0].plot([e["on"], e["off"]], [e["pitch"], e["pitch"]], color=col[e["role"]],
                   lw=0.8 + e["vel"] / 40.0, alpha=0.4 + 0.5 * e["vel"] / 127, solid_capstyle="butt")
    for i, (name, k, p) in enumerate(perf.sc.tags):
        tb = perf.t(i * 8.0)
        if k == 1:
            for a in ax:
                a.axvline(tb, color="k", lw=0.8, alpha=0.6)
            ax[0].text(tb + 0.3, 100, f"{name}{'' if name == 'Intro' else p}", fontsize=10, weight="bold")
    ax[0].set_ylabel("MIDI pitch"); ax[0].set_ylim(24, 103); ax[0].set_title(f"{perf.sc.title} - performance")
    tb = np.array([perf.t(i * 8.0) for i in range(len(perf.sc.bars) + 1)])
    ax[1].step(tb[:-1], 120.0 / np.diff(tb), where="post", color="k", lw=0.8)
    ax[1].set_ylabel("quarter-note bpm (per bar)"); ax[1].set_ylim(55, 105); ax[1].grid(alpha=0.3)
    for role in ("melody", "bass", "acc"):
        ax[2].scatter([e["on"] for e in ev if e["role"] == role], [e["vel"] for e in ev if e["role"] == role],
                      s=3, color=col[role], label={"acc": "after-beat chords"}.get(role, role))
    ax[2].set_ylabel("velocity"); ax[2].legend(loc="upper left", ncol=3, fontsize=8); ax[2].grid(alpha=0.3)
    ax[3].plot(perf.sustain[0], perf.sustain[1], lw=0.5, color="k")
    ax[3].set_ylabel("sustain pedal"); ax[3].set_xlabel("seconds")
    plt.tight_layout(); plt.savefig(path, dpi=70); plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="final"); ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--seed", type=int, default=1899)
    a = ap.parse_args()
    out = os.path.join(HERE, "..", "..", "out", f"ragtime_{a.tag}"); os.makedirs(out, exist_ok=True)
    issues, stats = rag_theory.check(piece.build(written=True), verbose=False)
    print(f"score: {len(issues)} proof-reading issues")
    for i in issues:
        print("   !", i)
    sc = piece.build()
    perf = RagPerformance(sc, piece.PLAN, seed=a.seed)
    ev = perf.perform()
    s = perf.summary()
    print(f"performance: {len(sc.bars)} bars as played, {s['key_strokes']} key strokes, {s['seconds']:.1f} s "
          f"({int(s['seconds']//60)}:{s['seconds']%60:04.1f})")
    print(f"  tempo per bar: median {s['bpm_median']:.1f}, p05 {s['bpm_p05']:.1f}, p95 {s['bpm_p95']:.1f} quarter-note bpm")
    print(f"  velocity p05/50/95 {s['vel_p05']:.0f}/{s['vel_p50']:.0f}/{s['vel_p95']:.0f}; melody {s['melody']:.0f}, "
          f"bass {s['bass']:.0f}, after-beat chords {s['chords']:.0f}; pedal down {100*s['pedal_share_down']:.0f}% of the time")
    perf.write_midi(os.path.join(out, f"{BASE}_performance.mid"))
    figure(perf, os.path.join(out, "interpretation.png"))
    json.dump([{k: (float(v) if isinstance(v, (np.floating, float)) else v) for k, v in e.items()} for e in ev],
              open(os.path.join(out, "performance_notes.json"), "w"))
    json.dump(s, open(os.path.join(out, "performance_summary.json"), "w"), indent=1)
    if a.no_audio:
        return
    from render_midi import render_events
    import hall
    # a parlour-sized room rather than a concert hall: closer, drier, livelier
    ir = hall.make_hall_ir(seconds=2.0, room=(10.0, 14.0, 6.0), src=(5.0, 3.6, 1.3),
                           mics=((3.9, 5.9, 2.0), (6.1, 5.9, 2.0)), rt60_mid=0.95, seed=11)
    wav = os.path.join(out, f"{BASE}.wav")
    render_events(perf.as_notes(), perf.sustain_for_render(), perf.soft, wav, resonance_db=-30.0, wet_db=-17.5,
                  target_lufs=-18.0, ir=ir, stereo_width=0.66, master_kw=dict(bass_shelf_db=-3.0, limit_db=2.0))
    for ext, args in (("flac", ["-c:a", "flac"]), ("mp3", ["-c:a", "libmp3lame", "-q:a", "0"])):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, *args, "-metadata", f"title={sc.title}",
                        "-metadata", "genre=Ragtime", os.path.join(out, f"{BASE}.{ext}")], check=True)
    print("written to", os.path.abspath(out))


if __name__ == "__main__":
    main()
