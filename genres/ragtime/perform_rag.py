"""The ragtime pianist.

A different player from the nocturne's.  What the sources ask for (Joplin's own markings
"Not fast" / "Slow march tempo", his School of Ragtime, and Bill Edwards's notes on
tempo and pedalling in ragtime) is built in as explicit rules:

  time      a steady march pulse - no rubato inside the strain.  Only: a hair of
            broadening at each strain's cadence, a breath between strains (a longer one
            before the trio), a shade more motion in B and D, a shade less in the trio,
            a ritardando over the last two bars.  Sixteenths are straight, not swung.
  touch     left hand: the bass octave is held for its eighth, the after-beat chord is
            short and lighter; right hand: single lines are bound, octaves and chords are
            detached; the tied (syncopated) notes carry the accent - "the rag".
  balance   tune on top; bass octaves firm (the march), after-beat chords well under.
  pedal     "dab" pedalling in the march strains: down just after the bass octave, up
            just before the chord, so the bass rings and the chord stays crisp; none in
            octave runs; in the trio the foot stays down through the chord and changes
            on every beat (legato); held through the final chord.
  repeats   each pass of a strain has its own level (see PLAN in the piece).
"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "engine"))
from midi_out import PerformanceOutput


class RagPerformance(PerformanceOutput):
    def __init__(self, sc, plan, seed=1899):
        self.sc, self.plan = sc, plan
        self.rng = np.random.default_rng(seed)
        self.notes = sc.all_notes()
        self._time_map()

    def S(self, bar, pos=0.0):
        return self.sc.s(bar, pos)

    # ------------------------------------------------------------------ time
    def _time_map(self):
        sc, plan = self.sc, self.plan
        nb = len(sc.bars)
        ds = 0.125
        grid = np.arange(0, sc.length + ds, ds)
        fac = np.ones_like(grid)
        # a human pulse is not a metronome: a slow drift of about half a percent
        drift = np.cumsum(self.rng.normal(0, 0.0016, nb))
        drift -= np.linspace(0, drift[-1], nb)
        for i, (name, k, p) in enumerate(sc.tags):
            sec = plan["sections"][(name, p)]
            m = (grid >= i * 8) & (grid < (i + 1) * 8)
            fac[m] = sec["tempo"] * (1 + drift[i])
            last = sum(1 for t in sc.tags if t[0] == name and t[2] == p)
            if k == last and name != "Intro":                     # the cadence bar sits back a little
                fac[m & (grid >= i * 8 + 4)] *= 0.972
            if name == "Intro" and k == last:
                fac[m & (grid >= i * 8 + 4)] *= 0.94
        rit = plan["final_rit"]                                    # last four beats of the piece
        for j, f in enumerate(rit):
            s0 = sc.length - 4 * (len(rit) - j)
            fac[(grid >= s0) & (grid < s0 + 4)] *= f
        self.bpm_grid = plan["bpm"] * fac
        spu = 15.0 / self.bpm_grid                                 # seconds per sixteenth
        self.grid = grid
        self.tgrid = np.concatenate([[0.0], np.cumsum(spu[:-1] * ds)])
        self.breaths = []
        for i, (name, k, p) in enumerate(sc.tags):
            if k == 1 and i > 0:
                b = plan["breath_before_trio"] if (name == "C" and p == 1) else plan["breath_between_strains"]
                self.breaths.append((i * 8.0, b))

    def t(self, s):
        base = float(np.interp(s, self.grid, self.tgrid))
        return base + sum(b for sb, b in self.breaths if sb <= s + 1e-9) + 1.0

    def level(self, bar):
        name, k, p = self.sc.tags[bar - 1]
        sec = self.plan["sections"][(name, p)]
        shape = self.plan["strain_shape"][k - 1] if name != "Intro" else [0.0, 0.02, 0.05, 0.06][k - 1]
        return sec["level"] + shape

    # ------------------------------------------------------------------ performance
    def perform(self):
        sc, plan, rng = self.sc, self.plan, self.rng
        notes = self.notes
        nbars = len(sc.bars)
        ev = []
        by_tok = {}
        for n in notes:
            by_tok.setdefault((n.hand, round(n.s, 4)), []).append(n)
        rh_on = sorted({round(n.s, 4) for n in notes if n.hand == "R"})
        lh_on = sorted({round(n.s, 4) for n in notes if n.hand == "L"})

        def nxt_onset(arr, s):
            i = np.searchsorted(arr, round(s, 4) + 1e-6)
            return arr[i] if i < len(arr) else None

        hand_off = {}

        def offset(hand, s):
            k = (hand, round(s, 4))
            if k not in hand_off:
                hand_off[k] = float(np.clip(rng.normal(-0.002 if hand == "R" else 0.0, 0.006), -0.016, 0.016))
            return hand_off[k]

        for n in notes:
            name, kbar, p = sc.tags[n.bar - 1]
            sec = plan["sections"][(name, p)]
            legato_strain = sec["pedal"] == "legato"
            L = self.level(n.bar)
            vbase = 40.0 + 62.0 * L
            t0 = self.t(n.s); t1 = self.t(n.s + n.dur)
            tok = by_tok[(n.hand, round(n.s, 4))]
            final_bar = n.bar == nbars
            on = t0 + offset(n.hand, n.s) + rng.normal(0, 0.0035)
            pos = n.pos
            off_beat_long = (abs(pos % 2 - 1) < 1e-6 and n.dur >= 2)            # the tied / "short-LONG-short" note

            if n.hand == "R":
                nx = nxt_onset(rh_on, n.s)
                rest_follows = nx is None or nx > n.s + n.dur + 1e-6
                single = len(tok) == 1
                nxt_tok = by_tok.get(("R", nx)) if nx is not None else None
                step_next = (single and nxt_tok is not None and len(nxt_tok) == 1
                             and abs(nxt_tok[0].pitch - n.pitch) <= 4)
                if n.role == "melody":
                    v = vbase
                    if off_beat_long: v += 6.0                                   # the syncopation is the accent
                    elif abs(pos) < 1e-6: v += 2.0
                    elif abs(pos - 4) < 1e-6: v += 1.0
                    elif n.dur <= 1: v -= 3.0
                    if n.dur >= 4: v += 2.0
                    v += float(np.clip(0.18 * (n.pitch - 77), -3, 4))
                else:
                    octave_low = any(m.pitch - n.pitch == 12 and m.role == "melody" for m in tok)
                    v = vbase - (7.0 if octave_low else 10.0) + (3.0 if off_beat_long else 0.0)
                    on -= 0.004 * (n.chord_size - 1 - n.chord_rank)              # the hand lands thumb first by a hair
                # articulation
                d = t1 - t0
                if final_bar and n.dur >= 4:
                    off = t1 + plan["final_hold"]
                elif rest_follows:
                    off = t0 + d * (0.72 if n.dur >= 4 else 0.62)
                elif step_next and nxt_tok[0].pitch == n.pitch:
                    off = self.t(nx) - 0.035                                     # a repeated note needs the key back
                elif step_next:
                    off = self.t(nx) + (0.02 if legato_strain else 0.006)        # bound line
                elif single:
                    off = t0 + d * (0.95 if legato_strain else 0.88)
                else:
                    off = t0 + d * (0.90 if legato_strain else 0.80)             # octaves and chords are detached
            else:
                nx = nxt_onset(lh_on, n.s)
                d = t1 - t0
                unison = name == "Intro" and len(tok) == 1 and n.dur <= 2
                if unison:
                    v = vbase - 6.0 + (4.0 if off_beat_long else 0.0)
                    off = t0 + d * 0.86
                elif n.role == "bass":
                    v = vbase - 9.0 + (2.0 if abs(pos) < 1e-6 else 0.0)
                    if n.chord_rank > 0:
                        v -= 5.0; on += 0.003                                    # upper note of the octave is the lighter one
                    off = t0 + d * (0.92 if (legato_strain or n.dur >= 4) else 0.86)
                else:
                    v = vbase - 19.0 - (1.0 if pos > 4 else 0.0) + (1.0 if n.chord_rank == n.chord_size - 1 else 0.0)
                    off = t0 + d * (0.72 if legato_strain else (0.86 if n.dur >= 4 else 0.52))
                    on -= 0.003 * (n.chord_size - 1 - n.chord_rank)
                if final_bar and n.dur >= 4:
                    off = t1 + plan["final_hold"]; v += 3.0
            if final_bar:
                v += 3.0
            v += rng.normal(0, 1.8)
            ev.append(dict(on=on, off=max(off, on + 0.05), pitch=n.pitch, vel=int(np.clip(round(v), 24, 114)),
                           role=n.role, bar=n.bar, pos=n.pos, s=n.s, hand=n.hand, name=n.name, dur=n.dur))
        ev.sort(key=lambda e: e["on"])
        self.events = ev
        self.sustain = self._pedal(by_tok, lh_on)
        self.soft = ([0.0], [0.0])
        return ev

    # ------------------------------------------------------------------ pedal
    def _pedal(self, by_tok, lh_on):
        sc, plan = self.sc, self.plan
        pts = [(0.0, 0.0)]
        nbars = len(sc.bars)
        t_end = max(e["off"] for e in self.events)

        def press(t_dn, t_up, depth):
            if t_up - t_dn < 0.05:
                return
            pts.extend([(t_dn, 0.0), (t_dn + 0.03, depth), (t_up - 0.03, depth), (t_up, 0.0)])

        for i, s in enumerate(lh_on):
            tok = by_tok[("L", s)]
            n = tok[0]
            if n.role != "bass":
                continue
            name, kbar, p = sc.tags[n.bar - 1]
            style = plan["sections"][(name, p)]["pedal"]
            nxt = lh_on[i + 1] if i + 1 < len(lh_on) else None
            nxt_tok = by_tok[("L", nxt)] if nxt is not None else None
            nxt_is_chord = nxt_tok is not None and nxt_tok[0].role == "acc"
            t_b = self.t(s)
            if n.bar == nbars and n.dur >= 4:                       # the last chord: foot down and stay
                pts.extend([(t_b + 0.04, 0.0), (t_b + 0.09, 0.85), (t_end + 0.2, 0.85), (t_end + 1.4, 0.0)])
                continue
            if style == "none" or nxt is None:
                continue
            if not nxt_is_chord and n.dur < 4:
                continue                                            # octave runs stay dry
            if style == "dab":
                # down just after the bass, up just before the chord
                t_up = self.t(nxt) - 0.018 if n.dur < 4 else self.t(s + n.dur) - 0.03
                press(t_b + 0.035, t_up, 0.74)
            else:                                                   # legato: through the chord, change on the beat
                beat_end = s - (s % 4) + 4
                press(t_b + 0.04, self.t(beat_end) - 0.035, 0.80)
        pts.sort()
        return ([q[0] for q in pts], [q[1] for q in pts])

    # ------------------------------------------------------------------ report
    def summary(self):
        ev = self.events
        v = np.array([e["vel"] for e in ev])
        role = lambda r: np.array([e["vel"] for e in ev if e["role"] == r])
        tb = np.array([self.t(i * 8.0) for i in range(len(self.sc.bars) + 1)])
        bpm = 120.0 / np.diff(tb)
        tt, pv = np.array(self.sustain[0]), np.array(self.sustain[1])
        g = np.arange(0, tt[-1], 0.005); down = np.interp(g, tt, pv) > 0.4
        return dict(seconds=float(max(e["off"] for e in ev)), key_strokes=len(ev),
                    bpm_median=float(np.median(bpm)), bpm_p05=float(np.percentile(bpm, 5)), bpm_p95=float(np.percentile(bpm, 95)),
                    vel_p05=float(np.percentile(v, 5)), vel_p50=float(np.percentile(v, 50)), vel_p95=float(np.percentile(v, 95)),
                    melody=float(np.median(role("melody"))), bass=float(np.median(role("bass"))), chords=float(np.median(role("acc"))),
                    pedal_share_down=float(down.mean()))
