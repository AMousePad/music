"""Corpus study of Chopin's nocturnes from the NIFC first-edition Humdrum scores.

Usage: python -I analyze_scores.py <kern_dir> <out_json>

For every nocturne (one edition per opus/number) we measure the things a
composer imitating the style has to get right:
  * metre, key signature, length
  * melody (top voice of upper staff): range, tessitura, interval vocabulary,
    proportion of conjunct motion, duration vocabulary, grace notes / tuplets
  * left hand: attacks per bar, lowest note per bar, bar-wise span, register
  * chromaticism: share of pitch classes foreign to the key signature
"""
import sys, json, glob, os, collections, statistics, warnings
warnings.filterwarnings("ignore")
from music21 import converter, note, chord, stream, meter, key, expressions

kern_dir, out_json = sys.argv[1], sys.argv[2]

NOCTURNES = {  # opus -> number of nocturnes in the opus
    "009": 3, "015": 3, "027": 2, "032": 2, "037": 2, "048": 2, "055": 2, "062": 2,
}
PREF = ["Sm", "BH", "KI", "W", "BR", "TR"]


def pick_files():
    out = []
    for op, n in NOCTURNES.items():
        for i in range(1, n + 1):
            cands = sorted(glob.glob(os.path.join(kern_dir, f"{op}-*-{i:03d}.krn")))
            if not cands:
                continue
            cands.sort(key=lambda p: next((k for k, s in enumerate(PREF) if f"-{s}-" in p), 99))
            out.append((f"Op.{int(op)} No.{i}", cands[0]))
    e = glob.glob(os.path.join(kern_dir, "072-*-001-nocturne.krn"))
    if e:
        out.append(("Op.72 No.1", e[0]))
    return out


def top_line(part):
    """Highest sounding pitch at each onset of a staff -> list of (offset, midi, quarterLength, isGrace)."""
    ev = {}
    for el in part.flatten().notes:
        off = float(el.offset)
        pitches = [p.midi for p in el.pitches]
        g = el.duration.isGrace
        k = (round(off, 4), g, id(el) if g else 0)
        cur = ev.get(k)
        m = max(pitches)
        if cur is None or m > cur[1]:
            ev[k] = (off, m, float(el.duration.quarterLength), g)
    return sorted(ev.values(), key=lambda t: (t[0], not t[3]))


def analyse(label, path):
    s = converter.parse(path)
    parts = list(s.parts)
    if len(parts) < 2:
        return None
    # Humdrum order is bottom-up, music21 reverses to score order; decide by mean pitch.
    means = []
    for p in parts:
        ms = [n.pitch.midi if isinstance(n, note.Note) else statistics.mean(q.midi for q in n.pitches)
              for n in p.flatten().notes]
        means.append(statistics.mean(ms) if ms else 0)
    rh = parts[means.index(max(means))]
    lh = parts[means.index(min(means))]

    ts = rh.flatten().getElementsByClass(meter.TimeSignature)
    ks = rh.flatten().getElementsByClass(key.KeySignature)
    ts0 = ts[0].ratioString if ts else "?"
    sharps = ks[0].sharps if ks else 0
    barlen = ts[0].barDuration.quarterLength if ts else 4.0
    nbars = len(rh.getElementsByClass(stream.Measure))

    mel = top_line(rh)
    pitches = [m[1] for m in mel]
    ivs = [b - a for a, b in zip(pitches, pitches[1:])]
    absiv = [abs(i) for i in ivs]
    n_iv = max(1, len(ivs))
    durs = collections.Counter(round(m[2], 3) for m in mel if not m[3])
    graces = sum(1 for m in mel if m[3])
    tuplets = sum(1 for n in rh.flatten().notes if n.duration.tuplets)
    trills = sum(1 for n in rh.flatten().notes for e in n.expressions
                 if isinstance(e, (expressions.Trill, expressions.Turn, expressions.Mordent,
                                   expressions.InvertedMordent, expressions.InvertedTurn)))

    # left hand per bar
    att, lows, spans = [], [], []
    for m in lh.getElementsByClass(stream.Measure):
        ns = list(m.flatten().notes)
        if not ns:
            continue
        ps = [p.midi for n in ns for p in n.pitches]
        att.append(len({round(float(n.offset), 4) for n in ns}))
        lows.append(min(ps))
        spans.append(max(ps) - min(ps))

    # chromaticism relative to the key signature's diatonic set
    tonic_pc = (sharps * 7) % 12
    diatonic = {(tonic_pc + d) % 12 for d in (0, 2, 4, 5, 7, 9, 11)}
    allp = [p.midi for n in s.flatten().notes for p in n.pitches]
    chrom = sum(1 for p in allp if p % 12 not in diatonic) / max(1, len(allp))

    return dict(
        piece=label, file=os.path.basename(path), metre=ts0, key_sig_sharps=sharps, bars=nbars,
        bar_quarters=float(barlen),
        melody=dict(
            notes=len(mel), low=min(pitches), high=max(pitches), median=statistics.median(pitches),
            pct_step=round(100 * sum(1 for i in absiv if 1 <= i <= 2) / n_iv, 1),
            pct_repeat=round(100 * sum(1 for i in absiv if i == 0) / n_iv, 1),
            pct_third=round(100 * sum(1 for i in absiv if 3 <= i <= 4) / n_iv, 1),
            pct_4th_5th=round(100 * sum(1 for i in absiv if 5 <= i <= 7) / n_iv, 1),
            pct_6th_plus=round(100 * sum(1 for i in absiv if i >= 8) / n_iv, 1),
            pct_up=round(100 * sum(1 for i in ivs if i > 0) / n_iv, 1),
            pct_down=round(100 * sum(1 for i in ivs if i < 0) / n_iv, 1),
            largest_leap=max(absiv) if absiv else 0,
            grace_notes=graces, ornaments_marked=trills, tuplet_notes=tuplets,
            top_durations=durs.most_common(6),
        ),
        left_hand=dict(
            attacks_per_bar_median=statistics.median(att) if att else 0,
            lowest_note_median=statistics.median(lows) if lows else 0,
            lowest_note_min=min(lows) if lows else 0,
            span_semitones_median=statistics.median(spans) if spans else 0,
            span_semitones_p90=sorted(spans)[int(0.9 * (len(spans) - 1))] if spans else 0,
        ),
        chromatic_share=round(100 * chrom, 1),
    )


results = []
for label, path in pick_files():
    try:
        r = analyse(label, path)
        if r:
            results.append(r)
            m, l = r["melody"], r["left_hand"]
            print(f"{label:11s} {r['metre']:5s} sig{r['key_sig_sharps']:+d} bars{r['bars']:4d} | mel {m['low']}-{m['high']} med{m['median']:.0f} "
                  f"step{m['pct_step']:5.1f} rep{m['pct_repeat']:5.1f} 3rd{m['pct_third']:5.1f} 4/5{m['pct_4th_5th']:5.1f} 6+{m['pct_6th_plus']:5.1f} "
                  f"grace{m['grace_notes']:4d} tup{m['tuplet_notes']:4d} | LH att{l['attacks_per_bar_median']:5.1f} low{l['lowest_note_median']:5.1f} "
                  f"span{l['span_semitones_median']:5.1f}/{l['span_semitones_p90']} | chrom{r['chromatic_share']:5.1f}%")
    except Exception as ex:  # keep going: a few editions use Humdrum features music21 cannot read
        print(f"{label}: FAILED {type(ex).__name__}: {str(ex)[:100]}")

json.dump(results, open(out_json, "w"), indent=1)
print("wrote", out_json, len(results))
