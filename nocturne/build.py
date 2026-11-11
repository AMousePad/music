"""Compose -> perform -> render.

python build.py [--tag final] [--no-audio]
Outputs go to ../out/nocturne_<tag>/ : performance MIDI, score MIDI, WAV (24-bit), FLAC, MP3,
a figure of the interpretation and a spectrogram.
"""
import argparse, json, os, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "engine"))
import nocturne_bm as piece
from perform import Performance
import theory


def figure(perf, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ev = perf.events
    fig, ax = plt.subplots(4, 1, figsize=(20, 13), gridspec_kw={"height_ratios": [4, 1.3, 1.3, 1]}, sharex=True)
    col = {"melody": "#d1495b", "duet": "#edae49", "rh_inner": "#edae49", "bass": "#00798c", "acc": "#66a182"}
    for e in ev:
        ax[0].plot([e["on"], e["off"]], [e["pitch"], e["pitch"]], color=col[e["role"]],
                   lw=1.0 + e["vel"] / 30.0, alpha=0.35 + 0.6 * e["vel"] / 127, solid_capstyle="butt")
    bars = [(b.number, perf.t(perf.S(b.number, 0))) for b in perf.sc.bars]
    for nb, tb in bars:
        for a in ax:
            a.axvline(tb, color="k", lw=0.3, alpha=0.3)
        ax[0].text(tb, 101, str(nb), fontsize=7)
    ax[0].set_ylabel("MIDI pitch"); ax[0].set_ylim(24, 103); ax[0].set_title(f"{perf.sc.title} - performance")
    # tempo actually played per eighth
    g = perf.grid[::8]; tt = np.array([perf.t(s) for s in g])
    bpm = 20.0 / (np.diff(tt) / np.diff(g))
    ax[1].plot(tt[:-1], bpm, color="k", lw=0.8); ax[1].set_ylabel("dotted-quarter bpm"); ax[1].set_ylim(15, 75); ax[1].grid(alpha=0.3)
    for role in ("melody", "bass", "acc"):
        xs = [e["on"] for e in ev if e["role"] == role]; ys = [e["vel"] for e in ev if e["role"] == role]
        ax[2].scatter(xs, ys, s=4, color=col[role], label=role)
    ax[2].set_ylabel("velocity"); ax[2].legend(loc="upper left", ncol=3, fontsize=7); ax[2].grid(alpha=0.3)
    ax[3].plot(perf.sustain[0], perf.sustain[1], lw=0.6, color="k", label="sustain")
    ax[3].plot(perf.soft[0], np.array(perf.soft[1]) * 0.5, lw=1.0, color="tab:blue", drawstyle="steps-post", label="una corda")
    ax[3].set_ylabel("pedals"); ax[3].set_xlabel("seconds"); ax[3].legend(fontsize=7, loc="upper left")
    plt.tight_layout(); plt.savefig(path, dpi=75); plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="final")
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--seed", type=int, default=1810)
    a = ap.parse_args()
    out = os.path.join(HERE, "..", "out", f"nocturne_{a.tag}"); os.makedirs(out, exist_ok=True)
    sc = piece.build()
    issues, stats = theory.check(sc, verbose=False)
    print(f"score: {stats['bars']} bars, {stats['notes']} notes, {len(issues)} proof-reading issues")
    for i in issues:
        print("   !", i)
    perf = Performance(sc, piece, seed=a.seed)
    ev = perf.perform()
    dur = max(e["off"] for e in ev)
    print(f"performance: {len(ev)} key strokes, {dur:.1f} s ({int(dur//60)}:{dur%60:04.1f})")
    # rubato statistics in the form used for the ASAP study (research/tempo_stats.json)
    tb = np.array([perf.t(perf.S(b.number, 0)) for b in sc.bars] + [perf.t(sc.length)])
    bar_t = np.diff(tb); rel = np.median(bar_t) / bar_t
    print(f"rubato: median bar {np.median(bar_t):.2f} s; bar tempo ratio p05 {np.percentile(rel,5):.2f} p95 {np.percentile(rel,95):.2f}; "
          f"last 4 bars {rel[-4:].mean():.2f}; slowest bar {rel.min():.2f}   (ASAP Chopin: p05 .57-.84, p95 1.15-1.49, last4 .56-.86, slowest .34-.66)")
    midi_path = os.path.join(out, "nocturne_b_minor_performance.mid")
    perf.write_midi(midi_path)
    figure(perf, os.path.join(out, "interpretation.png"))
    json.dump([{k: (float(v) if isinstance(v, (np.floating, float)) else v) for k, v in e.items() if k != "t_end"}
               for e in ev], open(os.path.join(out, "performance_notes.json"), "w"))
    if a.no_audio:
        return
    from render_midi import render_events
    wav = os.path.join(out, "nocturne_b_minor.wav")
    render_events(perf.as_notes(), perf.sustain_for_render(), perf.soft, wav)
    for ext, args in (("flac", ["-c:a", "flac"]), ("mp3", ["-c:a", "libmp3lame", "-q:a", "0"])):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, *args,
                        "-metadata", f"title={sc.title}", "-metadata", "genre=Classical",
                        os.path.join(out, f"nocturne_b_minor.{ext}")], check=True)
    print("written to", os.path.abspath(out))


if __name__ == "__main__":
    main()
