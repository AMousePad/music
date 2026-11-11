"""Does the recording contain the notes of the score?

python verify_audio.py <tag>
For every bar the pitch-class content of the audio (chroma from the spectrum) is compared
with what the score says should be sounding.  As a control the same comparison is made
against the score transposed by every other interval: the true transposition (0) has to
win in every bar.  This catches wrong notes in the renderer (it is how a mis-mapped
sample would show up) independently of the MIDI data.
"""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import stft
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "engine"))
import nocturne_bm as piece
from perform import Performance

tag = sys.argv[1] if len(sys.argv) > 1 else "final"
wav = os.path.join(HERE, "..", "..", "out", f"nocturne_{tag}", "nocturne_b_minor.wav")
x, sr = sf.read(wav, always_2d=True)
mono = x.mean(axis=1)
sc = piece.build()
perf = Performance(sc, piece)
ev = perf.perform()
LEAD = 0.4                                   # silence added by the mastering stage

f, t, Z = stft(mono, sr, nperseg=16384, noverlap=16384 - 2048)
P = np.abs(Z) ** 2
keep = (f > 60) & (f < 2500)
midi = 69 + 12 * np.log2(f[keep] / 440.0)
pc = np.round(midi).astype(int) % 12
near = np.abs(midi - np.round(midi)) < 0.35  # ignore energy between semitones
chroma = np.zeros((12, P.shape[1]))
for k in range(12):
    chroma[k] = P[keep][(pc == k) & near].sum(axis=0)

worst, wins, rows = 1.0, 0, []
for b in sc.bars:
    t0 = perf.t(perf.S(b.number, 0)) + LEAD
    t1 = perf.t(perf.S(b.number + 1, 0)) + LEAD if b.number < len(sc.bars) else t0 + 6
    m = (t >= t0 + 0.15) & (t < t1)
    a = chroma[:, m].sum(axis=1); a = np.sqrt(a / (a.sum() + 1e-20))
    e = np.zeros(12)
    for n in ev:
        if n["bar"] == b.number:
            w = (n["vel"] / 64.0) ** 2 * max(0.2, min(n["off"] - n["on"], 2.0))
            e[n["pitch"] % 12] += w
            e[(n["pitch"] + 7) % 12] += 0.18 * w      # third partial (a twelfth above)
            e[(n["pitch"] + 4) % 12] += 0.06 * w      # fifth partial
    e = np.sqrt(e / e.sum())
    sims = [float(np.dot(a, np.roll(e, s)) / (np.linalg.norm(a) * np.linalg.norm(e))) for s in range(12)]
    best = int(np.argmax(sims))
    wins += best == 0
    worst = min(worst, sims[0])
    rows.append((b.number, sims[0], best, sorted(sims)[-2] if best == 0 else sims[best]))
    flag = "" if best == 0 else f"   <-- best match is transposition {best}"
    print(f"bar {b.number:2d}  similarity {sims[0]:.3f}   runner-up {rows[-1][3]:.3f}{flag}")
print(f"\n{wins} of {len(sc.bars)} bars: the score at pitch is the best match; lowest similarity {worst:.3f}")
