"""Corpus study of Scott Joplin's rags (Humdrum edition by Craig Sapp).

Usage: python -I analyze_ragtime.py <kern_dir> <out_json>

Only the 2/4 rags are used.  Measured per piece:
  * right hand: the rhythm of every bar as an 8-slot onset pattern (sixteenths), with ties
    respected; share of bars with the tied syncopation over the middle of the bar, with the
    untied short-long-short figure, with plain running sixteenths
  * right hand texture: share of attacks that are octaves or fuller chords
  * left hand: share of bars that are the march bass (low - chord - low - chord in eighths)
  * melody (top line): interval vocabulary, range
  * key signatures in order (where the trio goes), bar count, chromatic share
"""
import sys, json, glob, os, collections, statistics, warnings
warnings.filterwarnings("ignore")
from music21 import converter, note, chord, stream, meter, key

kern_dir, out_json = sys.argv[1], sys.argv[2]
SKIP = {"school", "solace", "stoptime"}        # exercises, habanera, stop-time novelty


def onset_ok(el):
    if el.duration.isGrace:
        return False
    t = el.tie
    return t is None or t.type == "start"


def analyse(path):
    name = os.path.basename(path)[:-4]
    s = converter.parse(path)
    parts = list(s.parts)
    if len(parts) < 2:
        return None
    ts = parts[0].flatten().getElementsByClass(meter.TimeSignature)
    if not ts or ts[0].ratioString != "2/4":
        return None
    means = []
    for p in parts:
        ps = [q.midi for n in p.flatten().notes for q in n.pitches]
        means.append(statistics.mean(ps) if ps else 0)
    rh = parts[means.index(max(means))]; lh = parts[means.index(min(means))]

    pats = collections.Counter(); bars = 0
    tied_mid = untied_sls = running = 0
    att = oct_att = chord_att = 0
    top = []
    for m in rh.getElementsByClass(stream.Measure):
        if abs(m.duration.quarterLength - 2.0) > 1e-6:
            continue
        slots = [False] * 8
        ev = {}
        for el in m.flatten().notes:
            if not onset_ok(el):
                continue
            o = float(el.offset) * 4
            if abs(o - round(o)) > 1e-6 or not (0 <= round(o) < 8):
                continue                           # triplets / ornaments: ignore for the grid
            k = int(round(o)); slots[k] = True
            ps = sorted(p.midi for p in el.pitches)
            cur = ev.get(k, [])
            ev[k] = sorted(set(cur + ps))
        if not any(slots):
            continue
        bars += 1
        pat = "".join("x" if b else "." for b in slots)
        pats[pat] += 1
        if slots[3] and not slots[4]:
            tied_mid += 1
        if any(slots[b] and slots[b + 1] and not slots[b + 2] and slots[b + 3] for b in (0, 4)):
            untied_sls += 1
        if all(slots):
            running += 1
        for k in sorted(ev):
            ps = ev[k]; att += 1
            if len(ps) >= 2 and (ps[-1] - ps[0]) == 12:
                oct_att += 1
            if len(ps) >= 2:
                chord_att += 1
            top.append(ps[-1])

    lbars = march = 0
    lows = []
    for m in lh.getElementsByClass(stream.Measure):
        if abs(m.duration.quarterLength - 2.0) > 1e-6:
            continue
        ev = {}
        for el in m.flatten().notes:
            if not onset_ok(el):
                continue
            o = float(el.offset) * 4
            if abs(o - round(o)) > 1e-6:
                continue
            ev.setdefault(int(round(o)), []).extend(p.midi for p in el.pitches)
        if not ev:
            continue
        lbars += 1
        lows.append(min(min(v) for v in ev.values()))
        if set(ev) == {0, 2, 4, 6} and min(ev[0]) < min(ev[2]) and min(ev[4]) < min(ev[6]):
            march += 1

    iv = [abs(b - a) for a, b in zip(top, top[1:])]
    n_iv = max(1, len(iv))
    ks = [k.sharps for k in rh.flatten().getElementsByClass(key.KeySignature)]
    ksq = [k for i, k in enumerate(ks) if i == 0 or k != ks[i - 1]]
    tonic_pc = (ksq[0] * 7) % 12 if ksq else 0
    diat = {(tonic_pc + d) % 12 for d in (0, 2, 4, 5, 7, 9, 11)}
    allp = [p.midi for n in s.flatten().notes for p in n.pitches]
    return dict(
        piece=name, bars=bars, key_signatures=ksq,
        pct_bars_tied_syncopation=round(100 * tied_mid / max(1, bars), 1),
        pct_bars_short_long_short=round(100 * untied_sls / max(1, bars), 1),
        pct_bars_running_sixteenths=round(100 * running / max(1, bars), 1),
        pct_attacks_octave=round(100 * oct_att / max(1, att), 1),
        pct_attacks_chord=round(100 * chord_att / max(1, att), 1),
        attacks_per_bar=round(att / max(1, bars), 2),
        pct_bars_march_bass=round(100 * march / max(1, lbars), 1),
        lh_lowest_median=statistics.median(lows) if lows else 0,
        melody_low=min(top), melody_high=max(top), melody_median=statistics.median(top),
        pct_step=round(100 * sum(1 for i in iv if 1 <= i <= 2) / n_iv, 1),
        pct_repeat=round(100 * sum(1 for i in iv if i == 0) / n_iv, 1),
        pct_third=round(100 * sum(1 for i in iv if 3 <= i <= 4) / n_iv, 1),
        pct_4th_5th=round(100 * sum(1 for i in iv if 5 <= i <= 7) / n_iv, 1),
        pct_6th_plus=round(100 * sum(1 for i in iv if i >= 8) / n_iv, 1),
        chromatic_share=round(100 * sum(1 for p in allp if p % 12 not in diat) / max(1, len(allp)), 1),
        patterns=dict(pats.most_common(40)),
    )


if __name__ == "__main__":
    res, allpat = [], collections.Counter()
    for path in sorted(glob.glob(os.path.join(kern_dir, "*.krn"))):
        if os.path.basename(path)[:-4] in SKIP:
            continue
        try:
            r = analyse(path)
        except Exception as ex:
            print(os.path.basename(path), "FAILED", type(ex).__name__, str(ex)[:80]); continue
        if not r:
            continue
        res.append(r); allpat.update(r["patterns"])
        print(f"{r['piece']:14s} bars{r['bars']:4d} keys{str(r['key_signatures']):14s} tied{r['pct_bars_tied_syncopation']:5.1f} "
              f"sls{r['pct_bars_short_long_short']:5.1f} run{r['pct_bars_running_sixteenths']:5.1f} | oct{r['pct_attacks_octave']:5.1f} "
              f"chord{r['pct_attacks_chord']:5.1f} att/bar{r['attacks_per_bar']:5.2f} | march{r['pct_bars_march_bass']:5.1f} low{r['lh_lowest_median']:5.1f} | "
              f"mel {r['melody_low']}-{r['melody_high']} med{r['melody_median']:.0f} step{r['pct_step']:5.1f} rep{r['pct_repeat']:5.1f} "
              f"3rd{r['pct_third']:5.1f} 4/5{r['pct_4th_5th']:5.1f} 6+{r['pct_6th_plus']:5.1f} chrom{r['chromatic_share']:5.1f}")
    tot = sum(allpat.values())
    print("\nmost common right-hand bar rhythms (x = attack on that sixteenth):")
    for p, c in allpat.most_common(24):
        print(f"  {p[:4]} {p[4:]}   {100*c/tot:5.1f}%")
    json.dump(dict(pieces=res, bar_patterns={p: c / tot for p, c in allpat.most_common(60)}), open(out_json, "w"), indent=1)
    print("wrote", out_json, len(res))
