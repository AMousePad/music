# Research

Measurements of scores and recorded performances. The composers' proof-readers and
the performers are calibrated on these numbers. The results are stored here, so the
corpora are only needed to run the measurements again.

| Script | Reads | Writes | Used by |
|---|---|---|---|
| `analyze_scores.py` | Chopin's 19 nocturnes, first editions in Humdrum | `score_stats.json` | the nocturnes: melodic and left-hand style |
| `analyze_performances.py` | 19 recordings of Chopin nocturnes in MAESTRO | `performance_stats.json` | the nocturnes: touch, voicing, hand asynchrony, pedal |
| `analyze_tempo.py` | beat annotations of the Berceuse and Barcarolle in ASAP | `tempo_stats.json` | the nocturnes: rubato |
| `analyze_ragtime.py` | 33 rags by Scott Joplin in Humdrum | `ragtime_stats.json` | Larkspur Rag: rhythm, texture, register |
| `analyze_virtuoso.py` | 46 recordings of bravura Liszt in MAESTRO | `virtuoso_stats.json`, `virtuoso_stats.log` | Firethorn: speed, leaps, repeated notes, touch, pedal |

## Getting the corpora

Put them under `corpora/` (not tracked):

| Folder | Source | Licence |
|---|---|---|
| `corpora/chopin-first-editions` | <https://github.com/pl-wnifc/humdrum-chopin-first-editions> | CC BY 4.0 |
| `corpora/joplin-kern` | <https://github.com/craigsapp/joplin> | CC BY-NC-SA 4.0 |
| `corpora/asap-dataset` | <https://github.com/fosfrancesco/asap-dataset> | CC BY-NC-SA 4.0 |
| `corpora/maestro/maestro-v3.0.0` | <https://magenta.tensorflow.org/datasets/maestro> (the MIDI-only archive is enough) | CC BY-NC-SA 4.0 |

## Running

From the repository root:

```
python -I research/analyze_scores.py        corpora/chopin-first-editions/kern  research/score_stats.json
python -I research/analyze_performances.py  corpora/maestro/maestro-v3.0.0      research/performance_stats.json
python -I research/analyze_tempo.py         corpora/asap-dataset                research/tempo_stats.json
python -I research/analyze_ragtime.py       corpora/joplin-kern/kern            research/ragtime_stats.json
python -I research/analyze_virtuoso.py      corpora/maestro/maestro-v3.0.0      research/virtuoso_stats.json
```

`-I` runs Python in isolated mode, so nothing inside a downloaded folder can be
imported by accident.

The two `evaluate` scripts (`nocturne/evaluate.py`, `etude/evaluate_etude.py`) import
`analyze_performances.py` and `analyze_virtuoso.py`, so a generated performance is
measured by exactly the code that measured the pianists.
