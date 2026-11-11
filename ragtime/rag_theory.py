"""Proof-reading the rag: harmony, voice leading, playability, and style statistics that
are directly comparable with the Joplin corpus study (research/ragtime_stats.json).

python rag_theory.py
"""
import json, os, statistics, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
from score import chord_pcs
import larkspur_rag as piece

NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
nn = lambda p: f"{NAMES[p % 12]}{p // 12 - 1}"


def check(sc, verbose=True):
    notes = sc.all_notes()
    issues = []
    chord_at = lambda s: chord_pcs(sc.harmony_at(s))
    where = lambda n: f"{sc.tags[n.bar - 1][0]}{sc.tags[n.bar - 1][1]} pos {n.pos:g}"

    # 1 ---- left hand spells the harmony (a passing octave between two chord tones is allowed)
    lh = sorted((n for n in notes if n.hand == "L"), key=lambda n: (n.s, n.pitch))
    bass = [n for n in lh if n.role == "bass" and n.chord_rank == 0]
    for n in lh:
        pcs, b, root = chord_at(n.s)
        if n.pitch % 12 in pcs:
            continue
        if n.role == "bass":
            i = next(k for k, m in enumerate(bass) if abs(m.s - n.s) < 1e-6)
            prv = bass[i - 1].pitch if i else None
            nxt = bass[i + 1].pitch if i + 1 < len(bass) else None
            low = bass[i].pitch                    # judge an octave by its lower note
            if prv is not None and nxt is not None and 1 <= abs(low - prv) <= 2 and 1 <= abs(nxt - low) <= 2:
                continue
        issues.append(f"{where(n)}: LH {n.name} is not in {sc.harmony_at(n.s)}")
    # an inversion written into the harmony ("Eb/Bb") must really have that bass on the downbeat
    for n in bass:
        sym = sc.harmony_at(n.s)
        if abs(n.pos) < 1e-6 and "/" in sym and n.pitch % 12 != chord_at(n.s)[1]:
            issues.append(f"{where(n)}: downbeat bass {n.name} but harmony is {sym}")

    # 2 ---- melody: every non-chord tone is accounted for
    mel = sorted((n for n in notes if n.role == "melody"), key=lambda n: n.s)
    kinds = Counter()
    for i, n in enumerate(mel):
        pcs, _, root = chord_at(n.s)
        pcs2 = chord_at(n.s + max(0.0, n.dur - 0.01))[0]
        if n.pitch % 12 in pcs or n.pitch % 12 in pcs2:
            kinds["chord tone"] += 1; continue
        nxt = mel[i + 1] if i + 1 < len(mel) else None
        prv = mel[i - 1] if i else None
        out = nxt is not None and 1 <= abs(nxt.pitch - n.pitch) <= 2
        inn = prv is not None and 1 <= abs(prv.pitch - n.pitch) <= 2
        if inn and out:
            k = "passing or neighbour note"
        elif out:
            k = "appoggiatura / incomplete neighbour"
        elif nxt is not None and nxt.pitch == n.pitch:
            k = "anticipation"
        else:
            k = "UNRESOLVED"; issues.append(f"{where(n)}: melody {n.name} over {sc.harmony_at(n.s)} is left unresolved")
        kinds[k] += 1

    # 3 ---- outer voices: parallel fifths / octaves on successive bass notes
    pairs = []
    for b in bass:
        cand = [m for m in mel if m.s <= b.s + 1e-6 < m.s + m.dur + 1e-6]
        if cand:
            pairs.append((b, max(c.pitch for c in cand)))
    for (b0, m0), (b1, m1) in zip(pairs, pairs[1:]):
        if b0.pitch % 12 == b1.pitch % 12 or m0 == m1 or b1.s - b0.s > 4 + 1e-6:
            continue                               # same bass note in another octave is not a progression
        if sc.tags[b1.bar - 1][0] == "Intro" and sc.tags[b0.bar - 1][0] == "Intro":
            continue                               # the introduction is a deliberate unison
        i0, i1 = (m0 - b0.pitch) % 12, (m1 - b1.pitch) % 12
        if i0 == i1 and i0 in (0, 7) and (b1.pitch - b0.pitch) * (m1 - m0) > 0:
            issues.append(f"{where(b1)}: parallel {'octaves' if i0 == 0 else 'fifths'} bass/melody "
                          f"({nn(b0.pitch)}/{nn(m0)} -> {nn(b1.pitch)}/{nn(m1)})")

    # 4 ---- hands: spans, collisions, leaps the left hand has to make in an eighth
    toks = {}
    for n in notes:
        toks.setdefault((n.hand, n.s), []).append(n.pitch)
    for (hand, s), ps in toks.items():
        if max(ps) - min(ps) > 12:
            issues.append(f"bar {int(s // 8) + 1} {hand}H: chord spans {max(ps) - min(ps)} semitones")
    for b in sc.bars:
        for n in (m for m in b.notes if m.hand == "L"):
            if any(abs(m.s - n.s) < 1e-6 and m.pitch <= n.pitch for m in b.notes if m.hand == "R"):
                issues.append(f"{where(n)}: hands collide at {n.name}")

    for b in sc.bars:
        for r in (m for m in b.notes if m.hand == "R"):
            for l in (m for m in b.notes if m.hand == "L"):
                if l.pitch == r.pitch and r.s < l.s + l.dur - 1e-6 and l.s < r.s + r.dur - 1e-6:
                    issues.append(f"{where(r)}: both hands want {r.name} at the same time")

    stats = style_stats(sc)
    stats["melody_tone_types"] = dict(kinds)
    if verbose:
        print(f"{sc.title}: {len(sc.bars)} written bars, {len(notes)} notes")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        print(f"issues: {len(issues)}")
        for i in issues:
            print("  !", i)
    return issues, stats


def style_stats(sc):
    """the same measures as research/analyze_ragtime.py"""
    notes = sc.all_notes()
    bars = tied = sls = run = att = octs = chords = lbars = marchb = 0
    top, lows = [], []
    for b in sc.bars:
        rh = {}
        for n in b.notes:
            if n.hand == "R":
                rh.setdefault(int(round(n.pos)), []).append(n.pitch)
        if rh:
            bars += 1
            sl = [k in rh for k in range(8)]
            tied += sl[3] and not sl[4]
            sls += any(sl[q] and sl[q + 1] and not sl[q + 2] and sl[q + 3] for q in (0, 4))
            run += all(sl)
            for k in sorted(rh):
                ps = sorted(rh[k]); att += 1
                octs += len(ps) >= 2 and ps[-1] - ps[0] == 12
                chords += len(ps) >= 2
                top.append(ps[-1])
        lhd = {}
        for n in b.notes:
            if n.hand == "L":
                lhd.setdefault(int(round(n.pos)), []).append(n.pitch)
        if lhd:
            lbars += 1; lows.append(min(min(v) for v in lhd.values()))
            marchb += set(lhd) == {0, 2, 4, 6} and min(lhd[0]) < min(lhd[2]) and min(lhd[4]) < min(lhd[6])
    iv = [abs(y - x) for x, y in zip(top, top[1:])]; k = max(1, len(iv))
    diat = {(3 + d) % 12 for d in (0, 2, 4, 5, 7, 9, 11)}          # E-flat major
    pct = lambda a, b_: round(100 * a / max(1, b_), 1)
    return dict(
        pct_bars_tied_syncopation=pct(tied, bars), pct_bars_short_long_short=pct(sls, bars),
        pct_bars_running_sixteenths=pct(run, bars), pct_attacks_octave=pct(octs, att),
        pct_attacks_chord=pct(chords, att), attacks_per_bar=round(att / bars, 2),
        pct_bars_march_bass=pct(marchb, lbars), lh_lowest_median=statistics.median(lows),
        melody_low=nn(min(top)), melody_high=nn(max(top)), melody_median=statistics.median(top),
        pct_step=pct(sum(1 for i in iv if 1 <= i <= 2), k), pct_repeat=pct(sum(1 for i in iv if i == 0), k),
        pct_third=pct(sum(1 for i in iv if 3 <= i <= 4), k), pct_4th_5th=pct(sum(1 for i in iv if 5 <= i <= 7), k),
        pct_6th_plus=pct(sum(1 for i in iv if i >= 8), k),
        chromatic_share=pct(sum(1 for n in notes if n.pitch % 12 not in diat), len(notes)),
    )


def corpus_compare(stats, path):
    ref = json.load(open(path))["pieces"]
    keys = ["pct_bars_tied_syncopation", "pct_bars_short_long_short", "pct_bars_running_sixteenths",
            "pct_attacks_octave", "pct_attacks_chord", "attacks_per_bar", "pct_bars_march_bass",
            "lh_lowest_median", "melody_median", "pct_step", "pct_repeat", "pct_third", "pct_4th_5th",
            "pct_6th_plus", "chromatic_share"]
    print(f"\nagainst {len(ref)} Joplin rags (min / median / max):")
    inside = 0
    for k in keys:
        v = sorted(r[k] for r in ref if r["bars"] > 40)
        lo, md, hi = v[0], v[len(v) // 2], v[-1]
        ok = lo <= stats[k] <= hi; inside += ok
        print(f"  {k:30s} mine {stats[k]:6.1f}   Joplin {lo:6.1f} / {md:6.1f} / {hi:6.1f}   {'within' if ok else 'OUTSIDE'}")
    print(f"  {inside} of {len(keys)} inside Joplin's range")


if __name__ == "__main__":
    sc = piece.build(written=True)
    issues, stats = check(sc)
    ref = os.path.join(HERE, "..", "research", "ragtime_stats.json")
    if os.path.exists(ref):
        corpus_compare(stats, ref)
