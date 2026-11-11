"""The pianist.

Turns the score plus the performer's plan (nocturne_bm.TEMPO / DYNAMICS / ...) into a
performance: for every note an onset, a release and a key velocity; for the feet a
continuous sustain-pedal curve and the una corda.

The model is deliberately explicit - each rule corresponds to something pianists do and
that the MAESTRO / ASAP measurements in ../../research confirm:

  timing    authored tempo curve x phrase breathing x within-bar lilt, plus "taken" time
            (breaths, placements, fermatas); fioriture are free inside their time span
            (lingering start, flowing middle, broadening end); trills accelerate;
            grace notes on the beat with the bass
  hands     melody and bass are not struck together to the millisecond: small random
            asynchrony as measured (median ~0, IQR about +-18 ms), bass-before-melody
            only at a few structural downbeats; wide chords are rolled
  tone      melody sings above everything (about +20 velocity over the bass at mezzo
            piano), long notes get more weight than passing ones, resolutions are
            softer than their dissonances, the left-hand wave swells and subsides
  pedal     syncopated legato pedalling: the foot comes up just after the new bass is
            struck and is back down ~0.15 s later, so the bass (still held by the
            finger) is caught and the old harmony is cleared
"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "engine"))
from midi_out import PerformanceOutput


class Performance(PerformanceOutput):
    def __init__(self, sc, plan, seed=1810, opts=None):
        self.sc, self.plan = sc, plan
        self.rng = np.random.default_rng(seed)
        self.o = dict(
            lilt=1.0,              # strength of the within-bar tempo profile
            phrase_arch=1.0,       # strength of phrase-level breathing
            async_sd=0.028,        # s.d. of melody-vs-accompaniment asynchrony (s)
            jitter_sd=0.008,       # motor noise on every onset (s)
            vel_noise=1.6,
            mel_base=36.0, mel_span=66.0,
            bass_gap=23.0, acc_gap=20.0, duet_gap=9.0,
            tempo_scale=1.0,
            pedal_up=0.085, pedal_lift_delay=0.03,
        )
        if opts:
            self.o.update(opts)
        self.notes = sc.all_notes()
        self._build_time_map()

    # ------------------------------------------------------------------ helpers
    def S(self, bar, pos=0.0):
        return self.sc.s(bar, pos)

    def _curve(self, pts):
        s = np.array([self.S(b, p) for b, p, _ in pts]); v = np.array([x for _, _, x in pts], float)
        return s, v

    def level(self, s):
        return float(np.interp(s, *self._dyn))

    # ------------------------------------------------------------------ time
    def _build_time_map(self):
        sc, plan, o = self.sc, self.plan, self.o
        ds = 1.0 / 32
        grid = np.arange(0, sc.length + ds, ds)
        ts, tv = self._curve(plan.TEMPO)
        bpm = np.interp(grid, ts, tv) * o["tempo_scale"]
        # phrase breathing: ease in, move forward, broaden at the end
        mult = np.ones_like(grid)
        for (b0, p0), (b1, p1) in plan.PHRASES:
            s0, s1 = self.S(b0, p0), self.S(b1, p1)
            m = (grid >= s0) & (grid < s1)
            x = (grid[m] - s0) / (s1 - s0)
            mult[m] *= 1 + o["phrase_arch"] * (0.030 * np.sin(np.pi * x) - 0.022 * (1 - x) ** 6 - 0.045 * x ** 7)
        # within-bar lilt measured on ASAP (Barcarolle): beat 1 a shade broad, 2-3 flowing, 4 yielding
        prof_x = np.array([0, 1.5, 4.5, 7.5, 10.5, 12.0])
        prof_y = np.array([0.975, 0.985, 1.03, 1.025, 0.955, 0.975])
        pos = grid % sc.bar_len
        mult *= 1 + o["lilt"] * (np.interp(pos, prof_x, prof_y) - 1)
        # dense fioriture are given room
        for n in self.notes:
            if n.group and n.group[1] == 0 and n.group[2] >= 7:
                gid, k, cnt, s0, D = n.group
                dens = cnt / D
                f = float(np.clip(1 - 0.055 * (dens - 1.6), 0.80, 1.0))
                m = (grid >= s0) & (grid < s0 + D)
                mult[m] *= f
        self.bpm_grid = bpm * mult
        spe = 20.0 / self.bpm_grid                 # seconds per eighth (dotted quarter = 3 eighths)
        t = np.concatenate([[0.0], np.cumsum(spe[:-1] * ds)])
        self.grid, self.tgrid = grid, t
        self.breaths = sorted((self.S(b, p), sec) for b, p, sec in plan.BREATHS)
        self._dyn = self._curve(plan.DYNAMICS)
        self.auto_breaths = self._placements()

    def _placements(self):
        """A little time before melodic arrivals: wide upward leaps onto long notes."""
        out = []
        mel = [n for n in self.notes if n.role == "melody" and n.voice == "rh" and n.grace is None]
        for a, b in zip(mel, mel[1:]):
            if b.group is not None or b.dur < 2.5:
                continue
            leap = b.pitch - a.pitch
            on_beat = abs(b.pos % 3) < 1e-6
            if on_beat and leap >= 5:
                out.append((b.s, min(0.07, 0.012 * leap)))
            elif on_beat and abs(b.pos % 6) < 1e-6 and leap in (-2, -1) and a.dur <= 1:
                out.append((b.s, 0.018))            # appoggiatura on a strong beat: lean into it
        return out

    def t(self, s):
        """score position (eighths) -> seconds"""
        base = float(np.interp(s, self.grid, self.tgrid))
        extra = sum(sec for sb, sec in self.breaths if sb <= s + 1e-9)
        extra += sum(sec for sb, sec in self.auto_breaths if sb <= s + 1e-9)
        return base + extra + 1.0                  # one second of silence before the first note

    # ------------------------------------------------------------------ performance
    def perform(self):
        sc, plan, o, rng = self.sc, self.plan, self.o, self.rng
        notes = self.notes
        events = []                                 # dicts: on, off, pitch, vel, role, bar, pos

        bass_first = {self.S(b, p): ms / 1000.0 for b, p, ms in plan.BASS_FIRST}
        rolls = {self.S(b, p): ms / 1000.0 for (b, p), ms in plan.ROLLS.items()}

        # ---- per-voice neighbours (for legato and for the "sigh" rule)
        mel = [n for n in notes if n.role == "melody" and n.voice == "rh"]
        mel.sort(key=lambda n: (n.s, n.grace[0] if n.grace else 99, n.pitch))
        phrase_med = {}
        for (b0, p0), (b1, p1) in plan.PHRASES:
            ps = [n.pitch for n in mel if self.S(b0, p0) <= n.s < self.S(b1, p1)]
            phrase_med[(self.S(b0, p0), self.S(b1, p1))] = float(np.median(ps)) if ps else 76.0

        def med_pitch(s):
            for (s0, s1), v in phrase_med.items():
                if s0 <= s < s1:
                    return v
            return 76.0

        # one asynchrony draw per (score time, hand): notes of a chord move together
        async_cache = {}

        def hand_shift(n):
            key = (round(n.s, 5), n.hand)
            if key not in async_cache:
                if n.hand == "R":
                    d = rng.normal(-0.003, o["async_sd"])
                    d = float(np.clip(d, -0.058, 0.058))
                    d += bass_first.get(round(n.s, 5), bass_first.get(n.s, 0.0))
                else:
                    d = 0.0
                async_cache[key] = d
            return async_cache[key]

        def vel_melody(n, L, prev):
            v = o["mel_base"] + o["mel_span"] * L
            d_eff = n.dur if n.group is None and n.grace is None else (0.3 if n.grace else n.group[4] / n.group[2])
            v += float(np.clip(5.5 * math.log2(max(d_eff, 0.25) / 1.5), -9, 7))
            v += float(np.clip(0.25 * (n.pitch - med_pitch(n.s)), -5, 5))
            pos = n.pos
            v += 1.5 if abs(pos % 6) < 1e-6 else (0.5 if abs(pos % 3) < 1e-6 else -1.0)
            if prev is not None and n.group is None and n.grace is None and prev.grace is None:
                step = prev.pitch - n.pitch
                if 1 <= step <= 2 and prev.dur >= n.dur and abs(prev.pos % 3) < 1e-6 and prev.group is None:
                    v -= 5.0                        # resolution of a leaning note: softer
                if n.pitch == prev.pitch and prev.dur <= 1.0:
                    v += 1.5                        # the note an anticipation points to
                if n.pitch == prev.pitch and n.dur <= 1.0:
                    v -= 4.0                        # the anticipation itself is whispered
            if "!" in n.flags: v += 8
            if "_" in n.flags: v += 4
            if "'" in n.flags: v -= 6
            return v

        self._mel_line = [n for n in mel if n.grace is None and n.group is None]
        self._mel_index = {id(n): i for i, n in enumerate(self._mel_line)}
        prev_mel = None
        for n in notes:
            L = self.level(n.s)
            t0 = self.t(n.s)
            t1 = self.t(n.s + max(n.dur, 0.0))
            shift = hand_shift(n)
            jit = rng.normal(0, o["jitter_sd"])
            vmel0 = o["mel_base"] + o["mel_span"] * L
            ev = dict(pitch=n.pitch, role=n.role, bar=n.bar, pos=n.pos, s=n.s, hand=n.hand, name=n.name,
                      group=n.group[0] if n.group else None, grace=n.grace is not None, dur=n.dur)

            # ------------------------------------------------ right hand
            if n.role == "melody":
                if n.grace is not None:
                    k, cnt = n.grace
                    g = 0.075 if cnt == 1 else 0.065
                    on = t0 + shift + k * g
                    off = on + g + 0.03
                    v = vel_melody(n, L, prev_mel) - 6
                elif n.group is not None:
                    gid, k, cnt, gs0, D = n.group
                    ta, tb = self.t(gs0), self.t(gs0 + D)
                    if cnt >= 5:
                        u = (np.arange(cnt) + 0.5) / cnt
                        # free time inside the group: linger, flow, broaden; a cadenza takes more liberty
                        if cnt >= 20 and D >= 9:
                            speed = 1 - 0.56 * np.exp(-u / 0.13) - 0.66 * np.exp(-(1 - u) / 0.17)
                        else:
                            speed = 1 - 0.40 * np.exp(-u / 0.10) - 0.46 * np.exp(-(1 - u) / 0.13)
                        w = 1 / speed
                        cum = np.concatenate([[0], np.cumsum(w)]) / w.sum()
                    else:
                        cum = np.arange(cnt + 1) / cnt
                    on = ta + (tb - ta) * cum[k] + (shift if k == 0 else 0) + rng.normal(0, 0.003)
                    off = ta + (tb - ta) * cum[k + 1] + 0.02
                    uu = (k + 0.5) / cnt
                    v = vel_melody(n, L, None) - 8 + 6.5 * math.sin(math.pi * uu) ** 1.2
                    if k == 0: v += 4
                    if cnt < 5: v += 4
                else:
                    on = t0 + shift + jit + n.after_grace * 0.07 + self._melodic_rubato(n)
                    if "_" in n.flags:
                        on += 0.014                 # tenuto: the note is placed, not merely struck
                    off = None                      # set by legato pass
                    v = vel_melody(n, L, prev_mel)
                    if n.trill is not None:
                        ev["trill"] = n.trill
                if n.chord_size > 1 and n.s in rolls:
                    on += rolls[n.s] * (self._roll_index(n, notes))
                ev.update(on=on, off=off, vel=v, t_end=t1)
                if n.grace is None:
                    prev_mel = n
            elif n.role in ("duet", "rh_inner"):
                on = t0 + shift + jit + rng.normal(0, 0.004)
                top_gap = o["duet_gap"] if n.role == "duet" else 11.0
                # the lower note of a bare octave is the thumb: firmer than an inner filling
                octave_low = any(m.s == n.s and m.voice == n.voice and m.pitch - n.pitch == 12 and m.role == "melody"
                                 for m in notes if m.bar == n.bar)
                if n.role == "rh_inner" and octave_low:
                    top_gap = 7.0
                v = vmel0 - top_gap + (1.0 if abs(n.pos % 6) < 1e-6 else 0)
                v += float(np.clip(4.0 * math.log2(max(n.dur, 0.5) / 1.5), -5, 4))
                if n.s in rolls:
                    on += rolls[n.s] * self._roll_index(n, notes)
                else:
                    on -= 0.010 * (n.chord_size - 1 - n.chord_rank) * (1 if n.voice == "rh" else 0)
                ev.update(on=on, off=t1 - 0.05, vel=v, t_end=t1)
            # ------------------------------------------------ left hand
            elif n.role == "bass":
                on = t0 + jit
                v = vmel0 - o["bass_gap"] + 0.12 * max(0.0, vmel0 - 72)
                v += 3.0 if abs(n.pos) < 1e-6 else (1.0 if abs(n.pos - 6) < 1e-6 else -2.0)
                if n.chord_size > 1 and n.chord_rank > 0:
                    v -= 4.0
                    on += 0.004
                if n.s in rolls:
                    on += rolls[n.s] * self._roll_index(n, notes)
                ev.update(on=on, off=None, vel=v, t_end=t1)
            else:  # accompaniment figure
                on = t0 + jit
                v = vmel0 - o["acc_gap"] + 0.08 * max(0.0, vmel0 - 72)
                k6 = int(round(n.pos % 6))
                v += [0, -2.0, -0.5, 1.0, 0.0, -2.5][k6 % 6]
                # the lower a figure note lies the more it booms: the thumb side of the wave
                # carries the harmony, the notes near the bass are only touched
                v -= 0.45 * max(0, 52 - n.pitch)
                # the note struck together with a new long melody note steps back
                if any(abs(m.s - n.s) < 1e-6 and m.dur >= 3 for m in mel if m.bar == n.bar and m.grace is None):
                    v -= 2.0
                if n.s in rolls:
                    on += rolls[n.s] * self._roll_index(n, notes)
                ev.update(on=on, off=None, vel=v, t_end=t1)
            ev["vel"] = ev["vel"] + rng.normal(0, o["vel_noise"])
            events.append(ev)

        self._legato(events)
        events = self._expand_trills(events)
        for e in events:
            e["vel"] = int(np.clip(round(e["vel"]), 23, 112))
            e["off"] = max(e["off"], e["on"] + 0.06)
        events.sort(key=lambda e: e["on"])
        self.events = events
        self.sustain = self._pedal(events)
        self.soft = self._una_corda()
        return events

    def _melodic_rubato(self, n):
        """The right hand's own freedom against the left (Chopin's rubato in the narrow sense).

        * an anticipation - the short note that announces the next long one - is sung late,
          close to its goal, like a singer's portamento;
        * three rising upbeat eighths press forward into their arrival (the arrival itself is
          then placed late by the time map), so the line rushes a little and lingers."""
        idx = self._mel_index.get(id(n))
        if idx is None:
            return 0.0
        mel = self._mel_line
        nxt = mel[idx + 1] if idx + 1 < len(mel) else None
        spe = self.t(n.s + 1.0) - self.t(n.s)            # seconds per eighth here
        if nxt is not None and nxt.pitch == n.pitch and n.dur <= 0.5 and nxt.dur >= 2:
            return 0.30 * n.dur * spe
        b = n.pos % 3
        if nxt is not None and n.dur == 1.0 and n.group is None:
            grp = [m for m in mel[max(0, idx - 2): idx + 3] if int(m.s // 3) == int(n.s // 3) and m.dur == 1.0]
            if len(grp) == 3 and grp[0].pitch < grp[1].pitch < grp[2].pitch:
                k = grp.index(n)
                return -0.035 * spe * k                  # 0, -14 ms, -28 ms at eighth = 0.4 s
        return 0.0

    def _roll_index(self, n, notes):
        """rank of a note inside a rolled chord, bottom to top across both hands"""
        chord = sorted({m.pitch for m in notes if abs(m.s - n.s) < 1e-6 and m.grace is None and m.group is None})
        return chord.index(n.pitch)

    # ------------------------------------------------------------------ note lengths
    def _legato(self, events):
        rng = self.rng
        # melody: bind each note to the next one in the line
        mel = sorted((e for e in events if e["role"] == "melody" and e["off"] is None), key=lambda e: e["on"])
        allmel = sorted((e for e in events if e["role"] == "melody"), key=lambda e: e["on"])
        for e in mel:
            nxt = next((m for m in allmel if m["on"] > e["on"] + 1e-4), None)
            natural = e["t_end"]
            if nxt is None or nxt["on"] > natural + 0.25:          # a rest follows: lift, let the pedal carry it
                e["off"] = natural - 0.04
            elif nxt["pitch"] == e["pitch"]:
                e["off"] = nxt["on"] - 0.055                       # repeated note needs the key back
            else:
                # pianists lift a little before the next key goes down and let the pedal join
                # the tones (MAESTRO: median gap ~50 ms); in quick notes the fingers overlap
                ioi = nxt["on"] - e["on"]
                e["off"] = nxt["on"] - min(rng.uniform(0.015, 0.085), 0.25 * ioi) if ioi > 0.22 else nxt["on"] + 0.015
        # left hand: the bass key is kept down through the pedal change; figure notes are finger-legato
        lh = sorted((e for e in events if e["hand"] == "L"), key=lambda e: e["on"])
        for i, e in enumerate(lh):
            if e["off"] is not None:
                continue
            nxt = next((m for m in lh[i + 1:] if m["on"] > e["on"] + 0.03), None)
            if e["dur"] >= 3:
                e["off"] = e["t_end"] - 0.04
            elif nxt is None:
                e["off"] = e["t_end"]
            elif e["role"] == "bass":
                e["off"] = max(nxt["on"] + 0.05, e["on"] + 0.40)
            else:
                e["off"] = max(nxt["on"] + 0.03, e["on"] + 0.10)

    def _expand_trills(self, events):
        out = []
        for e in events:
            if "trill" not in e:
                out.append(e)
                continue
            t0, t1 = e["on"], e["t_end"]
            T = t1 - t0
            # start deliberately, then spin up: ~8 -> 12.5 notes per second
            ts, tcur, k = [], t0, 0
            while True:
                u = (tcur - t0) / T
                rate = 7.5 + 5.0 * min(1.0, u / 0.45)
                ioi = 1.0 / rate
                if tcur + ioi > t1 - 0.02:
                    break
                ts.append(tcur); tcur += ioi; k += 1
            if len(ts) % 2 == 0:                     # finish on the main note
                ts = ts[:-1]
            scale = (T - 0.0) / (ts[-1] - t0 + 1.0 / 12.5) if len(ts) > 1 else 1.0
            ts = [t0 + (x - t0) * min(scale, 1.15) for x in ts]
            for i, x in enumerate(ts):
                u = i / max(1, len(ts) - 1)
                v = e["vel"] - (3 if i == 0 else 14) + 4.0 * math.sin(math.pi * u)
                nxt = ts[i + 1] if i + 1 < len(ts) else t1
                f = dict(e); f.pop("trill")
                f.update(on=x, off=nxt + 0.015, vel=v, pitch=e["pitch"] if i % 2 == 0 else e["trill"], trill_note=True)
                out.append(f)
        return out

    # ------------------------------------------------------------------ feet
    def _pedal(self, events):
        sc, o = self.sc, self.o
        pts = [(0.0, 0.0), (0.45, 0.0), (0.6, 0.8)]   # foot down before the first note
        changes = []
        for b in sc.bars:
            for p in b.pedal:
                s = self.S(b.number, p)
                if s > 0:
                    changes.append(s)
        flutter = getattr(self.plan, "FLUTTER", [])
        for s in sorted(changes):
            tc = self.t(s)
            L = self.level(s)
            up = o["pedal_up"] + (0.03 if L < 0.3 else 0.0)
            a = tc + o["pedal_lift_delay"] + self.rng.uniform(-0.012, 0.02)
            # how deep the foot goes back: pianists rarely floor the pedal (MAESTRO: ~15 % of the
            # time is spent in the partial range), deeper when the playing is loud
            depth = float(np.clip(0.64 + 0.30 * L + self.rng.uniform(-0.05, 0.12), 0.62, 1.0))
            prev = pts[-1][1]
            # coming up takes ~50 ms, going down ~90 ms (a foot is not a switch)
            pts += [(a, prev), (a + 0.025, 0.5 * prev), (a + 0.05, 0.10), (a + 0.05 + up * 0.5, 0.04),
                    (a + 0.05 + up, 0.22), (a + 0.05 + up + 0.04, 0.55), (a + 0.05 + up + 0.09, depth)]
        for (bb, pp, depth) in flutter:               # half-changes: thin the wash, keep the bass
            tc = self.t(self.S(bb, pp))
            pts += [(tc, 0.9), (tc + 0.03, depth), (tc + 0.10, depth), (tc + 0.14, 0.85)]
        t_end = max(e["off"] for e in events)
        pts += [(t_end + 0.4, pts[-1][1]), (t_end + 0.9, 0.6), (t_end + 1.6, 0.3), (t_end + 2.6, 0.0)]
        pts.sort()
        return ([p[0] for p in pts], [p[1] for p in pts])

    def _una_corda(self):
        pts = [(0.0, 0.0)]
        for (b0, p0), (b1, p1) in self.plan.UNA_CORDA:
            pts.append((max(0.0, self.t(self.S(b0, p0)) - 0.25), 1.0))
            pts.append((self.t(self.S(b1, p1)) - 0.30, 0.0))
        pts.sort()
        return ([p[0] for p in pts], [p[1] for p in pts])
