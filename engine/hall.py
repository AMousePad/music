"""Concert-hall acoustics and mastering for the piano render.

The Salamander samples are close-miked (two AKG C414 ~12 cm above the strings), i.e.
drier and wider than anything a listener hears in a recital recording.  This module
puts the instrument on a stage:

  * early reflections from an image-source model of a shoebox hall (stage position,
    spaced-omni main pair a few metres in front of the piano),
  * a diffuse late field with frequency-dependent decay (longer in the bass, air
    absorption in the treble),
  * gentle width control, high-pass, loudness normalisation with true-peak ceiling.

The hall is synthesised rather than sampled so that every parameter is known and
nothing in the chain has licensing strings attached.
"""
import numpy as np
from scipy.signal import fftconvolve, butter, sosfiltfilt, sosfilt

C_SOUND = 343.0


def _band_noise(n, sr, rng, bands, rt60s):
    """Gaussian noise whose decay time differs per frequency band."""
    out = np.zeros(n)
    t = np.arange(n) / sr
    edges = [0] + [np.sqrt(a * b) for a, b in zip(bands[:-1], bands[1:])] + [sr / 2]
    for i, rt in enumerate(rt60s):
        x = rng.standard_normal(n)
        lo, hi = edges[i], edges[i + 1]
        if lo <= 0:
            sos = butter(4, hi / (sr / 2), btype="low", output="sos")
        elif hi >= sr / 2 * 0.999:
            sos = butter(4, lo / (sr / 2), btype="high", output="sos")
        else:
            sos = butter(4, [lo / (sr / 2), hi / (sr / 2)], btype="band", output="sos")
        x = sosfiltfilt(sos, x)
        out += x * np.exp(-6.91 * t / rt)
    return out


def make_hall_ir(sr=48000, seconds=3.6, room=(19.0, 34.0, 15.0), src=(9.0, 5.5, 1.3),
                 mics=((7.6, 9.5, 2.8), (10.4, 9.5, 2.8)), rt60_mid=2.05, seed=3,
                 max_order=24, direct=False):
    """Stereo impulse response (n, 2).  With direct=False the direct sound is left out
    so the dry piano keeps its own presence and the hall is mixed underneath."""
    rng = np.random.default_rng(seed)
    n = int(seconds * sr)
    L = np.array(room)
    V = L.prod(); S = 2 * (L[0] * L[1] + L[1] * L[2] + L[0] * L[2])
    # mean absorption from Sabine for the mid band
    alpha = 0.161 * V / (S * rt60_mid)
    refl = np.sqrt(max(1e-3, 1 - alpha))
    ir = np.zeros((n, 2))
    t_mix = 0.085                       # after this the field is treated as diffuse
    # ---- early reflections: image sources
    rng_o = range(-3, 4)
    for ch, mic in enumerate(mics):
        mic = np.array(mic)
        for nx in rng_o:
            for ny in rng_o:
                for nz in rng_o:
                    for px in (0, 1):
                        for py in (0, 1):
                            for pz in (0, 1):
                                img = np.array([(1 - 2 * px) * src[0] + 2 * nx * L[0],
                                                (1 - 2 * py) * src[1] + 2 * ny * L[1],
                                                (1 - 2 * pz) * src[2] + 2 * nz * L[2]])
                                order = abs(2 * nx - px) + abs(2 * ny - py) + abs(2 * nz - pz)
                                if order > max_order:
                                    continue
                                if order == 0 and not direct:
                                    continue
                                d = np.linalg.norm(img - mic)
                                tt = d / C_SOUND
                                if tt > t_mix * 1.6:
                                    continue
                                a = (refl ** order) / d
                                # the floor reflection off the stage is strong, the audience absorbs
                                if pz == 1 and nz == 0:
                                    a *= 0.8
                                pos = tt * sr
                                i0 = int(pos); fr = pos - i0
                                if i0 + 1 < n:
                                    ir[i0, ch] += a * (1 - fr)
                                    ir[i0 + 1, ch] += a * fr
    # time-align so the direct path would sit at t=0
    d0 = min(np.linalg.norm(np.array(src) - np.array(m)) for m in mics) / C_SOUND
    shift = int(d0 * sr)
    ir = np.roll(ir, -shift, axis=0); ir[-shift:] = 0
    # soften reflections slightly (walls are not mirrors): one-pole low-pass that grows with time
    sos = butter(1, 9000 / (sr / 2), output="sos")
    ir = sosfilt(sos, ir, axis=0)
    early_energy = (ir ** 2).sum()

    # ---- diffuse tail
    bands = [63, 125, 250, 500, 1000, 2000, 4000, 8000, 14000]
    rt = rt60_mid * np.array([1.22, 1.18, 1.10, 1.02, 1.0, 0.92, 0.74, 0.50, 0.30])
    tail = np.stack([_band_noise(n, sr, rng, bands, rt) for _ in range(2)], axis=1)
    # a little low-frequency coherence between the channels, as in a real room
    mono = tail.mean(axis=1, keepdims=True)
    sos_l = butter(2, 180 / (sr / 2), output="sos")
    lowm = sosfiltfilt(sos_l, mono, axis=0); lows = sosfiltfilt(sos_l, tail, axis=0)
    tail = tail - 0.6 * lows + 0.6 * lowm
    t = np.arange(n) / sr
    onset = np.clip((t - 0.02) / (t_mix - 0.02), 0, 1) ** 2      # build-up of the diffuse field
    tail *= onset[:, None]
    # level of the tail relative to the early part: set by the hall's reverberant ratio
    tail_energy = (tail ** 2).sum()
    tail *= np.sqrt(early_energy / tail_energy) * 1.55
    ir = ir + tail
    ir *= np.clip((seconds - t) / 0.3, 0, 1)[:, None]            # fade the very end
    ir /= np.sqrt((ir ** 2).sum(axis=0).mean())
    return ir.astype(np.float32)


def width(x, w):
    m = (x[:, 0] + x[:, 1]) * 0.5; s = (x[:, 0] - x[:, 1]) * 0.5
    return np.stack([m + w * s, m - w * s], axis=1)


def place_in_hall(dry, sr=48000, wet_db=-14.0, predelay_ms=18.0, stereo_width=0.62, ir=None):
    """Mix the dry instrument with the hall. wet_db is the hall's RMS level relative to dry."""
    if ir is None:
        ir = make_hall_ir(sr)
    dry = width(dry.astype(np.float32), stereo_width)
    pd = int(predelay_ms * 1e-3 * sr)
    # true-stereo-ish: each dry channel excites both hall channels, mostly its own side
    wl = fftconvolve(dry[:, 0], ir[:, 0]) * 0.8 + fftconvolve(dry[:, 1], ir[:, 0]) * 0.45
    wr = fftconvolve(dry[:, 1], ir[:, 1]) * 0.8 + fftconvolve(dry[:, 0], ir[:, 1]) * 0.45
    wet = np.stack([wl, wr], axis=1)
    wet = np.concatenate([np.zeros((pd, 2), dtype=wet.dtype), wet])
    n = len(wet)
    out = np.zeros((n, 2), dtype=np.float64)
    out[:len(dry)] += dry
    ref = np.sqrt(np.mean(dry.astype(np.float64) ** 2)) + 1e-12
    wr_ = np.sqrt(np.mean(wet[:len(dry)].astype(np.float64) ** 2)) + 1e-12
    out += wet * (ref / wr_) * 10 ** (wet_db / 20.0)
    return out


def low_shelf(x, sr, f0, gain_db):
    """RBJ low shelf, zero-phase."""
    A = 10 ** (gain_db / 40.0); w0 = 2 * np.pi * f0 / sr; cw, sw = np.cos(w0), np.sin(w0)
    alpha = sw / 2 * np.sqrt(2.0)
    b = np.array([A * ((A + 1) - (A - 1) * cw + 2 * np.sqrt(A) * alpha), 2 * A * ((A - 1) - (A + 1) * cw),
                  A * ((A + 1) - (A - 1) * cw - 2 * np.sqrt(A) * alpha)])
    a = np.array([(A + 1) + (A - 1) * cw + 2 * np.sqrt(A) * alpha, -2 * ((A - 1) + (A + 1) * cw),
                  (A + 1) + (A - 1) * cw - 2 * np.sqrt(A) * alpha])
    from scipy.signal import filtfilt
    # filtfilt applies the filter twice: use half the gain per pass
    A2 = 10 ** (gain_db / 80.0)
    b2 = np.array([A2 * ((A2 + 1) - (A2 - 1) * cw + 2 * np.sqrt(A2) * alpha), 2 * A2 * ((A2 - 1) - (A2 + 1) * cw),
                   A2 * ((A2 + 1) - (A2 - 1) * cw - 2 * np.sqrt(A2) * alpha)])
    a2 = np.array([(A2 + 1) + (A2 - 1) * cw + 2 * np.sqrt(A2) * alpha, -2 * ((A2 - 1) + (A2 + 1) * cw),
                   (A2 + 1) + (A2 - 1) * cw - 2 * np.sqrt(A2) * alpha])
    return filtfilt(b2 / a2[0], a2 / a2[0], x, axis=0)


def soft_limit(x, sr, reduce_db, window_ms=30.0):
    """Take the top `reduce_db` off the highest peaks with a slow, look-ahead gain curve
    (what a mastering engineer does to the two or three loudest chords of a recital so
    the quiet pages need not sit lower than necessary). Everything below is untouched."""
    from scipy.ndimage import maximum_filter1d, uniform_filter1d
    env = np.abs(x).max(axis=1)
    thr = env.max() * 10 ** (-reduce_db / 20.0)
    w = int(window_ms * 1e-3 * sr) | 1
    pk = maximum_filter1d(env, size=2 * w + 1)
    gain = np.minimum(1.0, thr / np.maximum(pk, 1e-12))
    gain = uniform_filter1d(uniform_filter1d(gain, size=w), size=w)
    return x * gain[:, None]


def master(x, sr=48000, target_lufs=-19.0, ceiling_db=-1.0, hp_hz=26.0, fade_out=2.5, lead_in=0.4,
           bass_shelf_db=-4.0, bass_shelf_hz=125.0, limit_db=2.5):
    """High-pass, tonal correction, trim, loudness-normalise. No compression: the dynamics
    are the performance.  The low shelf takes out the bass excess of microphones that sit
    12 cm above the strings (calibrated against concert recordings, see reference_compare.py)."""
    import pyloudnorm as pyln
    sos = butter(2, hp_hz / (sr / 2), btype="high", output="sos")
    x = sosfiltfilt(sos, x, axis=0)
    if bass_shelf_db:
        x = low_shelf(x, sr, bass_shelf_hz, bass_shelf_db)
    if limit_db:
        x = soft_limit(x, sr, limit_db)
    # trim trailing silence (keep the natural decay down to -72 dBFS relative to peak)
    env = np.abs(x).max(axis=1)
    thr = env.max() * 10 ** (-72 / 20)
    last = np.nonzero(env > thr)[0][-1]
    x = x[: min(len(x), last + int(0.5 * sr))]
    nf = int(fade_out * sr)
    x[-nf:] *= (np.cos(np.linspace(0, np.pi, nf)) * 0.5 + 0.5)[:, None]
    x = np.concatenate([np.zeros((int(lead_in * sr), 2)), x])
    meter = pyln.Meter(sr)
    loud = meter.integrated_loudness(x)
    g = 10 ** ((target_lufs - loud) / 20.0)
    # true-peak guard (4x oversampled estimate)
    import soxr
    pk = np.abs(soxr.resample(x.astype(np.float32), sr, sr * 4, quality="HQ")).max()
    g = min(g, 10 ** (ceiling_db / 20.0) / pk)
    x = x * g
    return x, dict(input_lufs=float(loud), gain_db=float(20 * np.log10(g)),
                   output_lufs=float(meter.integrated_loudness(x)),
                   true_peak_db=float(20 * np.log10(pk * g)))
