"""Render any performance MIDI file through the project's piano + hall.

python render_midi.py <in.mid> <out.wav> [--start S] [--end S] [--dry]
"""
import argparse, os, sys, time
import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from piano import Piano, midi_to_events, SR
import hall

# the Salamander Grand Piano, unpacked under soundfonts/ (see the README), or wherever SALAMANDER_SFZ points
SFZ = os.environ.get("SALAMANDER_SFZ") or os.path.join(
    HERE, "..", "soundfonts", "salamander",
    "SalamanderGrandPiano-SFZ+FLAC-V3+20200602", "SalamanderGrandPianoRetuned-V3+20200602.sfz")


def render_events(notes, sus, sft, out_path, dry=False, resonance_db=-27.0, wet_db=-14.0,
                  target_lufs=-19.0, verbose=True, ir=None, stereo_width=0.62, master_kw=None):
    t0 = time.time()
    p = Piano(SFZ)
    x = p.render(notes, sus, sft)
    t1 = time.time()
    if resonance_db is not None:
        x = p.add_resonance(x, resonance_db)
    t2 = time.time()
    y = x.astype(np.float64) if dry else hall.place_in_hall(x, SR, wet_db=wet_db, ir=ir, stereo_width=stereo_width)
    y, info = hall.master(y, SR, target_lufs=target_lufs, **(master_kw or {}))
    sf.write(out_path, y.astype(np.float32), SR, subtype="PCM_24")
    if verbose:
        print(f"notes {len(notes)}  piano {t1-t0:.1f}s  resonance {t2-t1:.1f}s  hall+master {time.time()-t2:.1f}s  "
              f"-> {out_path}  {len(y)/SR:.1f}s  {info}")
    return y, info


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("midi"); ap.add_argument("out")
    ap.add_argument("--start", type=float, default=0.0); ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    notes, sus, sft = midi_to_events(a.midi)
    if a.end is not None or a.start > 0:
        e = a.end if a.end is not None else 1e9
        notes = [(on - a.start, off - a.start, k, v) for on, off, k, v in notes if a.start <= on < e]
        def cut(c):
            t = np.array(c[0]); v = np.array(c[1]); m = (t >= a.start - 5) & (t < e)
            return (list(np.maximum(0, t[m] - a.start)), list(v[m]))
        sus, sft = cut(sus), cut(sft)
    render_events(notes, sus, sft, a.out, dry=a.dry)
