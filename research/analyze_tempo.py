"""Tempo rubato statistics from ASAP beat annotations (Chopin Berceuse op.57 and Barcarolle op.60:
the two nocturne-type works in ASAP).  Usage: python -I analyze_tempo.py <asap_root> <out_json>"""
import sys, json, numpy as np
root, out = sys.argv[1], sys.argv[2]
ann = json.load(open(root + "/asap_annotations.json"))
res = []
for k, a in ann.items():
    if not ("Berceuse" in k or "Barcarolle" in k):
        continue
    b = np.array(a["performance_beats"]); db = set(np.round(a["performance_downbeats"], 3))
    ibi = np.diff(b); bpm = 60 / ibi
    med = np.median(bpm); rel = bpm / med
    # position of each beat inside its bar
    pos, p = [], 0
    for t in b[:-1]:
        if round(float(t), 3) in db: p = 0
        pos.append(p); p += 1
    pos = np.array(pos); nb = pos.max() + 1
    prof = [float(np.median(rel[pos == i])) for i in range(nb)]
    # bar-level tempo and how it moves bar to bar
    d = np.array(sorted(a["performance_downbeats"])); bar = np.diff(d); barrel = np.median(bar) / bar
    res.append(dict(piece=k.split("/")[1], perf=k.split("/")[-1][:28], median_bpm=float(med),
        beat_tempo_ratio_p05=float(np.percentile(rel, 5)), beat_tempo_ratio_p95=float(np.percentile(rel, 95)),
        sd_log2_beat=float(np.std(np.log2(rel))), within_bar_profile=prof,
        bar_tempo_ratio_p05=float(np.percentile(barrel, 5)), bar_tempo_ratio_p95=float(np.percentile(barrel, 95)),
        sd_log2_bar=float(np.std(np.log2(barrel))),
        bar_to_bar_change_sd=float(np.std(np.diff(np.log2(barrel)))),
        last4_bars_ratio=float(np.mean(barrel[-4:])), slowest_bar=float(barrel.min())))
    r = res[-1]
    print(f"{r['piece'][:14]:14s} {r['perf']:28s} bpm{r['median_bpm']:6.1f} beat p5/p95 {r['beat_tempo_ratio_p05']:.2f}/{r['beat_tempo_ratio_p95']:.2f} "
          f"bar p5/p95 {r['bar_tempo_ratio_p05']:.2f}/{r['bar_tempo_ratio_p95']:.2f} last4 {r['last4_bars_ratio']:.2f} min {r['slowest_bar']:.2f} prof {[round(x,2) for x in prof]}")
json.dump(res, open(out, "w"), indent=1)
