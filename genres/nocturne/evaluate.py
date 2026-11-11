"""Hold the generated performance against the measured playing of concert pianists.

python evaluate.py <performance.mid>
Every metric is computed with the same code that analysed the 19 MAESTRO nocturne
recordings; the table shows where this performance falls inside their range.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "research"))
from analyze_performances import analyse

ref = json.load(open(os.path.join(HERE, "..", "..", "research", "performance_stats.json")))["performances"]
mine = analyse(dict(midi_filename=sys.argv[1], canonical_title="mine", year=""))

def get(d, path):
    for k in path:
        d = d[k] if d is not None else None
    return d

ROWS = [("velocity p05", ["vel", "p05"]), ("velocity median", ["vel", "p50"]), ("velocity p95", ["vel", "p95"]),
        ("velocity max", ["vel", "max"]), ("melody velocity (median)", ["melody_vel_median"]),
        ("bass velocity (median)", ["bass_vel_median"]), ("inner velocity (median)", ["inner_vel_median"]),
        ("melody minus bass", ["melody_minus_bass", "p50"]),
        ("melody after bass ms p25", ["melody_after_bass_ms", "p25"]), ("melody after bass ms p50", ["melody_after_bass_ms", "p50"]),
        ("melody after bass ms p75", ["melody_after_bass_ms", "p75"]), ("share bass first", ["melody_after_bass_ms", "share_bass_first"]),
        ("share melody first", ["melody_after_bass_ms", "share_melody_first"]),
        ("chord spread ms p50", ["chord_spread_ms", "p50"]), ("chord spread ms p90", ["chord_spread_ms", "p90"]),
        ("melody overlap ms p50", ["melody_overlap_ms", "p50"]),
        ("pedal share down", ["pedal", "share_down"]), ("pedal share half", ["pedal", "share_half"]),
        ("pedal changes / min", ["pedal", "changes_per_min"]), ("pedal lift after bass ms", ["pedal", "lift_after_bass_ms", "p50"]),
        ("pedal re-press after bass ms", ["pedal", "repress_after_bass_ms", "p50"]), ("pedal up time ms", ["pedal", "up_time_ms", "p50"]),
        ("una corda share", ["una_corda_share"]), ("10 s loudness window min", ["loudness_windows", "min"]),
        ("10 s loudness window max", ["loudness_windows", "max"]), ("10 s loudness window s.d.", ["loudness_windows", "sd"])]
print(f"{'metric':32s} {'mine':>8s}   {'pianists: min / median / max':32s} verdict")
bad = 0
for name, path in ROWS:
    vals = sorted(v for v in (get(r, path) for r in ref) if v is not None and v == v)
    m = get(mine, path)
    lo, md, hi = vals[0], vals[len(vals) // 2], vals[-1]
    ok = lo <= m <= hi
    bad += not ok
    print(f"{name:32s} {m:8.2f}   {lo:8.2f} / {md:8.2f} / {hi:8.2f}    {'within' if ok else 'OUTSIDE'}")
print(f"\n{len(ROWS) - bad} of {len(ROWS)} metrics inside the range of the recorded pianists")
