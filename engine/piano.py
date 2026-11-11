"""A sample-based concert grand, written for this project.

It plays the Salamander Grand Piano (Yamaha C5, 16 velocity layers, 48 kHz / 24 bit,
CC-BY Alexander Holm) and adds the things a plain SFZ player leaves out and that
matter most in a nocturne:

  * a continuous damper model - the sustain pedal is a depth (0..1), not a switch, so
    half-pedalling and quick "syncopated" changes that let the bass keep ringing work
    the way they do on a real instrument;
  * register-dependent damping speed, undamped top octaves;
  * release-triggered string resonance and key noise from the sample set;
  * sympathetic resonance of the open strings while the pedal is down (convolution
    with a "string cloud" built from the instrument's own samples);
  * una corda;
  * same-string re-strike handling.

Usage as a module:  Piano(sfz).render(notes, sustain, soft)  ->  float32 stereo
"""
import os
import re
import numpy as np
import soundfile as sf
import soxr
from scipy.signal import fftconvolve

SR = 48000
CTRL = 500  # control rate (Hz) for pedal / damper envelopes


def _num(v):
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v


def parse_sfz(path):
    text = re.sub(r"//.*", "", open(path, encoding="utf8", errors="ignore").read())
    regions, group = [], {}
    for m in re.finditer(r"<(\w+)>([^<]*)", text):
        hdr, body = m.group(1), m.group(2)
        ops = {k: _num(v) for k, v in re.findall(r"(\w+)=(\S+)", body)}
        if hdr == "group":
            group = ops
        elif hdr == "region":
            r = dict(group)
            r.update(ops)
            regions.append(r)
    return regions


class Piano:
    def __init__(self, sfz_path, sr=SR, veltrack_scale=1.0, verbose=False, regulate=True):
        self.sr = sr
        self.dir = os.path.dirname(sfz_path)
        self.verbose = verbose
        self.veltrack_scale = veltrack_scale
        regs = parse_sfz(sfz_path)
        self.attack = {}      # key -> [(lovel, hivel, region)]
        self.release = {}     # key -> [region]   (string resonance + key noise)
        self.pedal_noise = {"down": [], "up": []}
        for r in regs:
            if r.get("lokey", 0) == -1:
                (self.pedal_noise["down"] if "on_locc64" in r and r["on_locc64"] > 64 else self.pedal_noise["up"]).append(r)
                continue
            lo, hi = r.get("lokey", r.get("key", 0)), r.get("hikey", r.get("key", 127))
            for k in range(lo, hi + 1):
                if r.get("trigger") == "release":
                    self.release.setdefault(k, []).append(r)
                else:
                    self.attack.setdefault(k, []).append((r.get("lovel", 1), r.get("hivel", 127), r))
        self._raw, self._shifted = {}, {}
        self.voicing = self._regulate() if regulate else {}

    def _regulate(self, limit_db=5.0):
        """Voicing regulation, the job a technician does on a real instrument.

        The sample set is not even: e.g. the C6 samples are 3-5 dB weaker than their
        neighbours in the middle layers and D#6 is 4-5 dB stronger - right where a
        nocturne melody lives.  For every velocity layer the level of each sampled key is
        compared with the running median of its neighbours (+-6 semitones) and the
        deviation (not the natural bass-to-treble trend) is taken out."""
        import json
        cache = os.path.join(self.dir, "voicing_regulation.json")
        if os.path.exists(cache):
            return json.load(open(cache))
        keys = sorted(k for k in self.attack if self.attack[k][0][2].get("pitch_keycenter", 60) == k)
        nl = max(len(self.attack[k]) for k in keys)
        L = np.full((len(keys), nl), np.nan)
        for i, k in enumerate(keys):
            for j, (lo, hi, reg) in enumerate(self.attack[k]):
                x = self._load(reg["sample"])[: int(1.5 * self.sr)].astype(np.float64)
                L[i, j] = 10 * np.log10((x ** 2).mean() + 1e-20)
        table = {}
        for j in range(nl):
            col = L[:, j]
            for i, k in enumerate(keys):
                sm = np.nanmedian(col[max(0, i - 2): i + 3])
                dev = float(np.clip(col[i] - sm, -limit_db, limit_db))
                table[self.attack[k][j][2]["sample"]] = round(-dev, 2)     # gain to apply, dB
        self._raw.clear()
        json.dump(table, open(cache, "w"), indent=0)
        return table

    # ------------------------------------------------------------------ samples
    def _load(self, name):
        x = self._raw.get(name)
        if x is None:
            x, sr = sf.read(os.path.join(self.dir, name), dtype="float32", always_2d=True)
            if x.shape[1] == 1:
                x = np.repeat(x, 2, axis=1)
            if sr != self.sr:
                x = soxr.resample(x, sr, self.sr, quality="VHQ")
            self._raw[name] = x
        return x

    def _pitched(self, region, key):
        """Sample of `region` transposed to `key` (cached)."""
        ck = (region["sample"], key)
        y = self._shifted.get(ck)
        if y is None:
            x = self._load(region["sample"])
            cents = region.get("tune", 0)
            if region.get("pitch_keytrack", 100) != 0:
                cents += 100 * (key - region.get("pitch_keycenter", 60))   # SFZ default centre is C4
            if cents:
                ratio = 2.0 ** (cents / 1200.0)
                y = soxr.resample(x, self.sr * ratio, self.sr, quality="VHQ").astype(np.float32)
            else:
                y = x
            self._shifted[ck] = y
        return y

    def _velgain(self, region, vel):
        t = region.get("amp_veltrack", 100) / 100.0 * self.veltrack_scale
        v = (vel / 127.0) ** 2
        return (1.0 - t * (1.0 - v)) * 10 ** (region.get("volume", 0) / 20.0)

    @staticmethod
    def damp_rate(key):
        """Damper efficiency (nepers/s when fully engaged). Bass strings are heavy and
        take longer to stop; the top 1.5 octaves have no dampers at all."""
        if key >= 89:
            return 0.0
        t60 = np.interp(key, [21, 36, 60, 76, 88], [0.60, 0.40, 0.22, 0.16, 0.13])
        return 6.91 / t60

    # ------------------------------------------------------------------ render
    def render(self, notes, sustain=None, soft=None, tail=7.0, release_level=1.0,
               pedal_noise_db=-30.0, seed=7):
        """notes: iterable of (onset_s, offset_s, midi_key, velocity 1..127)
        sustain / soft: (times, values in 0..1) step functions (MIDI CC64 / CC67)."""
        sr = self.sr
        rng = np.random.default_rng(seed)
        notes = sorted(notes, key=lambda n: n[0])
        end = max(n[1] for n in notes) + tail
        N = int(end * sr) + 1
        out = np.zeros((N, 2), dtype=np.float32)
        grid = np.arange(0, int(end * CTRL) + 2) / CTRL

        def step(curve):
            if curve is None or len(curve[0]) == 0:
                return np.zeros_like(grid)
            t, v = np.asarray(curve[0], float), np.asarray(curve[1], float)
            idx = np.searchsorted(t, grid, side="right") - 1
            return np.where(idx >= 0, v[np.clip(idx, 0, len(v) - 1)], 0.0)

        P = step(sustain)
        S = step(soft)
        # a real pedal mechanism has inertia: smooth by ~12 ms
        k = np.hanning(13); k /= k.sum()
        P = np.convolve(P, k, mode="same")
        # damper engagement 0 (free) .. 1 (fully on the string)
        D = np.clip((0.58 - P) / (0.58 - 0.30), 0.0, 1.0)
        C = np.concatenate([[0.0], np.cumsum(D) / CTRL])      # C[i] = integral of D up to grid[i]
        self.P, self.grid = P, grid

        # next onset of the same key (the hammer re-strikes the same strings)
        nxt, last = {}, {}
        for i in range(len(notes) - 1, -1, -1):
            kkey = notes[i][2]
            nxt[i] = last.get(kkey)
            last[kkey] = notes[i][0]

        for i, (on, off, key, vel) in enumerate(notes):
            if key not in self.attack:
                continue
            soft_on = S[min(len(S) - 1, int(on * CTRL))] > 0.5
            v_eff = vel * 0.90 if soft_on else vel        # una corda: softer, rounder
            v_eff = float(np.clip(v_eff, 1, 127))
            vi = int(round(v_eff))
            reg = next((r for lo, hi, r in self.attack[key] if lo <= vi <= hi), self.attack[key][-1][2])
            x = self._pitched(reg, key)
            g = self._velgain(reg, v_eff) * (0.93 if soft_on else 1.0)
            g *= 10 ** (self.voicing.get(reg["sample"], 0.0) / 20.0)

            R = self.damp_rate(key)
            i_on = int(on * CTRL)
            i_off = min(len(grid) - 1, max(i_on + 1, int(np.ceil(off * CTRL))))
            n_ctrl = min(len(grid) - i_on, int(len(x) / sr * CTRL) + 2)
            idx = np.arange(i_on, i_on + n_ctrl)
            cum = R * np.maximum(0.0, C[idx] - C[i_off])
            if nxt[i] is not None:                           # re-strike kills the old vibration
                cum += np.maximum(0.0, grid[idx] - nxt[i]) / 0.035
            env = np.exp(-cum)
            dead = np.nonzero(env < 2e-4)[0]
            n_ctrl_eff = dead[0] + 1 if len(dead) else n_ctrl
            n_audio = min(len(x), int(n_ctrl_eff / CTRL * sr), N - int(on * sr))
            if n_audio <= 0:
                continue
            s0 = int(round(on * sr))
            seg = x[:n_audio] * g
            if cum[min(n_ctrl_eff, n_ctrl) - 1] > 1e-6:
                ta = (np.arange(n_audio) / sr) + (s0 / sr - grid[i_on])
                e = np.interp(ta, grid[idx[:n_ctrl_eff]] - grid[i_on], env[:n_ctrl_eff]).astype(np.float32)
                seg = seg * e[:, None]
            out[s0:s0 + n_audio] += seg

            # release-triggered layers: fire when the damper really lands on the string
            if release_level > 0 and R > 0:
                j = np.nonzero(D[i_off:i_off + int(4 * CTRL)] > 0.6)[0]
                if len(j):
                    t_d = grid[i_off + j[0]]
                    if nxt[i] is None or t_d < nxt[i]:
                        age = t_d - on
                        for rr in self.release.get(key, []):
                            if not (rr.get("lovel", 1) <= vel <= rr.get("hivel", 127)):
                                continue
                            gg = self._velgain(rr, vel) * 10 ** (-rr.get("rt_decay", 0) * age / 20.0) * release_level
                            if gg < 1e-4:
                                continue
                            y = self._pitched(rr, key)
                            s1 = int(t_d * sr)
                            m = min(len(y), N - s1)
                            if m > 0:
                                out[s1:s1 + m] += y[:m] * gg

        # pedal mechanism noise (very quiet; it is part of the acoustic picture of a recording)
        if pedal_noise_db is not None and sustain is not None and self.pedal_noise["down"]:
            gpn = 10 ** (pedal_noise_db / 20.0)
            down = np.nonzero((P[:-1] < 0.5) & (P[1:] >= 0.5))[0]
            up = np.nonzero((P[:-1] >= 0.5) & (P[1:] < 0.5))[0]
            for idxs, bank in ((down, self.pedal_noise["down"]), (up, self.pedal_noise["up"])):
                for ii in idxs:
                    y = self._load(bank[rng.integers(len(bank))]["sample"])
                    s1 = int(grid[ii] * sr); m = min(len(y), N - s1)
                    if m > 0:
                        out[s1:s1 + m] += y[:m] * gpn * rng.uniform(0.6, 1.0)
        return out

    # ------------------------------------------------------- sympathetic resonance
    def string_cloud(self, seconds=5.0, layer=5, lo=24, hi=88):
        """Impulse response of 'all dampers raised': the summed free response of every
        string (attack removed), used to convolve the dry signal while the pedal is down."""
        n = int(seconds * self.sr)
        ir = np.zeros((n, 2), dtype=np.float64)
        fade = int(0.12 * self.sr)
        w_in = np.sin(np.linspace(0, np.pi / 2, fade)) ** 2
        for key in range(lo, hi + 1):
            regs = self.attack.get(key)
            if not regs:
                continue
            reg = regs[min(layer, len(regs) - 1)][2]
            x = self._pitched(reg, key)[:n].astype(np.float64)
            x = x.copy()
            x[:fade] *= w_in[:len(x[:fade]), None]
            e = np.sqrt((x ** 2).sum()) + 1e-12
            ir[:len(x)] += x / e
        ir *= np.exp(-np.arange(n) / (1.6 * self.sr))[:, None]
        ir /= np.sqrt((ir ** 2).sum())
        return ir.astype(np.float32)

    def add_resonance(self, dry, level_db=-27.0):
        """Feed the dry signal into the open strings whenever the pedal is down."""
        P, grid = self.P, self.grid
        t = np.arange(len(dry)) / self.sr
        gate = np.interp(t, grid, np.clip((P - 0.45) / 0.25, 0, 1)).astype(np.float32)
        ir = self.string_cloud()
        wet = fftconvolve(dry * gate[:, None], ir, mode="full", axes=0)[:len(dry)]
        # when the dampers come down the halo is cut off as well
        k = int(0.06 * self.sr)
        gs = np.convolve(gate, np.ones(k) / k, mode="same").astype(np.float32)
        wet *= gs[:, None]
        ref = np.sqrt(np.mean(dry ** 2)) + 1e-12
        wr = np.sqrt(np.mean(wet ** 2)) + 1e-12
        return dry + wet * (ref / wr) * 10 ** (level_db / 20.0)


# ----------------------------------------------------------------------- MIDI in
def midi_to_events(path):
    """Read a performance MIDI file -> notes, sustain curve, soft curve."""
    import pretty_midi
    pm = pretty_midi.PrettyMIDI(path)
    notes, cc64, cc67 = [], [], []
    for inst in pm.instruments:
        notes += [(n.start, n.end, n.pitch, n.velocity) for n in inst.notes]
        cc64 += [(c.time, c.value / 127.0) for c in inst.control_changes if c.number == 64]
        cc67 += [(c.time, c.value / 127.0) for c in inst.control_changes if c.number == 67]
    cc64.sort(); cc67.sort()
    sus = ([c[0] for c in cc64], [c[1] for c in cc64])
    sft = ([c[0] for c in cc67], [c[1] for c in cc67])
    return notes, sus, sft
