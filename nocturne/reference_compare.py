"""Compare a render with real nocturne recordings (public-domain Musopen recordings).

python reference_compare.py <mine.wav> <ref1> <ref2> ...
Long-term spectrum in octave bands (relative to the 250-500 Hz band), stereo image,
loudness range, decay behaviour.  Used to calibrate the hall and the mastering EQ
without relying on ears.
"""
import sys, os
import numpy as np, soundfile as sf
from scipy.signal import welch
import pyloudnorm as pyln

BANDS = [(31, 63), (63, 125), (125, 250), (250, 500), (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000), (8000, 16000)]

def analyse(path):
    x, sr = sf.read(path, always_2d=True)
    if x.shape[1] == 1:
        x = np.repeat(x, 2, axis=1)
    mono = x.mean(axis=1)
    f, P = welch(mono, sr, nperseg=8192)
    b = [10 * np.log10(P[(f >= lo) & (f < hi)].sum() + 1e-30) for lo, hi in BANDS]
    b = np.array(b) - b[3]
    # typical balance: median over time of each band's level (not dominated by the climax)
    from scipy.signal import stft
    ff, tt, Z = stft(mono, sr, nperseg=8192, noverlap=4096)
    Pw = np.abs(Z) ** 2
    act = Pw.sum(axis=0) > Pw.sum(axis=0).max() * 1e-4
    mb = np.array([np.median(10 * np.log10(Pw[(ff >= lo) & (ff < hi)][:, act].sum(axis=0) + 1e-30)) for lo, hi in BANDS])
    mb = mb - mb[3]
    corr = np.corrcoef(x[:, 0], x[:, 1])[0, 1]
    m = (x[:, 0] + x[:, 1]) / 2; s = (x[:, 0] - x[:, 1]) / 2
    sm = 10 * np.log10((s ** 2).mean() / (m ** 2).mean() + 1e-20)
    meter = pyln.Meter(sr); lufs = meter.integrated_loudness(x)
    w = int(3 * sr); st = []
    for i in range(0, len(x) - w, sr):
        v = meter.integrated_loudness(x[i:i + w])
        if np.isfinite(v) and v > lufs - 20: st.append(v)
    lra = np.percentile(st, 95) - np.percentile(st, 10)
    # decay speed after note onsets: median slope of the 400 ms RMS envelope where it falls (dB/s)
    hop = int(0.05 * sr); e = np.array([np.sqrt((mono[i:i + hop] ** 2).mean() + 1e-14) for i in range(0, len(mono) - hop, hop)])
    edb = 20 * np.log10(e); d = np.diff(edb) / 0.05
    fall = d[(d < 0) & (edb[1:] > edb.max() - 45)]
    peak = 20 * np.log10(np.abs(x).max())
    return dict(name=os.path.basename(path)[:28], bands=b, mbands=mb, corr=corr, sm=sm, lufs=lufs, lra=lra,
                fall=np.median(fall), crest=peak - lufs, dur=len(x) / sr)

rows = [analyse(p) for p in sys.argv[1:]]
print(f"{'':28s} " + " ".join(f"{lo:>5d}" for lo, hi in BANDS) + "   corr  S/M   LUFS   LRA  fall dB/s  crest")
for r in rows:
    print(f"{r['name']:28s} " + " ".join(f"{v:5.1f}" for v in r["bands"]) +
          f"   {r['corr']:.2f} {r['sm']:5.1f} {r['lufs']:6.1f} {r['lra']:5.1f} {r['fall']:8.1f} {r['crest']:7.1f}")
print()
print("typical (median over time) balance:")
for r in rows:
    print(f"{r['name']:28s} " + " ".join(f"{v:5.1f}" for v in r["mbands"]))
