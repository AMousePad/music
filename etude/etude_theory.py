"""Proof-reading Firethorn: harmony, voice leading, and whether two hands can play it.

python etude_theory.py

  1  every accompanying note (bass, chords, arpeggios, inner notes) belongs to the stated harmony
  2  every note of a line that is not a chord tone is accounted for (passing, neighbour,
     appoggiatura, anticipation); the augmented seconds of the Hungarian scale count as steps
  3  bell notes are chord tones or the dominant pedal
  4  no parallel fifths or octaves between bass and top line
  5  playability, at the planned tempo and against limits measured on recordings of
     La Campanella, the Hungarian Rhapsodies and the Transcendental Etudes:
     chord spans, hand crossings, shared keys, leaps, repeated keys, octave and chord speed
"""
import json, os, statistics, sys
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
from score import chord_pcs
import firethorn as piece

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
nn = lambda p: f"{NAMES[p % 12]}{p // 12 - 1}"
HUNG = ({9, 0}, {2, 5})                    # A-B# and D-E#: the augmented seconds of the Hungarian minor on F#

# limits (seconds), from research/virtuoso_stats.json where available
LIMITS = dict(repeat=0.085, single=0.062, octave=0.095, chord=0.105, leap12=0.090, leap17=0.115, leap24=0.150, leap36=0.300)


def step(a, b):
    d = abs(a - b)
    return 1 <= d <= 2 or (d == 3 and {a % 12, b % 12} in HUNG)


def seconds_fn(sc):
    """nominal time (s) of a score position, from the tempo plan (no breaths)"""
    ds = 0.125
    grid = np.arange(0, sc.length + ds, ds)
    bpm = piece.span_curve(sc, piece.TEMPO, grid)
    t = np.concatenate([[0.0], np.cumsum(15.0 / bpm[:-1] * ds)])
    return lambda s: float(np.interp(s, grid, t))


def lines(sc, notes):
    """the melodic lines to be checked: (name, [notes]) with repeated pitches merged"""
    upper, lower = [], []
    by_on = {}
    for n in notes:
        by_on.setdefault(round(n.s, 4), []).append(n)
    for s in sorted(by_on):
        grp = by_on[s]
        tx = sc.bars[grp[0].bar - 1].texture
        r = [n for n in grp if n.hand == "R" and n.grace is None
             and (n.role in ("melody", "run") or (n.role == "bell" and tx == "bell"))]
        l = [n for n in grp if n.hand == "L" and n.role == "run"]
        if tx in piece.LINE_TX:
            if tx == "interlock":                       # the thumbs carry the line
                if r and all(m.role == "run" for m in r) and len(r) <= 2:
                    upper.append(min(r, key=lambda n: n.pitch))
                elif l:
                    upper.append(max(l, key=lambda n: n.pitch))
                elif r:
                    upper.append(max(r, key=lambda n: n.pitch))
            else:
                cand = r + l
                if cand:
                    upper.append(max(cand, key=lambda n: n.pitch))
        else:
            if r:
                upper.append(max(r, key=lambda n: n.pitch))
            if l:
                lower.append(max(l, key=lambda n: n.pitch))
    return [("line", upper), ("left-hand run", lower)]


def check(sc, verbose=True):
    notes = sc.all_notes()
    issues = []
    chord_at = lambda s: chord_pcs(sc.harmony_at(s))
    tx = lambda n: sc.bars[n.bar - 1].texture
    where = lambda n: f"{sc.tags[n.bar - 1][0]} {sc.tags[n.bar - 1][1]} pos {n.pos:g}"
    T = seconds_fn(sc)

    by_on = {}
    for n in notes:
        by_on.setdefault((n.hand, round(n.s, 4)), []).append(n)

    # 1 ---- accompanying notes spell the harmony
    for n in notes:
        if n.role not in ("bass", "acc", "arp", "rh_inner") or n.grace is not None:
            continue
        pcs = chord_at(n.s)[0]
        if n.pitch % 12 in pcs:
            continue
        mates = by_on[(n.hand, round(n.s, 4))]
        if n.role == "rh_inner" and any(m.pitch % 12 == n.pitch % 12 and m.role in ("melody", "run", "bell") for m in mates):
            continue                                    # octave doubling of the line
        if tx(n) in ("recit", "unison"):
            other = by_on.get(("R", round(n.s, 4)), [])
            if any(m.pitch % 12 == n.pitch % 12 for m in other):
                continue                                # the hands are in unison
        issues.append(f"{where(n)}: {n.role} {n.name} is not in {sc.harmony_at(n.s)}")

    # 2 ---- lines
    kinds = Counter()
    for lname, raw in lines(sc, notes):
        seq = []                                        # merge immediate repetitions
        for n in raw:
            if seq and seq[-1][0].pitch == n.pitch and n.s - (seq[-1][0].s + seq[-1][1]) < 2.01:
                seq[-1][1] = n.s + n.dur - seq[-1][0].s
            else:
                seq.append([n, n.dur])
        for i, (n, d) in enumerate(seq):
            pcs = chord_at(n.s)[0]
            pcs2 = chord_at(n.s + max(0.0, d - 0.01))[0]
            if n.pitch % 12 in pcs or n.pitch % 12 in pcs2:
                kinds["chord tone"] += 1; continue
            prv = seq[i - 1][0] if i else None
            nxt = seq[i + 1][0] if i + 1 < len(seq) else None
            inn = prv is not None and step(prv.pitch, n.pitch)
            out = nxt is not None and step(nxt.pitch, n.pitch)
            if inn and out:
                k = "passing or neighbour note"
            elif out:
                k = "appoggiatura / incomplete neighbour"
            else:
                k = "UNRESOLVED"
                issues.append(f"{where(n)}: {lname} {n.name} over {sc.harmony_at(n.s)} is left unresolved")
            kinds[k] += 1

    # 3 ---- the bell
    bells = [n for n in notes if n.role == "bell"]
    for i, n in enumerate(bells):
        if n.pitch % 12 in chord_at(n.s)[0] or n.pitch % 12 == 1:
            continue
        issues.append(f"{where(n)}: bell {n.name} is neither in {sc.harmony_at(n.s)} nor the dominant pedal")

    # 4 ---- outer voices
    top = [n for lname, raw in lines(sc, notes) if lname == "line" for n in raw]
    bass = []
    for n in notes:
        t = tx(n)
        if t in piece.LINE_TX or t in ("recit", "unison"):
            continue
        if n.hand == "L" and n.chord_rank == 0 and (n.role == "bass" or (t == "run_lh" and abs(n.pos) < 1e-6)):
            bass.append(n)
    pairs = []
    for b in bass:
        cand = [m for m in top if m.s <= b.s + 1e-6 and b.s < m.s + max(m.dur, 2.0) + 1e-6]
        if cand:
            pairs.append((b, cand[-1].pitch))
    for (b0, m0), (b1, m1) in zip(pairs, pairs[1:]):
        if b0.pitch % 12 == b1.pitch % 12 or m0 == m1 or b1.s - b0.s > 8 + 1e-6:
            continue
        i0, i1 = (m0 - b0.pitch) % 12, (m1 - b1.pitch) % 12
        if i0 == i1 and i0 in (0, 7) and (b1.pitch - b0.pitch) * (m1 - m0) > 0:
            issues.append(f"{where(b1)}: parallel {'octaves' if i0 == 0 else 'fifths'} bass/top "
                          f"({nn(b0.pitch)}/{nn(m0)} -> {nn(b1.pitch)}/{nn(m1)})")

    # 5 ---- hands
    hard = Counter()
    for hand in "RL":
        ev = sorted(((s, ns) for (h, s), ns in by_on.items() if h == hand), key=lambda e: e[0])
        ev = [(s, [m for m in ns if m.grace is None]) for s, ns in ev]
        ev = [(s, ns) for s, ns in ev if ns]
        last_key = {}
        for i, (s, ns) in enumerate(ev):
            ps = sorted(m.pitch for m in ns)
            if ps[-1] - ps[0] > 12:
                issues.append(f"{where(ns[0])}: {hand}H chord spans {ps[-1] - ps[0]} semitones")
            for m in ns:
                if m.pitch in last_key and T(s) - T(last_key[m.pitch]) < LIMITS["repeat"] - 1e-4:
                    issues.append(f"{where(m)}: {hand}H repeats {m.name} after {1000 * (T(s) - T(last_key[m.pitch])):.0f} ms")
                last_key[m.pitch] = s
            if i == 0:
                continue
            s0, ns0 = ev[i - 1]
            p0 = sorted(m.pitch for m in ns0)
            dt = T(s) - T(s0)
            kind = "single" if len(ps) == 1 and len(p0) == 1 else ("chord" if len(ps) >= 3 and len(p0) >= 3 else "octave")
            if dt < LIMITS[kind] - 1e-4:
                issues.append(f"{where(ns[0])}: {hand}H {kind}s {1000 * dt:.0f} ms apart")
            if max(ps[-1], p0[-1]) - min(ps[0], p0[0]) > 12:            # does not fit under one hand position
                d = abs((ps[0] + ps[-1]) / 2 - (p0[0] + p0[-1]) / 2)
                for lim, key in ((36, "leap36"), (24, "leap24"), (17, "leap17"), (12, "leap12")):
                    if d >= lim:
                        hard[key] += 1
                        if dt < LIMITS[key] - 1e-4:
                            issues.append(f"{where(ns[0])}: {hand}H leaps {d:.0f} semitones in {1000 * dt:.0f} ms")
                        break
    for b in sc.bars:
        if b.texture in piece.LINE_TX:
            continue
        R = [m for m in b.notes if m.hand == "R" and m.grace is None]
        L = [m for m in b.notes if m.hand == "L"]
        for l in L:
            for r in R:
                if abs(l.s - r.s) < 1e-6 and l.pitch > r.pitch and not (b.texture == "sing" and r.voice == "rh2"):
                    issues.append(f"{where(l)}: hands cross ({l.name} above {r.name})")
                if l.pitch == r.pitch and r.s < l.s + l.dur - 1e-6 and l.s < r.s + r.dur - 1e-6:
                    issues.append(f"{where(r)}: both hands want {r.name} at the same time")

    stats = dict(bars=len(sc.bars), notes=len(notes), lowest=nn(min(n.pitch for n in notes)), highest=nn(max(n.pitch for n in notes)),
                 nominal_seconds=round(T(sc.length), 1), line_tone_types=dict(kinds), bell_notes=len(bells),
                 leaps_over_an_octave=dict(hard), sections={name: len(bars) for name, bars in piece.SECTIONS})
    if verbose:
        print(f"{sc.title}: {len(sc.bars)} bars, {len(notes)} notes, {stats['lowest']} to {stats['highest']}, "
              f"{stats['nominal_seconds']} s at the planned tempi (before breaths and fermatas)")
        print("  line tones:", dict(kinds))
        print("  leaps beyond one hand position:", dict(hard))
        print(f"issues: {len(issues)}")
        for i in issues:
            print("  !", i)
    return issues, stats


if __name__ == "__main__":
    check(piece.build())
