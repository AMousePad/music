"""Proof-reading the composition: harmony, voice leading, playability, style statistics.

python theory.py            -> report for the nocturne
"""
import json, os, statistics, sys
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from score import chord_pcs

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def nn(p):
    return f"{NAMES[p % 12]}{p // 12 - 1}"


def check(sc, verbose=True):
    notes = sc.all_notes()
    issues, info = [], []

    def chord_at(s):
        return chord_pcs(sc.harmony_at(s))

    # 1 ---- left hand must spell the harmony
    for n in notes:
        if n.hand != "L":
            continue
        pcs, bass, root = chord_at(n.s)
        if n.pitch % 12 not in pcs:
            issues.append(f"bar {n.bar} pos {n.pos:g}: LH {n.name} is not in {sc.harmony_at(n.s)}")
        if n.role == "bass" and n.pos in [p for p, _ in sc.bars[n.bar - 1].harmony] and n.pitch % 12 != bass:
            issues.append(f"bar {n.bar} pos {n.pos:g}: bass {n.name} but harmony {sc.harmony_at(n.s)} wants another bass")

    # 2 ---- melody: every non-chord tone has to go somewhere by step
    mel = [n for n in notes if n.role == "melody" and n.voice == "rh" and n.grace is None]
    mel.sort(key=lambda n: n.s)
    nct = Counter()
    for i, n in enumerate(mel):
        pcs, _, root = chord_at(n.s)
        pcs_end, _, _ = chord_at(n.s + max(0.0, n.dur - 0.01))
        if n.pitch % 12 in pcs or n.pitch % 12 in pcs_end:
            nct["chord tone"] += 1
            continue
        nxt = mel[i + 1] if i + 1 < len(mel) else None
        prv = mel[i - 1] if i else None
        step_out = nxt is not None and 1 <= abs(nxt.pitch - n.pitch) <= 2
        step_in = prv is not None and 1 <= abs(prv.pitch - n.pitch) <= 2
        strong = abs(n.pos % 3) < 1e-6
        if nxt is not None and nxt.pitch == n.pitch and n.dur <= 1 and (nxt.pitch % 12 in chord_at(nxt.s)[0]):
            kind = "anticipation"
        elif step_out and strong and n.dur >= 2:
            kind = "appoggiatura / accented dissonance"
        elif step_in and step_out:
            kind = "passing or neighbour note"
        elif step_out:
            kind = "incomplete neighbour (leap in, step out)"
        elif step_in and nxt is not None and abs(nxt.pitch - n.pitch) in (3, 4):
            kind = "escape / changing note (step in, third out)"
        elif (n.pitch - root) % 12 in (1, 2, 9, 8) and nxt is not None:
            kind = "chord extension (9th/13th) left by leap"
        else:
            kind = "UNRESOLVED"
            issues.append(f"bar {n.bar} pos {n.pos:g}: melody {n.name} over {sc.harmony_at(n.s)} is left unresolved")
        nct[kind] += 1

    # 3 ---- outer voices: no parallel fifths or octaves
    bass = sorted((n for n in notes if n.role == "bass" and n.chord_rank == 0), key=lambda n: n.s)
    pairs = []
    for b in bass:
        cand = [m for m in mel if m.s <= b.s + 1e-6 < m.s + max(m.dur, 0.01) + 1e-6]
        if cand:
            pairs.append((b.s, b.pitch, max(c.pitch for c in cand), b.bar, b.pos))
    for (s0, b0, m0, *_), (s1, b1, m1, bar, pos) in zip(pairs, pairs[1:]):
        if b0 == b1 or m0 == m1:
            continue
        i0, i1 = (m0 - b0) % 12, (m1 - b1) % 12
        same_dir = (b1 - b0) * (m1 - m0) > 0
        if i0 == i1 and i0 in (0, 7) and same_dir:
            issues.append(f"bar {bar} pos {pos:g}: parallel {'octaves' if i0 == 0 else 'fifths'} between bass and melody "
                          f"({nn(b0)}/{nn(m0)} -> {nn(b1)}/{nn(m1)})")

    # 4 ---- hands
    by_tok = {}
    for n in notes:
        if n.grace is None and n.group is None:
            by_tok.setdefault((n.voice, n.s), []).append(n.pitch)
    for (voice, s), ps in by_tok.items():
        span = max(ps) - min(ps)
        if span > 12 and (voice.startswith("rh") or span > 16):
            issues.append(f"bar {int(s // sc.bar_len) + 1} {voice}: chord spans {span} semitones (needs rolling)")
    for b in sc.bars:
        lh = sorted((n for n in b.notes if n.hand == "L"), key=lambda n: n.s)
        rh = [n for n in b.notes if n.hand == "R"]
        for n in lh:
            clash = [m for m in rh if abs(m.s - n.s) < 1e-6 and m.pitch <= n.pitch]
            if clash:
                issues.append(f"bar {b.number} pos {n.pos:g}: hands cross / collide at {n.name}")

    # 5 ---- style statistics (comparable to research/score_stats.json)
    seq = [n.pitch for n in mel]
    iv = [abs(b - a) for a, b in zip(seq, seq[1:])]
    k = max(1, len(iv))
    lows, spans, att = [], [], []
    for b in sc.bars:
        lh = [n for n in b.notes if n.hand == "L"]
        if lh:
            lows.append(min(n.pitch for n in lh)); spans.append(max(n.pitch for n in lh) - min(n.pitch for n in lh))
            att.append(len({round(n.s, 4) for n in lh}))
    diat = {(11 + d) % 12 for d in (0, 2, 3, 5, 7, 8, 10)}          # B natural minor
    chrom = sum(1 for n in notes if n.pitch % 12 not in diat) / len(notes)
    stats = dict(
        bars=len(sc.bars), notes=len(notes), melody_notes=len(mel),
        melody_low=nn(min(seq)), melody_high=nn(max(seq)), melody_median=nn(int(statistics.median(seq))),
        pct_step=round(100 * sum(1 for i in iv if 1 <= i <= 2) / k, 1),
        pct_repeat=round(100 * sum(1 for i in iv if i == 0) / k, 1),
        pct_third=round(100 * sum(1 for i in iv if 3 <= i <= 4) / k, 1),
        pct_4th_5th=round(100 * sum(1 for i in iv if 5 <= i <= 7) / k, 1),
        pct_6th_plus=round(100 * sum(1 for i in iv if i >= 8) / k, 1),
        grace_notes=sum(1 for n in notes if n.grace is not None),
        fioritura_notes=sum(1 for n in notes if n.group is not None),
        lh_attacks_per_bar_median=statistics.median(att), lh_lowest_median=nn(int(statistics.median(lows))),
        lh_span_median=statistics.median(spans), chromatic_share=round(100 * chrom, 1),
        melody_tone_types=dict(nct),
    )
    if verbose:
        print(f"{sc.title}: {stats['bars']} bars, {stats['notes']} notes")
        for kx, v in stats.items():
            print(f"  {kx}: {v}")
        print(f"issues: {len(issues)}")
        for i in issues:
            print("  !", i)
    return issues, stats


def corpus_compare(stats, path):
    ref = json.load(open(path))
    def rng(f):
        v = sorted(f(r) for r in ref)
        return v[1], v[len(v) // 2], v[-2]
    rows = [("% stepwise", stats["pct_step"], rng(lambda r: r["melody"]["pct_step"])),
            ("% repeated", stats["pct_repeat"], rng(lambda r: r["melody"]["pct_repeat"])),
            ("% thirds", stats["pct_third"], rng(lambda r: r["melody"]["pct_third"])),
            ("% 4ths/5ths", stats["pct_4th_5th"], rng(lambda r: r["melody"]["pct_4th_5th"])),
            ("% 6ths+", stats["pct_6th_plus"], rng(lambda r: r["melody"]["pct_6th_plus"])),
            ("LH span (st)", stats["lh_span_median"], rng(lambda r: r["left_hand"]["span_semitones_median"])),
            ("chromatic %", stats["chromatic_share"], rng(lambda r: r["chromatic_share"]))]
    print("\nagainst Chopin's 19 nocturnes (2nd-lowest / median / 2nd-highest):")
    for name, mine, (lo, md, hi) in rows:
        flag = "ok" if lo <= mine <= hi else "outside"
        print(f"  {name:14s} mine {mine:6.1f}   corpus {lo:5.1f} / {md:5.1f} / {hi:5.1f}   {flag}")


if __name__ == "__main__":
    import nocturne_bm
    sc = nocturne_bm.build()
    issues, stats = check(sc)
    ref = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "research", "score_stats.json")
    if os.path.exists(ref):
        corpus_compare(stats, ref)
