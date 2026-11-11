"""Objective checks on a rendered recording (I cannot listen, so I measure).

python diagnose.py <wav> <out.png>
Prints loudness statistics, stereo correlation, spectral balance, click detection and
decay time of the final chord; writes a spectrogram + loudness-contour figure.
"""
import sys
import numpy as np
import soundfile as sf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import stft
import pyloudnorm as pyln

path, png = sys.argv[1], sys.argv[2]
x, sr = sf.read(path, always_2d=True)
mono = x.mean(axis=1)
meter = pyln.Meter(sr)
lufs = meter.integrated_loudness(x)

# short-term loudness (3 s window, 1 s hop) and momentary-ish RMS (400 ms)
hop = int(0.1 * sr); win = int(0.4 * sr)
rms = np.array([np.sqrt(np.mean(mono[i:i + win] ** 2) + 1e-12) for i in range(0, len(mono) - win, hop)])
rms_db = 20 * np.log10(rms)
act = rms_db[rms_db > rms_db.max() - 50]
print(f"file {path}\n duration {len(x)/sr:.1f}s  integrated {lufs:.1f} LUFS  sample peak {20*np.log10(np.abs(x).max()):.1f} dBFS")
print(f" 400ms RMS dB: p05 {np.percentile(act,5):.1f}  p50 {np.percentile(act,50):.1f}  p95 {np.percentile(act,95):.1f}  max {act.max():.1f}"
      f"  => dynamic span p95-p05 {np.percentile(act,95)-np.percentile(act,5):.1f} dB")
# loudness range (EBU-like): distribution of 3 s loudness
st = []
w3 = int(3 * sr)
for i in range(0, len(x) - w3, sr):
    try:
        st.append(meter.integrated_loudness(x[i:i + w3]))
    except Exception:
        pass
st = np.array([s for s in st if np.isfinite(s) and s > lufs - 20])
if len(st):
    print(f" LRA (p95-p10 of 3 s loudness) {np.percentile(st,95)-np.percentile(st,10):.1f} LU")
corr = np.corrcoef(x[:, 0], x[:, 1])[0, 1]
side = (x[:, 0] - x[:, 1]) / 2; mid = (x[:, 0] + x[:, 1]) / 2
print(f" stereo correlation {corr:.2f}   side/mid energy {10*np.log10((side**2).mean()/(mid**2).mean()):.1f} dB")
# spectral balance
f, t, Z = stft(mono, sr, nperseg=4096, noverlap=3072)
Pw = (np.abs(Z) ** 2).mean(axis=1)
def band(lo, hi):
    m = (f >= lo) & (f < hi)
    return 10 * np.log10(Pw[m].sum() / Pw.sum() + 1e-20)
print(" energy share dB: <100Hz %.1f | 100-400 %.1f | 400-1.6k %.1f | 1.6-6k %.1f | >6k %.1f" %
      (band(0, 100), band(100, 400), band(400, 1600), band(1600, 6000), band(6000, 24000)))
cent = (f[:, None] * np.abs(Z) ** 2).sum(axis=0) / ((np.abs(Z) ** 2).sum(axis=0) + 1e-20)
print(f" spectral centroid median {np.median(cent):.0f} Hz")
# clicks: large sample-to-sample jumps relative to local level
d = np.abs(np.diff(mono))
print(f" max |dx| {d.max():.4f} (p99.99 {np.percentile(d, 99.99):.4f})  DC {mono.mean():.2e}")
# final decay: time from last -20 dB(rel. to peak) crossing to -60
env = np.abs(mono); k = int(0.05 * sr)
envs = np.convolve(env, np.ones(k) / k, mode="same"); e_db = 20 * np.log10(envs / envs.max() + 1e-12)
tail = e_db[-int(12 * sr):]
print(f" last 12 s level: start {tail[0]:.1f} dB  end {tail[-int(0.2*sr)]:.1f} dB")

fig, ax = plt.subplots(2, 1, figsize=(16, 8), gridspec_kw={"height_ratios": [3, 1]})
S = 20 * np.log10(np.abs(Z) + 1e-9)
ax[0].pcolormesh(t, f, S, vmin=S.max() - 90, vmax=S.max(), shading="auto", cmap="magma")
ax[0].set_yscale("log"); ax[0].set_ylim(30, 12000); ax[0].set_ylabel("Hz"); ax[0].set_title(path)
ax[1].plot(np.arange(len(rms_db)) * hop / sr, rms_db, lw=0.8); ax[1].set_ylim(rms_db.max() - 55, rms_db.max() + 3)
ax[1].set_xlim(0, len(mono) / sr); ax[1].set_ylabel("RMS dBFS"); ax[1].set_xlabel("s"); ax[1].grid(alpha=0.3)
plt.tight_layout(); plt.savefig(png, dpi=80)
print(" wrote", png)
