"""The virtuoso.

A third player, after the nocturne's and the rag's.  The rules are explicit and each one
is either standard practice for this repertoire or taken from the measurements in
../../research/virtuoso_stats.json (46 recordings of La Campanella, the Hungarian
Rhapsodies and the Transcendental Etudes):

  time      a tempo plan per section (firethorn.TEMPO): free in the introduction, strict in
            the variations, breathing in four-bar arches in the cantabile, pressing forward
            through the coda.  Time is taken, not stretched, at the joins (BREATHS).
  touch     every texture has its own:
              staccato   theme, bell variation, light friska  - eighths short, sixteenths bound
              perle      running lines                        - each key released just before
                                                                the next (measured key-hold
                                                                ratio of fast notes: 0.5-0.8)
              repeat     repeated notes                       - half the gap, so the key is back
              legato     cantabile                            - melody overlapped, the rest in
                                                                the pedal
              marcato    octaves and chords                   - weight, slightly detached
              martellato alternating hands                    - short, equal, hammered
  balance   the line above everything; the bell lighter than the tune it answers; bass
            octaves firm, after-beat chords well under; arpeggios under the melody;
            running lines follow their contour (louder upward)
  pedal     dabs with the bass in the staccato textures, none in the relayed line, changes
            on every beat or harmony under octaves and arpeggios, long in the introduction
"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "engine"))
from midi_out import PerformanceOutput
import firethorn as piece

TOUCH = dict(recit="marcato", bell="bell", arioso="legato", cadenza="perle", theme="stacc", relay="perle",
             run_rh="perle", run_lh="perle", campanella="stacc", repeat="repeat", sing="legato", sing8="legato",
             apoth="legato", retrans="perle", unison="marcato", bravura="marcato", friska="stacc",
             friska8="marcato", interlock="martel", martel="martel", final="marcato")
PEDAL = dict(recit="note", bell="bar", arioso="harm", cadenza="bar", theme="dab", relay="none", run_rh="dab",
             run_lh="beat", campanella="dab", repeat="dab2", sing="harm", sing8="harm", apoth="harm",
             retrans="bar", unison="beat", bravura="dabhold", friska="dab", friska8="dabhold",
             interlock="beat", martel="harm", final="harm")
PEDAL_AT = {("Intro", 12): "bar", ("Retrans", 5): "hold", ("Coda", 35): "bar", ("Coda", 36): "hold", ("Coda", 41): "bar"}
MEL_GAIN = dict(sing=9, sing8=8, arioso=8, apoth=4, recit=3, theme=4, campanella=4, friska=4, repeat=3, final=4)


class Virtuoso(PerformanceOutput):
    def __init__(self, sc, plan=None, seed=1851):
        self.sc, self.plan = sc, plan or piece.PLAN
        self.rng = np.random.default_rng(seed)
        self.notes = sc.all_notes()
        self._time_map()

    # ------------------------------------------------------------------ time
    def _time_map(self):
        sc, plan, rng = self.sc, self.plan, self.rng
        ds = 1.0 / 16
        grid = np.arange(0, sc.length + ds, ds)
        bpm = piece.span_curve(sc, plan["tempo"], grid)
        nb = len(sc.bars)
        # the cantabile breathes in four-bar arches: ease in, move, broaden
        for name, amp in plan.get("arch", {}).items():
            first = sc.where[(name, 1)] - 1
            for b0 in range(first, first + 16, 4):
                a, b = b0 * 8.0, (b0 + 4) * 8.0
                m = (grid >= a) & (grid < b)
                x = (grid[m] - a) / (b - a)
                bpm[m] *= 1 + amp * (np.sin(np.pi * x) - 0.55 * (1 - x) ** 6 - 1.1 * x ** 7)
        # nobody is a metronome: a slow drift of a few tenths of a percent
        drift = np.cumsum(rng.normal(0, 0.0022, nb))
        drift -= np.linspace(0, drift[-1], nb)
        bpm *= 1 + drift[np.minimum(nb - 1, (grid // 8).astype(int))]
        self.grid, self.bpm_grid = grid, bpm
        self.tgrid = np.concatenate([[0.0], np.cumsum(15.0 / bpm[:-1] * ds)])
        self.level_grid = piece.span_curve(sc, plan["level"], grid)
        self.breaths = sorted(((sc.where[(n, b)] - 1) * 8.0 + p, sec) for n, b, p, sec in plan["breaths"])

    def S(self, name, bar, pos=0.0):
        return (self.sc.where[(name, bar)] - 1) * 8.0 + pos

    def t(self, s):
        base = float(np.interp(s, self.grid, self.tgrid))
        return base + sum(sec for sb, sec in self.breaths if sb <= s + 1e-9) + 1.0

    def level(self, s):
        return float(np.interp(s, self.grid, self.level_grid))

    def bpm(self, s):
        return float(np.interp(s, self.grid, self.bpm_grid))

    # ------------------------------------------------------------------ performance
    def perform(self):
        sc, rng = self.sc, self.rng
        notes = [n for n in self.notes]
        nbars = len(sc.bars)
        tx_of = lambda n: sc.bars[n.bar - 1].texture

        # onsets of each hand, and of the shared line in relay textures
        on_hand = {"R": sorted({round(n.s, 5) for n in notes if n.hand == "R" and n.grace is None}),
                   "L": sorted({round(n.s, 5) for n in notes if n.hand == "L"})}
        on_all = sorted(set(on_hand["R"]) | set(on_hand["L"]))
        on_mel = sorted({round(n.s, 5) for n in notes if n.role == "melody" and n.grace is None})

        def nxt(arr, s):
            i = np.searchsorted(arr, round(s, 5) + 1e-6)
            return arr[i] if i < len(arr) else None

        tok = {}
        for n in notes:
            tok.setdefault((n.hand, round(n.s, 5)), []).append(n)
        run_med = {}
        for b in sc.bars:
            for hand in "RL":
                ps = [n.pitch for n in b.notes if n.role == "run" and n.hand == hand]
                if ps:
                    run_med[(b.number, hand)] = float(np.median(ps))
        shift = {}

        def hand_shift(n, fast):
            key = (round(n.s, 5), n.hand)
            if key not in shift:
                sd = 0.004 if fast else 0.011
                shift[key] = float(np.clip(rng.normal(0.0, sd), -2.5 * sd, 2.5 * sd)) if n.hand == "R" else 0.0
            return shift[key]

        ev = []
        prev_mel = None
        rep_k = 0
        for n in notes:
            tx = tx_of(n)
            touch = TOUCH[tx]
            L = self.level(n.s)
            vb = 36.0 + 62.0 * L
            t0, t1 = self.t(n.s), self.t(n.s + max(n.dur, 0.0))
            d = t1 - t0
            fast = self.bpm(n.s) >= 90
            mates = tok[(n.hand, round(n.s, 5))]
            line = on_all if tx in piece.LINE_TX else on_hand[n.hand]
            sn = nxt(line, n.s)
            tn = self.t(sn) if sn is not None else t1 + 1.0
            ioi = tn - t0
            rest_follows = sn is None or sn > n.s + n.dur + 1e-6
            final_bar = n.bar == nbars
            beat0, beat = abs(n.pos) < 1e-6, abs(n.pos % 4) < 1e-6
            on = t0 + hand_shift(n, fast) + rng.normal(0, 0.003 if fast else 0.006)
            role = n.role

            # ---------------------------------------------------- how loud
            if n.grace is not None:
                k, cnt = n.grace
                on = t0 - 0.055 * (cnt - k) + rng.normal(0, 0.002)
                off = t0 + 0.02
                v = vb - 4
            elif role == "melody":
                v = vb + MEL_GAIN.get(tx, 3)
                v += 2.0 if beat0 else (1.0 if beat else 0.0)
                if touch in ("stacc", "marcato") and n.dur <= 1:
                    v -= 3.0
                if n.dur >= 4:
                    v += 2.0
                if touch != "legato":
                    v += float(np.clip(0.15 * (n.pitch - 78), -3, 3))
                elif prev_mel is not None and 1 <= prev_mel.pitch - n.pitch <= 2 and abs(prev_mel.pos % 4) < 1e-6 and prev_mel.dur >= n.dur:
                    v -= 3.0                                      # the resolution is softer than the leaning note
                if tx == "repeat":
                    rep_k = rep_k + 1 if (prev_mel is not None and prev_mel.pitch == n.pitch and n.s - prev_mel.s < 1.01) else 0
                    v += [3.0, -4.0, -5.0, -2.5][min(rep_k, 3)]
                if "!" in n.flags: v += 8
                if "_" in n.flags: v += 4
                prev_mel = n
            elif role == "rh_inner":
                doubling = any(m.pitch - n.pitch == 12 and m.role == "melody" for m in mates)
                v = vb - (3.5 if doubling and touch == "marcato" else (5.0 if doubling else 8.0))
                if tx == "sing8" and not doubling:
                    v -= 2.0
            elif role == "bell":
                v = max(vb + 6.0, 60.0) if tx == "bell" else max(vb - 3.0, 46.0)   # alone, the bell has to carry
            elif role == "run":
                med = run_med.get((n.bar, n.hand), n.pitch)
                v = vb + 1.0 + float(np.clip(0.20 * (n.pitch - med), -5, 5)) + (2.5 if beat else 0.0)
                if tx == "run_lh":
                    v -= 5.0
                if touch == "martel":
                    thumb = (n.hand == "R" and n.chord_rank == 0 and n.chord_size == 2) or (n.hand == "L" and n.chord_rank == 1)
                    v += -4.0 if thumb else 2.0
                if "!" in n.flags: v += 8
            elif role == "bass":
                v = vb - {"sing": 10.0, "sing8": 9.0, "apoth": 3.0, "recit": 1.0, "unison": 1.0, "retrans": 7.0}.get(tx, 5.0)
                v += 2.0 if beat0 else 0.0
                if n.chord_size > 1 and n.chord_rank > 0:
                    v -= 4.0
            elif role == "acc":
                v = vb - (12.0 if tx == "repeat" else 15.0) + (1.0 if n.chord_rank == n.chord_size - 1 else 0.0)
                if touch == "martel":
                    v = vb - 3.0
            else:                                                 # arpeggio
                v = vb - 17.0 + float(np.clip(0.10 * (n.pitch - 60), -3, 3))
                if tx == "sing":                                  # figuration around a tenor melody: a murmur
                    v -= 3.0 if n.hand == "R" else 2.0

            # ---------------------------------------------------- how long
            if n.grace is not None:
                pass
            elif final_bar:
                off = t1 + self.plan["final_hold"]
            elif touch == "bell":
                off = t0 + 0.9 * d
            elif touch == "legato":
                if role == "melody":
                    sm = nxt(on_mel, n.s)
                    off = (self.t(sm) + 0.02) if (sm is not None and sm <= n.s + n.dur + 1e-6) else t1 - 0.03
                elif role == "arp":
                    off = tn + 0.03 if not rest_follows else t1
                elif role == "bass":
                    off = max(t0 + 0.9 * d, t0 + 0.45)
                else:
                    off = t1 - 0.04
            elif touch == "repeat":
                if role in ("melody",):
                    off = t0 + max(0.035, min(0.55 * ioi, ioi - 0.030)) if not rest_follows else t0 + 0.7 * d
                elif role == "bell":
                    off = t0 + min(0.6 * d, 0.18)
                else:
                    off = t0 + 0.50 * d
            elif touch == "stacc":
                if role == "bell":
                    off = t0 + min(0.6 * d, 0.16)
                elif role in ("melody", "rh_inner"):
                    off = t0 + min(0.50 * d, 0.20) if n.dur >= 2 else (t0 + 0.72 * d if rest_follows else min(tn - 0.008, t0 + 0.9 * d))
                elif role == "bass":
                    off = t0 + 0.55 * d
                else:
                    off = t0 + min(0.45 * d, 0.16)
            elif touch == "perle":
                if role == "run":
                    hold = rng.uniform(0.56, 0.90)
                    off = t0 + hold * ioi if not rest_follows else t0 + 0.8 * d
                elif role == "bass":
                    off = t0 + 0.55 * d
                elif role == "acc":
                    off = t0 + min(0.45 * d, 0.16)
                else:                                             # chords and short figures over a running hand
                    off = t0 + (0.60 * d if n.dur >= 2 else 0.85 * d)
            elif touch == "martel":
                off = t0 + 0.80 * d if n.dur <= 1 else t0 + 0.85 * d
            else:                                                 # marcato
                if tx == "recit":
                    off = t1 - 0.03 if n.dur >= 3 else t0 + 0.9 * d
                elif role == "acc":
                    off = t0 + 0.50 * d
                elif n.dur <= 1:
                    off = t0 + 0.70 * d
                else:
                    off = t0 + 0.82 * d

            # ---------------------------------------------------- inside a chord
            if n.grace is None and n.chord_size > 1:
                if tx in ("apoth", "final") and n.chord_size >= 4:
                    on += 0.011 * n.chord_rank                    # full chords are spread a little, bottom to top
                elif tx == "arioso" and n.hand == "L" and n.chord_size >= 3:
                    on += 0.022 * n.chord_rank
                else:
                    on -= 0.0025 * (n.chord_size - 1 - n.chord_rank)
            if tx == "final":
                v += 5.0                                          # the last chords carry the whole arm
            v += rng.normal(0, 1.6)
            ev.append(dict(on=on, off=max(off, on + 0.04), pitch=n.pitch, vel=int(np.clip(round(v), 22, 122)), role=role,
                           bar=n.bar, pos=n.pos, s=n.s, hand=n.hand, name=n.name, dur=n.dur, tx=tx))
        ev.sort(key=lambda e: e["on"])
        self.events = ev
        self.sustain = self._pedal()
        self.soft = self._una_corda()
        return ev

    # ------------------------------------------------------------------ feet
    def _pedal(self):
        sc, rng = self.sc, self.rng
        seg = []                                   # (t_down, t_up, depth)
        open_at = None                             # start of the legato pedal that is currently down

        def depth(s, light=False):
            L = self.level(s)
            return float(np.clip((0.56 if light else 0.62) + 0.30 * L + rng.uniform(-0.04, 0.07), 0.5, 1.0))

        def close(t_up):
            nonlocal open_at
            if open_at is not None:
                seg.append((open_at[0], t_up, open_at[1])); open_at = None

        for b in sc.bars:
            name, k = sc.tags[b.number - 1]
            style = PEDAL_AT.get((name, k), PEDAL[b.texture])
            s0 = (b.number - 1) * 8.0
            lh = sorted({round(n.s, 5) for n in b.notes if n.hand == "L"})
            bass = sorted({round(n.s, 5) for n in b.notes if n.hand == "L" and n.role == "bass"})
            if style in ("none", "dab", "dab2", "dabhold"):
                close(self.t(s0) - 0.02)
                if style == "none":
                    continue
                for i, s in enumerate(bass):
                    after = [x for x in lh if x > s + 1e-6]
                    if style == "dab":
                        if not after:
                            continue
                        up = self.t(after[0]) - 0.02
                    elif style == "dab2":
                        up = self.t(s0 + 4.0) - 0.03
                    else:
                        up = self.t(bass[i + 1] if i + 1 < len(bass) else s0 + 8.0) - 0.03
                    if up - self.t(s) > 0.10:
                        seg.append((self.t(s) + 0.03, up, depth(s, light=style != "dabhold")))
                continue
            if style == "hold":
                if open_at is None:
                    open_at = (self.t(s0) + 0.04, depth(s0))
                continue
            if style == "bar":
                pts = [s0]
            elif style == "beat":
                pts = [s0, s0 + 4.0]
            elif style == "harm":
                pts = sorted({s0} | {s0 + p for p, _ in b.harmony})
            else:                                  # "note": every long note of the declamation
                pts = sorted({round(n.s, 5) for n in b.notes if n.hand == "L" and n.dur >= 3} | {s0})
            for s in pts:
                tc = self.t(s)
                if open_at is None:
                    open_at = (tc + 0.04, depth(s))
                else:                              # syncopated change: up just after the new attack, down again at once
                    close(tc + 0.02 + rng.uniform(0, 0.015))
                    open_at = (tc + 0.105 + rng.uniform(0, 0.02), depth(s))
        t_end = max(e["off"] for e in self.events)
        close(t_end + 0.3)
        # rasterise: a foot is not a switch (about 45 ms down, 35 ms up)
        tt = np.arange(0, t_end + 3.0, 0.005)
        P = np.zeros_like(tt)
        for a, b, dpt in seg:
            if b <= a:
                continue
            env = np.clip((tt - a) / 0.045, 0, 1) * np.clip((b + 0.035 - tt) / 0.035, 0, 1)
            P = np.maximum(P, dpt * env)
        last = seg[-1]
        tail = (tt > last[1]) & (tt < last[1] + 1.6)
        P[tail] = np.maximum(P[tail], last[2] * (1 - (tt[tail] - last[1]) / 1.6))
        return (list(tt), list(P))

    def _una_corda(self):
        pts = [(0.0, 0.0)]
        for (n0, b0), (n1, b1) in self.plan["una_corda"]:
            pts.append((max(0.0, self.t(self.S(n0, b0)) - 0.2), 1.0))
            pts.append((self.t(self.S(n1, b1, 8.0)) - 0.1, 0.0))
        pts.sort()
        return ([p[0] for p in pts], [p[1] for p in pts])

    # ------------------------------------------------------------------ report
    def summary(self):
        ev = self.events
        v = np.array([e["vel"] for e in ev])
        tb = np.array([self.t(i * 8.0) for i in range(len(self.sc.bars) + 1)])
        tt, pv = np.array(self.sustain[0]), np.array(self.sustain[1])
        end = max(e["off"] for e in ev)
        down = pv[tt < end] > 0.5
        sec = {}
        for i, (name, k) in enumerate(self.sc.tags):
            sec.setdefault(name, [tb[i], tb[i + 1]])[1] = tb[i + 1]
        return dict(seconds=float(end), key_strokes=len(ev), notes_per_second=float(len(ev) / (end - 1.0)),
                    vel_p05=float(np.percentile(v, 5)), vel_p50=float(np.percentile(v, 50)), vel_p95=float(np.percentile(v, 95)),
                    vel_max=int(v.max()), pedal_share_down=float(down.mean()),
                    sections={k: dict(start=round(float(a), 1), seconds=round(float(b - a), 1)) for k, (a, b) in sec.items()})
