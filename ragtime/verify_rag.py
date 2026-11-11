"""Does the recording contain the notes of the score?   python verify_rag.py <tag>

Same method as nocturne/verify_audio.py, in four-bar windows (a rag bar lasts 1.3 s,
too short for a stable spectrum): the pitch-class content of the audio is compared with
what the performance says should sound, and - as a control - with the same notes
transposed by every other interval.  Transposition 0 has to win everywhere.
"""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import stft
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "engine"))
import larkspur_rag as piece
from perform_rag import RagPerformance

tag = sys.argv[1] if len(sys.argv) > 1 else "final"
x, sr = sf.read(os.path.join(HERE, "..", "out", f"ragtime_{tag}", "larkspur_rag.wav"), always_2d=True)
mono = x.mean(axis=1)
sc = piece.build()
perf = RagPerformance(sc, piece.PLAN)
ev = perf.perform()
LEAD = 0.4

f, t, Z = stft(mono, sr, nperseg=8192, noverlap=8192 - 1024)
P = np.abs(Z) ** 2
keep = (f > 60) & (f < 2500)
midi = 69 + 12 * np.log2(f[keep] / 440.0)
pc = np.round(midi).astype(int) % 12
near = np.abs(midi - np.round(midi)) < 0.35
chroma = np.stack([P[keep][(pc == k) & near].sum(axis=0) for k in range(12)])

W = 4
wins = n = 0; worst = 1.0
for b0 in range(0, len(sc.bars), W):
    b1 = min(len(sc.bars), b0 + W)
    t0, t1 = perf.t(b0 * 8.0) + LEAD, perf.t(b1 * 8.0) + LEAD
    m = (t >= t0) & (t < t1)
    a = chroma[:, m].sum(axis=1); a = np.sqrt(a / (a.sum() + 1e-20))
    e = np.zeros(12)
    for nte in ev:
        if b0 < nte["bar"] <= b1:
            w = (nte["vel"] / 64.0) ** 2 * max(0.1, min(nte["off"] - nte["on"], 1.5))
            e[nte["pitch"] % 12] += w
            e[(nte["pitch"] + 7) % 12] += 0.18 * w
            e[(nte["pitch"] + 4) % 12] += 0.06 * w
    e = np.sqrt(e / e.sum())
    sims = [float(np.dot(a, np.roll(e, s)) / (np.linalg.norm(a) * np.linalg.norm(e))) for s in range(12)]
    best = int(np.argmax(sims)); n += 1; wins += best == 0; worst = min(worst, sims[0])
    name, k, p = sc.tags[b0]
    flag = "" if best == 0 else f"   <-- best match is transposition {best}"
    print(f"{name:5s} pass {p} bars {k:2d}-{k + b1 - b0 - 1:2d}  similarity {sims[0]:.3f}  runner-up {sorted(sims)[-2] if best == 0 else sims[best]:.3f}{flag}")
print(f"\n{wins} of {n} four-bar windows: the score at pitch is the best match; lowest similarity {worst:.3f}")
