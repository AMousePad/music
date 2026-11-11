# Engine

The tools every piece shares. Nothing here knows about a particular piece or genre.

| File | What it does |
|---|---|
| `score.py` | The text notation and its parser: tokens to notes, chord symbols to pitch classes, bars to a `Score` |
| `midi_out.py` | What every performer hands on: key strokes for the sampler, a standard MIDI file, the pedal curve |
| `piano.py` | A sampler for the Salamander Grand Piano with a continuous damper pedal, string resonance, una corda and re-strike handling |
| `hall.py` | A synthesised room (early reflections and a diffuse tail) and mastering (high-pass, tonal correction, loudness, true-peak ceiling) |
| `render_midi.py` | Key strokes and pedal to a finished WAV; also renders any MIDI file: `python render_midi.py in.mid out.wav` |
| `lily.py` | LilyPond helpers: pitch names, note values, one voice of notation text as LilyPond |
| `diagnose.py` | Measurements on a recording: loudness, dynamic range, stereo image, spectrum, clicks. `python diagnose.py in.wav figure.png` |

## The notation

A voice is a string of tokens. The time unit is chosen per piece: the eighth note in
the nocturnes (12/8, 12 units a bar), the sixteenth in the rag and the étude (2/4, 8
units a bar).

```
F#5:6            a note, 6 units long (default length 1)
B4+G5:3          a chord; the top note is the melody
r:3              a rest
(A5)G5:2         grace note before a note
{E5 F#5 B5}:3    a group: n notes spread over 3 units (ornaments, tuplets, runs)
tr(E5 F#5):2.5   a trill on E5 with F#5
D5:3~            tied into the next token
C#7:2'           flags after the length:  !  accent   _  tenuto   '  lighter (or a role the piece defines)
```

Harmony is written as chord symbols, one or two per bar: `F#m`, `C#7`, `G/B`,
`B#dim7`, `DGer6`. Two symbols split the bar in half; `Em/G@0 GIt6@3 F#@6` gives
explicit positions. Known qualities: major, `m`, `6`, `7`, `m7`, `maj7`, `dim`,
`dim7`, `m7b5`, `7b9`, `sus4`, `It6`, `Ger6`, `Fr6`.

A piece builds its score one bar at a time:

```python
from score import Score
sc = Score("My piece", bar_len=8.0)                      # 2/4 with the sixteenth as unit
sc.bar("F#5:2 C#6:2 B5 A5 G#5 A5",                       # right hand
       "F#2:2 F#3+A3+C#4:2 r:2 F#3+A3+C#4:2",            # left hand
       "F#m")                                            # harmony
```

`bar()` also takes a second voice for either hand (`rh2`, `lh2`), a pedal hint and a
texture name. The proof-readers and performers in `genres/` read the result.

## Writing a new piece

Copy the folder in `genres/` that is closest in style. Each has the same parts: the piece (notes
plus the interpretation plan), a proof-reader, a performer that inherits
`PerformanceOutput` from `midi_out.py`, and build, engrave and verify scripts.
