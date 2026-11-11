"""How do concert pianists play bravura Liszt?

Usage: python -I analyze_virtuoso.py <maestro_root> <out_json>
       (or import measure(path) to apply the same measures to any performance MIDI)

Reference set from MAESTRO v3 (Disklavier recordings, International Piano-e-Competition):
La Campanella, the Hungarian Rhapsodies, Gnomenreigen, Feux follets, Mazeppa, Wilde Jagd,
the Tarantella from Venezia e Napoli.  Measures what a virtuoso showpiece has to live up to
and what a performance model has to reproduce:

  speed        notes per second (1 s windows), inter-onset intervals of the fastest runs
  repetition   how fast the same key is re-struck, and how often
  leaps        how quickly the top line jumps an octave or more
  texture      share of single notes / octaves / full chords, register in use
  touch        velocity vocabulary; how loud fast notes are compared with the rest
  articulation key-hold ratio in fast single-note passages (staccato .. legato)
  pedal        share of time down, changes per minute, pedal in dense vs. sparse seconds
  contrast     spread of loudness and of density over 5 s windows
"""
import csv, json, os, statistics, sys
import numpy as np
import pretty_midi

SEL = ("campanella", "hungarian rhapsody", "gnomenreigen", "feux", "mazeppa", "wilde jagd", "tarantella")


def pct(a, q):
    return float(np.percentile(a, q)) if len(a) else float("nan")


def measure(path):
    pm = pretty_midi.PrettyMIDI(path)
    inst = pm.instruments[0]
    notes = sorted(inst.notes, key=lambda n: (n.start, n.pitch))
    on = np.array([n.start for n in notes]); off = np.array([n.end for n in notes])
    pit = np.array([n.pitch for n in notes]); vel = np.array([n.velocity for n in notes])
    t0, t1 = on.min(), on.max()
    dur = t1 - t0

    # ---- density
    edges = np.arange(t0, t1, 1.0)
    nps = np.histogram(on, bins=np.append(edges, t1 + 1e-6))[0].astype(float)
    w5 = np.array([((on >= t) & (on < t + 5)).sum() / 5.0 for t in np.arange(t0, t1 - 5, 2.5)])
    v5 = np.array([vel[(on >= t) & (on < t + 5)].mean() for t in np.arange(t0, t1 - 5, 2.5)
                   if ((on >= t) & (on < t + 5)).sum() > 4])

    # ---- onset clusters: keys struck together (25 ms: fast runs have IOIs of 60-90 ms)
    clusters, cur = [], [0]
    for i in range(1, len(notes)):
        if on[i] - on[cur[0]] <= 0.025:
            cur.append(i)
        else:
            clusters.append(cur); cur = [i]
    clusters.append(cur)
    c_on = np.array([on[c[0]] for c in clusters]); c_n = np.array([len(c) for c in clusters])
    c_top = np.array([pit[c].max() for c in clusters]); c_bot = np.array([pit[c].min() for c in clusters])
    ioi = np.diff(c_on)
    run_ioi = ioi[(ioi >= 0.045) & (ioi < 0.5)]         # below 45 ms it is a rolled chord, not a run
    octave = np.array([len(c) == 2 and abs(int(pit[c[0]]) - int(pit[c[1]])) == 12 for c in clusters])
    fast = ioi < 0.10                                  # faster than ten attacks a second

    # ---- repeated keys
    rep = []
    last = {}
    for i in range(len(notes)):
        p = pit[i]
        if p in last and on[i] - last[p] < 0.25:
            rep.append(on[i] - last[p])
        last[p] = on[i]
    rep = np.array(rep)

    # ---- leaps in the top line (single notes or octaves, above middle C)
    leap_ioi, leap17, leap_n = [], [], 0
    lean = (c_n == 1) | octave                         # single notes and bare octaves only
    for k in range(len(clusters) - 1):
        d = abs(int(c_top[k + 1]) - int(c_top[k]))
        if lean[k] and lean[k + 1] and c_top[k] >= 60 and c_top[k + 1] >= 60 and 0.05 <= ioi[k] < 0.30 and d >= 12:
            leap_ioi.append(ioi[k]); leap_n += 1
            if d >= 17:
                leap17.append(ioi[k])

    # ---- articulation of fast single notes: how long the key stays down relative to the IOI
    hold = []
    for k in range(len(clusters) - 1):
        if c_n[k] == 1 and ioi[k] < 0.15:
            i = clusters[k][0]
            hold.append((off[i] - on[i]) / ioi[k])
    fast_v = np.array([vel[clusters[k][0]] for k in range(len(clusters) - 1) if ioi[k] < 0.10 and c_n[k] == 1])

    # ---- pedal
    cc = sorted([c for c in inst.control_changes if c.number == 64], key=lambda c: c.time)
    grid = np.arange(t0, t1, 0.01)
    if cc:
        tt = np.array([c.time for c in cc]); vv = np.array([c.value for c in cc])
        idx = np.searchsorted(tt, grid, side="right") - 1
        p = np.where(idx >= 0, vv[np.clip(idx, 0, len(vv) - 1)], 0)
    else:
        p = np.zeros_like(grid)
    down = p >= 64
    lifts = int(((p[:-1] >= 40) & (p[1:] < 40)).sum())
    sec_down = np.array([down[(grid >= e) & (grid < e + 1)].mean() if ((grid >= e) & (grid < e + 1)).any() else 0 for e in edges])
    dense, sparse = nps >= 10, nps <= 5

    return dict(
        seconds=float(dur), notes=int(len(notes)), notes_per_second=float(len(notes) / dur),
        nps_p50=pct(nps, 50), nps_p90=pct(nps, 90), nps_p99=pct(nps, 99), nps_max=float(nps.max()),
        share_seconds_over_12=float((nps >= 12).mean()),
        ioi_ms_p05=1000 * pct(run_ioi, 5), ioi_ms_p25=1000 * pct(run_ioi, 25), ioi_ms_p50=1000 * pct(run_ioi, 50),
        share_attacks_fast=float(fast.mean()),
        repeats_per_min=float(60 * len(rep) / dur), repeat_ioi_ms_p10=1000 * pct(rep, 10), repeat_ioi_ms_p50=1000 * pct(rep, 50),
        leaps_per_min=float(60 * leap_n / dur), leap_ioi_ms_p10=1000 * pct(leap_ioi, 10), leap_ioi_ms_p50=1000 * pct(leap_ioi, 50),
        wide_leaps_per_min=float(60 * len(leap17) / dur), wide_leap_ioi_ms_p10=1000 * pct(leap17, 10) if len(leap17) > 5 else float("nan"),
        share_single=float((c_n == 1).mean()), share_octave=float(octave.mean()), share_chord3plus=float((c_n >= 3).mean()),
        notes_per_attack=float(c_n.mean()),
        pitch_p01=pct(pit, 1), pitch_p05=pct(pit, 5), pitch_p50=pct(pit, 50), pitch_p95=pct(pit, 95), pitch_p99=pct(pit, 99),
        share_above_c6=float((pit >= 84).mean()), share_above_c7=float((pit >= 96).mean()), share_below_c2=float((pit < 36).mean()),
        vel_p05=pct(vel, 5), vel_p25=pct(vel, 25), vel_p50=pct(vel, 50), vel_p75=pct(vel, 75), vel_p95=pct(vel, 95),
        vel_max=float(vel.max()), share_vel_over_100=float((vel >= 100).mean()), share_vel_under_40=float((vel < 40).mean()),
        fast_note_vel_p50=pct(fast_v, 50), fast_minus_all_vel=pct(fast_v, 50) - pct(vel, 50),
        hold_ratio_p25=pct(hold, 25), hold_ratio_p50=pct(hold, 50), hold_ratio_p75=pct(hold, 75),
        pedal_share_down=float(down.mean()), pedal_changes_per_min=float(60 * lifts / dur),
        pedal_down_dense=float(sec_down[dense].mean()) if dense.any() else float("nan"),
        pedal_down_sparse=float(sec_down[sparse].mean()) if sparse.any() else float("nan"),
        density_5s_min=float(w5.min()), density_5s_max=float(w5.max()),
        loudness_5s_min=float(v5.min()), loudness_5s_max=float(v5.max()), loudness_5s_sd=float(v5.std()),
    )


if __name__ == "__main__":
    root, out_json = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(os.path.join(root, "maestro-v3.0.0.csv"), encoding="utf8")))
    sel = [r for r in rows if "Liszt" in r["canonical_composer"] and any(k in r["canonical_title"].lower() for k in SEL)]
    res = []
    for r in sel:
        m = measure(os.path.join(root, r["midi_filename"]))
        m.update(title=r["canonical_title"], year=r["year"], file=r["midi_filename"])
        res.append(m)
        print(f"{m['title'][:44]:44s} {m['year']} {m['seconds']:5.0f}s  n/s {m['notes_per_second']:4.1f} p90 {m['nps_p90']:3.0f} max {m['nps_max']:3.0f}"
              f" | ioi p5 {m['ioi_ms_p05']:3.0f} | rep/min {m['repeats_per_min']:4.0f} p10 {m['repeat_ioi_ms_p10']:3.0f}"
              f" | leaps/min {m['leaps_per_min']:4.0f} p10 {m['leap_ioi_ms_p10']:3.0f} | vel {m['vel_p05']:.0f}/{m['vel_p50']:.0f}/{m['vel_p95']:.0f} max {m['vel_max']:.0f}"
              f" | hold {m['hold_ratio_p50']:.2f} | ped {100*m['pedal_share_down']:.0f}% dense {100*m['pedal_down_dense']:.0f}% chg {m['pedal_changes_per_min']:.0f}", flush=True)
    keys = [k for k in res[0] if isinstance(res[0][k], float)]
    summary = {k: dict(min=min(r[k] for r in res if r[k] == r[k]), median=statistics.median(r[k] for r in res if r[k] == r[k]),
                       max=max(r[k] for r in res if r[k] == r[k])) for k in keys}
    json.dump(dict(n=len(res), summary=summary, performances=res), open(out_json, "w"), indent=1)
    print(f"\n{len(res)} performances")
    for k in keys:
        s = summary[k]
        print(f"  {k:26s} {s['min']:8.2f} / {s['median']:8.2f} / {s['max']:8.2f}")
