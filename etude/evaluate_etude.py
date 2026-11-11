"""Hold the performance against recorded pianists playing bravura Liszt.

python evaluate_etude.py <performance.mid>
Every measure is computed by the same code (research/analyze_virtuoso.py) that analysed
46 MAESTRO recordings of La Campanella, the Hungarian Rhapsodies, Gnomenreigen, Feux
follets, Mazeppa, Wilde Jagd and the Tarantella.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "research"))
from analyze_virtuoso import measure

ref = json.load(open(os.path.join(HERE, "..", "research", "virtuoso_stats.json")))
mine = measure(sys.argv[1])
ROWS = [
    ("notes per second, whole piece", "notes_per_second"), ("notes per second, median second", "nps_p50"),
    ("notes per second, busiest 10% of seconds", "nps_p90"), ("notes per second, peak second", "nps_max"),
    ("share of seconds with 12+ notes", "share_seconds_over_12"),
    ("gap between attacks in runs, fastest 5% (ms)", "ioi_ms_p05"), ("same, fastest quarter (ms)", "ioi_ms_p25"),
    ("same, median (ms)", "ioi_ms_p50"), ("share of attacks under 100 ms apart", "share_attacks_fast"),
    ("repeated keys per minute", "repeats_per_min"), ("repeated key, fastest 10% (ms)", "repeat_ioi_ms_p10"),
    ("repeated key, median (ms)", "repeat_ioi_ms_p50"),
    ("leaps of an octave or more per minute", "leaps_per_min"), ("leap, median gap (ms)", "leap_ioi_ms_p50"),
    ("share of attacks: single notes", "share_single"), ("share of attacks: bare octaves", "share_octave"),
    ("share of attacks: chords of 3+", "share_chord3plus"), ("notes per attack", "notes_per_attack"),
    ("pitch, 5th percentile", "pitch_p05"), ("pitch, median", "pitch_p50"), ("pitch, 95th percentile", "pitch_p95"),
    ("share of notes above C6", "share_above_c6"), ("share of notes above C7", "share_above_c7"),
    ("share of notes below C2", "share_below_c2"),
    ("velocity p05", "vel_p05"), ("velocity p25", "vel_p25"), ("velocity median", "vel_p50"), ("velocity p75", "vel_p75"),
    ("velocity p95", "vel_p95"), ("velocity max", "vel_max"), ("share of notes at velocity 100+", "share_vel_over_100"),
    ("share of notes under velocity 40", "share_vel_under_40"), ("fast notes minus all notes (velocity)", "fast_minus_all_vel"),
    ("key-hold ratio of fast notes, p25", "hold_ratio_p25"), ("same, median", "hold_ratio_p50"), ("same, p75", "hold_ratio_p75"),
    ("pedal: share of time down", "pedal_share_down"), ("pedal changes per minute", "pedal_changes_per_min"),
    ("pedal down in dense seconds", "pedal_down_dense"), ("pedal down in sparse seconds", "pedal_down_sparse"),
    ("density, quietest 5 s (notes/s)", "density_5s_min"), ("density, busiest 5 s (notes/s)", "density_5s_max"),
    ("loudness, softest 5 s (mean velocity)", "loudness_5s_min"), ("loudness, loudest 5 s", "loudness_5s_max"),
    ("loudness spread over 5 s windows (s.d.)", "loudness_5s_sd"),
]
print(f"{'measure':48s} {'mine':>8s}   {'pianists: min / median / max':30s} verdict")
bad = 0
for name, k in ROWS:
    s = ref["summary"][k]
    m = mine[k]
    ok = s["min"] <= m <= s["max"]
    bad += not ok
    print(f"{name:48s} {m:8.2f}   {s['min']:8.2f} / {s['median']:8.2f} / {s['max']:8.2f}    {'within' if ok else 'OUTSIDE'}")
print(f"\n{len(ROWS) - bad} of {len(ROWS)} measures inside the range of the {ref['n']} recordings")
