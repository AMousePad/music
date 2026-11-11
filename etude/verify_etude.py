"""Does the recording contain the notes of the score?   python verify_etude.py <tag>

Same method as nocturne/verify_audio.py.  The piece moves between 27 and 156 quarter
notes a minute, so the windows are sized in time, not in bars: consecutive bars are
gathered until the window lasts three seconds.  For each window the pitch-class content
of the audio is compared with what the performance says should be sounding at that time
(keys held by the fingers or by the pedal, and the undamped top strings) and - as a
control - with the same notes transposed by every other interval.  Transposition 0 has
to win.
"""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import stft
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "engine"))
import firethorn as piece
from perform_etude import Virtuoso

tag = sys.argv[1] if len(sys.argv) > 1 else "final"
x, sr = sf.read(os.path.join(HERE, "..", "out", f"etude_{tag}", "firethorn.wav"), always_2d=True)
mono = x.mean(axis=1)
sc = piece.build()
perf = Virtuoso(sc, piece.PLAN)
ev = perf.perform()
LEAD = 0.4                                   # silence added by the mastering stage

f, t, Z = stft(mono, sr, nperseg=8192, noverlap=8192 - 1024)
P = np.abs(Z) ** 2
keep = (f > 60) & (f < 4500)
midi = 69 + 12 * np.log2(f[keep] / 440.0)
pc = np.round(midi).astype(int) % 12
near = np.abs(midi - np.round(midi)) < 0.35
chroma = np.stack([P[keep][(pc == k) & near].sum(axis=0) for k in range(12)])

# what should be sounding, by the clock: a key sounds until it is released, or - if the pedal
# is down at that moment - until the pedal comes up; the top strings (key 89 and above)
# have no dampers and ring on whatever the hands and feet do
pt, pv = np.array(perf.sustain[0]), np.array(perf.sustain[1])
up_times = pt[(pv < 0.3)]


def sounding_until(e):
    if e["pitch"] >= 89:
        return e["on"] + 3.0
    if np.interp(e["off"], pt, pv) < 0.3:
        return e["off"]
    i = np.searchsorted(up_times, e["off"])
    return min(up_times[i] if i < len(up_times) else e["off"] + 6.0, e["on"] + 8.0)


for e_ in ev:
    e_["end"] = sounding_until(e_)
    e_["T"] = 1.6 * 2.0 ** (-(e_["pitch"] - 60) / 24.0)        # decay time: long in the bass, short on top

tb = [perf.t(i * 8.0) for i in range(len(sc.bars) + 1)]
wins = n = 0; worst = 1.0; b0 = 0
while b0 < len(sc.bars):
    b1 = b0 + 1
    while b1 < len(sc.bars) and tb[b1] - tb[b0] < 3.0:
        b1 += 1
    if len(sc.bars) - b1 < 2:
        b1 = len(sc.bars)
    t0, t1 = tb[b0], tb[b1] + (4.0 if b1 == len(sc.bars) else 0.0)
    m = (t >= t0 + LEAD) & (t < t1 + LEAD)
    a = chroma[:, m].sum(axis=1); a = np.sqrt(a / (a.sum() + 1e-20))
    e = np.zeros(12)
    for nte in ev:
        lo, hi = max(nte["on"], t0), min(nte["end"], t1)
        if hi <= lo:
            continue
        T = nte["T"]
        w = (nte["vel"] / 64.0) ** 3 * T * (np.exp(-(lo - nte["on"]) / T) - np.exp(-(hi - nte["on"]) / T))
        e[nte["pitch"] % 12] += w
        e[(nte["pitch"] + 7) % 12] += 0.18 * w      # third partial (a twelfth above)
        e[(nte["pitch"] + 4) % 12] += 0.06 * w      # fifth partial
    e = np.sqrt(e / e.sum())
    sims = [float(np.dot(a, np.roll(e, s)) / (np.linalg.norm(a) * np.linalg.norm(e))) for s in range(12)]
    best = int(np.argmax(sims)); n += 1; wins += best == 0; worst = min(worst, sims[0])
    name, k = sc.tags[b0]
    flag = "" if best == 0 else f"   <-- best match is transposition {best}"
    print(f"{name:8s} bars {k:2d}-{sc.tags[b1 - 1][1]:2d}  {t1 - t0:4.1f} s  similarity {sims[0]:.3f}  "
          f"runner-up {sorted(sims)[-2] if best == 0 else sims[best]:.3f}{flag}")
    b0 = b1
print(f"\n{wins} of {n} windows: the score at pitch is the best match; lowest similarity {worst:.3f}")
