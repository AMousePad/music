"""How do concert-level pianists actually play Chopin nocturnes?

Usage: python -I analyze_performances.py <maestro_root> <out_json>

Reads the MAESTRO v3 Disklavier recordings (International Piano-e-Competition)
of Chopin nocturnes and measures the performance parameters that a rendering
model has to reproduce:
  * key velocity vocabulary, overall and per register role (melody / bass / inner)
  * melody-vs-accompaniment velocity gap ("voicing")
  * melody / bass onset asynchrony at nominally simultaneous attacks
  * within-chord onset spread (rolled / staggered chords)
  * sustain pedal: share of time engaged, depth vocabulary (half-pedalling),
    change rate, and the timing of the pedal change relative to the bass note
  * una corda use
  * articulation: key overlap of consecutive melody notes (finger legato)
  * long-range dynamics: 10-second loudness contour spread
"""
import sys, json, csv, os, statistics, collections
import numpy as np
import pretty_midi



def pct(a, q):
    return float(np.percentile(a, q)) if len(a) else float("nan")


def analyse(r, root=""):
    """r: a MAESTRO csv row, or a dict with midi_filename / canonical_title / year."""
    pm = pretty_midi.PrettyMIDI(os.path.join(root, r["midi_filename"]))
    inst = pm.instruments[0]
    notes = sorted(inst.notes, key=lambda n: (n.start, n.pitch))
    on = np.array([n.start for n in notes]); pit = np.array([n.pitch for n in notes])
    vel = np.array([n.velocity for n in notes]); off = np.array([n.end for n in notes])

    # ---- onset clusters (notes struck "together": within 60 ms of the cluster start)
    clusters, cur = [], [0]
    for i in range(1, len(notes)):
        if on[i] - on[cur[0]] <= 0.06:
            cur.append(i)
        else:
            clusters.append(cur); cur = [i]
    clusters.append(cur)

    mel_v, bass_v, inner_v, gap_mb, async_mb, spread = [], [], [], [], [], []
    mel_idx = []
    for c in clusters:
        ps = pit[c]
        top = c[int(np.argmax(ps))]; bot = c[int(np.argmin(ps))]
        if len(c) >= 2 and pit[top] >= 60 and pit[bot] <= 55 and pit[top] - pit[bot] >= 12:
            mel_v.append(vel[top]); bass_v.append(vel[bot])
            gap_mb.append(int(vel[top]) - int(vel[bot]))
            async_mb.append(1000 * (on[top] - on[bot]))      # >0: melody after bass
            spread.append(1000 * (on[c].max() - on[c].min()))
            inner_v += [vel[i] for i in c if i not in (top, bot)]
            mel_idx.append(top)
        elif len(c) == 1 and pit[c[0]] >= 65:
            mel_idx.append(c[0])

    # melody-line legato: overlap between consecutive top-voice notes (ms, >0 = overlap)
    overlaps = []
    for a, b in zip(mel_idx, mel_idx[1:]):
        gapt = on[b] - on[a]
        if 0.08 < gapt < 1.5 and abs(int(pit[b]) - int(pit[a])) <= 4:
            overlaps.append(1000 * (off[a] - on[b]))

    # ---- pedals
    cc64 = sorted([c for c in inst.control_changes if c.number == 64], key=lambda c: c.time)
    cc67 = sorted([c for c in inst.control_changes if c.number == 67], key=lambda c: c.time)
    dur = pm.get_end_time()
    grid = np.arange(0, dur, 0.01)

    def sample(ccs):
        if not ccs:
            return np.zeros_like(grid)
        t = np.array([c.time for c in ccs]); v = np.array([c.value for c in ccs])
        idx = np.searchsorted(t, grid, side="right") - 1
        return np.where(idx >= 0, v[np.clip(idx, 0, len(v) - 1)], 0)

    p = sample(cc64); s = sample(cc67)
    down = p >= 64
    # pedal changes = releases (down->up crossings of 40) followed by re-press
    lifts = np.where((p[:-1] >= 40) & (p[1:] < 40))[0]
    presses = np.where((p[:-1] < 40) & (p[1:] >= 40))[0]
    # timing of pedal change relative to nearest bass onset
    bass_on = on[pit <= 52]
    lift_rel, press_rel, up_ms = [], [], []
    for li in lifts:
        t = grid[li]
        j = np.searchsorted(bass_on, t)
        cands = [bass_on[k] for k in (j - 1, j) if 0 <= k < len(bass_on)]
        if cands:
            d = min(cands, key=lambda x: abs(x - t))
            if abs(d - t) < 0.4:
                lift_rel.append(1000 * (t - d))
        nxt = presses[presses > li]
        if len(nxt):
            g = 1000 * (grid[nxt[0]] - t)
            if g < 1500:
                up_ms.append(g)
                j = np.searchsorted(bass_on, grid[nxt[0]])
                cands = [bass_on[k] for k in (j - 1, j) if 0 <= k < len(bass_on)]
                if cands:
                    d = min(cands, key=lambda x: abs(x - grid[nxt[0]]))
                    if abs(d - grid[nxt[0]]) < 0.6:
                        press_rel.append(1000 * (grid[nxt[0]] - d))

    # ---- loudness contour: mean velocity in 10 s windows
    win = [vel[(on >= t) & (on < t + 10)].mean() for t in np.arange(0, dur - 10, 5)
           if ((on >= t) & (on < t + 10)).sum() > 5]

    return dict(
        title=r["canonical_title"], year=r["year"], seconds=round(dur), notes=len(notes),
        vel=dict(p05=pct(vel, 5), p25=pct(vel, 25), p50=pct(vel, 50), p75=pct(vel, 75), p95=pct(vel, 95), max=int(vel.max())),
        melody_vel_median=float(np.median(mel_v)) if mel_v else None,
        bass_vel_median=float(np.median(bass_v)) if bass_v else None,
        inner_vel_median=float(np.median(inner_v)) if inner_v else None,
        melody_minus_bass=dict(p25=pct(gap_mb, 25), p50=pct(gap_mb, 50), p75=pct(gap_mb, 75)),
        melody_after_bass_ms=dict(p10=pct(async_mb, 10), p25=pct(async_mb, 25), p50=pct(async_mb, 50),
                                  p75=pct(async_mb, 75), p90=pct(async_mb, 90),
                                  share_bass_first=float(np.mean(np.array(async_mb) > 8)) if async_mb else None,
                                  share_melody_first=float(np.mean(np.array(async_mb) < -8)) if async_mb else None),
        chord_spread_ms=dict(p50=pct(spread, 50), p90=pct(spread, 90)),
        melody_overlap_ms=dict(p25=pct(overlaps, 25), p50=pct(overlaps, 50), p75=pct(overlaps, 75)),
        pedal=dict(share_down=float(down.mean()), share_half=float(((p >= 20) & (p < 90)).mean()),
                   depth_p50_when_down=pct(p[p >= 20], 50) if (p >= 20).any() else None,
                   changes_per_min=60 * len(lifts) / dur,
                   lift_after_bass_ms=dict(p25=pct(lift_rel, 25), p50=pct(lift_rel, 50), p75=pct(lift_rel, 75)),
                   repress_after_bass_ms=dict(p25=pct(press_rel, 25), p50=pct(press_rel, 50), p75=pct(press_rel, 75)),
                   up_time_ms=dict(p25=pct(up_ms, 25), p50=pct(up_ms, 50), p75=pct(up_ms, 75))),
        una_corda_share=float((s >= 64).mean()),
        loudness_windows=dict(min=float(min(win)), max=float(max(win)), sd=float(np.std(win))) if win else None,
    )


if __name__ == "__main__":
    root, out_json = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(os.path.join(root, "maestro-v3.0.0.csv"), encoding="utf8")))
    sel = [r for r in rows if "Chopin" in r["canonical_composer"] and "octurne" in r["canonical_title"]]
    res = []
    for r in sel:
        a = analyse(r, root)
        res.append(a)
        print(f"{a['title'][:38]:38s} {a['year']} {a['seconds']:4d}s vel p5/50/95 {a['vel']['p05']:.0f}/{a['vel']['p50']:.0f}/{a['vel']['p95']:.0f} max{a['vel']['max']}"
              f" | mel {a['melody_vel_median']:.0f} bass {a['bass_vel_median']:.0f} inner {a['inner_vel_median']:.0f}"
              f" | mel-after-bass ms p25/50/75 {a['melody_after_bass_ms']['p25']:.0f}/{a['melody_after_bass_ms']['p50']:.0f}/{a['melody_after_bass_ms']['p75']:.0f}"
              f" bassfirst {100*a['melody_after_bass_ms']['share_bass_first']:.0f}% melfirst {100*a['melody_after_bass_ms']['share_melody_first']:.0f}%"
              f" | ped down {100*a['pedal']['share_down']:.0f}% half {100*a['pedal']['share_half']:.0f}% chg/min {a['pedal']['changes_per_min']:.0f}"
              f" lift {a['pedal']['lift_after_bass_ms']['p50']:.0f} repress {a['pedal']['repress_after_bass_ms']['p50']:.0f} up {a['pedal']['up_time_ms']['p50']:.0f}"
              f" | uc {100*a['una_corda_share']:.0f}% | legato {a['melody_overlap_ms']['p50']:.0f}ms | win {a['loudness_windows']['min']:.0f}-{a['loudness_windows']['max']:.0f}")

    def med(path):
        vals = []
        for a in res:
            v = a
            for k in path:
                v = v[k] if v is not None else None
            if v is not None and v == v:
                vals.append(v)
        return round(statistics.median(vals), 2)

    summary = {
        "n_performances": len(res),
        "velocity_p05": med(["vel", "p05"]), "velocity_p50": med(["vel", "p50"]), "velocity_p95": med(["vel", "p95"]),
        "melody_vel": med(["melody_vel_median"]), "bass_vel": med(["bass_vel_median"]), "inner_vel": med(["inner_vel_median"]),
        "melody_minus_bass_p50": med(["melody_minus_bass", "p50"]),
        "melody_after_bass_ms_p25": med(["melody_after_bass_ms", "p25"]),
        "melody_after_bass_ms_p50": med(["melody_after_bass_ms", "p50"]),
        "melody_after_bass_ms_p75": med(["melody_after_bass_ms", "p75"]),
        "melody_after_bass_ms_p90": med(["melody_after_bass_ms", "p90"]),
        "share_bass_first": med(["melody_after_bass_ms", "share_bass_first"]),
        "share_melody_first": med(["melody_after_bass_ms", "share_melody_first"]),
        "chord_spread_ms_p50": med(["chord_spread_ms", "p50"]), "chord_spread_ms_p90": med(["chord_spread_ms", "p90"]),
        "melody_overlap_ms_p50": med(["melody_overlap_ms", "p50"]),
        "pedal_share_down": med(["pedal", "share_down"]), "pedal_share_half": med(["pedal", "share_half"]),
        "pedal_changes_per_min": med(["pedal", "changes_per_min"]),
        "pedal_lift_after_bass_ms": med(["pedal", "lift_after_bass_ms", "p50"]),
        "pedal_repress_after_bass_ms": med(["pedal", "repress_after_bass_ms", "p50"]),
        "pedal_up_time_ms": med(["pedal", "up_time_ms", "p50"]),
        "una_corda_share": med(["una_corda_share"]),
    }
    print(json.dumps(summary, indent=1))
    json.dump(dict(summary=summary, performances=res), open(out_json, "w"), indent=1)
