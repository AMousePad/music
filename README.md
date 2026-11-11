# Piano pieces composed, performed and recorded in code

Four original pieces for solo piano. Each one is a text file of notes. A program
proof-reads it for harmony, voice leading and playability. A rule-based pianist,
calibrated on recordings of concert pianists, plays it. A sampled Yamaha grand in a
simulated room records it, and LilyPond engraves the score. Nothing is quoted from
existing music.

> No human ear was involved. Every decision was checked by measurement, not by
> listening. See [Known limits](#known-limits).

| Piece | In the manner of | Length | Listen | Score | How it was made |
|---|---|---|---|---|---|
| Nocturne in B minor | Chopin's nocturnes | 4:12 | [MP3](examples/nocturne_b_minor/nocturne_b_minor.mp3) | [PDF](examples/nocturne_b_minor/nocturne_b_minor.pdf) | [nocturne/](nocturne/README.md) |
| The Last Lamp, Nocturne in F minor | Chopin's nocturnes | 5:13 | [MP3](examples/the_last_lamp/the_last_lamp.mp3) | [PDF](examples/the_last_lamp/the_last_lamp.pdf) | [nocturne/last_lamp/](nocturne/last_lamp/README.md) |
| Larkspur Rag | Scott Joplin's classic rags | 3:17 | [MP3](examples/larkspur_rag/larkspur_rag.mp3) | [PDF](examples/larkspur_rag/larkspur_rag.pdf) | [ragtime/](ragtime/README.md) |
| Firethorn, Rhapsodie-Étude in F-sharp minor | Liszt's bravura pieces | 4:11 | [MP3](examples/firethorn/firethorn.mp3) | [PDF](examples/firethorn/firethorn.pdf) | [etude/](etude/README.md) |

The pieces were written by AI coding agents working from short briefs: the Nocturne
in B minor, Larkspur Rag and Firethorn with Claude Code, The Last Lamp with Codex on
the same engine.

## How a piece is made

1. **Research.** Scores and recorded performances in the style are measured: how melodies move, how fast the hands go, how loud the playing is, how the pedal is used (`research/`).
2. **Composition.** The piece is written as text, bar by bar, together with its harmony, for example [etude/firethorn.py](etude/firethorn.py). The notation is described in [engine/README.md](engine/README.md).
3. **Proof-reading.** A checker reports accompaniment notes outside the harmony, unresolved dissonances, parallel fifths and octaves, and passages a hand cannot play.
4. **Performance.** A performer turns the score and an interpretation plan (tempo, dynamics, breaths) into key strokes and pedal movement. The result is compared with the measurements from step 1.
5. **Recording.** The key strokes are played on the Salamander Grand Piano samples with continuous pedalling and string resonance, placed in a simulated room and mastered.
6. **Engraving.** The same text becomes a LilyPond score.
7. **Verification.** The pitch content of the audio is compared with the score; loudness and spectrum are measured.

## Layout

```
engine/      shared tools: notation parser, piano sampler, room and mastering, MIDI and LilyPond output
nocturne/    Nocturne in B minor, and The Last Lamp in nocturne/last_lamp/
ragtime/     Larkspur Rag
etude/       Firethorn
research/    the style measurements and the scripts that produced them
examples/    finished outputs of every piece: MP3, score PDF, performance MIDI, figures, check reports
```

Each genre folder holds the piece itself (notes and interpretation plan), its
proof-reader, its performer, and its build, engrave and verify scripts, with a README
on the research and the music.

## Setup

- **Python 3.12** and the packages in `requirements.txt`: `pip install -r requirements.txt`
- **ffmpeg** on the PATH, for FLAC and MP3 encoding.
- **LilyPond 2.24** for the scores: on the PATH, or unpacked under `tools/lilypond/`, or named by the `LILYPOND` environment variable.
- **The piano.** Download the [Salamander Grand Piano V3](https://freepats.zenvoid.org/Piano/acoustic-grand-piano.html) (the SFZ + FLAC package, 48 kHz / 24 bit, version V3+20200602) and unpack it so that this file exists:
  `soundfonts/salamander/SalamanderGrandPiano-SFZ+FLAC-V3+20200602/SalamanderGrandPianoRetuned-V3+20200602.sfz`.
  Alternatively set `SALAMANDER_SFZ` to that file wherever it is. The first render measures the samples and saves a small voicing table next to them.
- **Research corpora** are only needed to re-run the measurements. Their results are already in `research/*.json`. See [research/README.md](research/README.md).

`soundfonts/`, `tools/`, `corpora/` and `out/` are not tracked.

## Build a piece

```
cd etude
python etude_theory.py                        # proof-read
python build_etude.py --tag final             # perform and record  -> ../out/etude_final
python engrave_etude.py ../out/etude_final    # score
python evaluate_etude.py ../out/etude_final/firethorn_performance.mid
python verify_etude.py final                  # audio against score
```

The other pieces follow the same steps; the commands are in each folder's README.
Builds write to `out/`, and `examples/` holds the finished results. A full render
takes about a minute per piece. Builds are deterministic: the same code gives the
same MIDI and the same audio.

## What this builds on

- **Salamander Grand Piano V3** by Alexander Holm, [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). The recordings in `examples/` are played on it. Credit it if you redistribute them.
- **Style measurements** were derived from the [Chopin first editions in Humdrum](https://github.com/pl-wnifc/humdrum-chopin-first-editions) (Fryderyk Chopin Institute, CC BY 4.0), [MAESTRO v3](https://magenta.tensorflow.org/datasets/maestro) (CC BY-NC-SA 4.0), [ASAP](https://github.com/fosfrancesco/asap-dataset) (CC BY-NC-SA 4.0) and [Scott Joplin's works in Humdrum](https://github.com/craigsapp/joplin) (Craig Sapp, CC BY-NC-SA 4.0). None of that material is in this repository, only statistics derived from it.
- **LilyPond** for engraving and **FFmpeg** for encoding.

## Known limits

- Not auditioned by a human. Measurements cannot say whether a piece is moving.
- The rag's playing is rule-based from written sources; unlike the nocturne it could not be checked against recorded pianists.
- Several of the rag's style measures sit at the edge of Joplin's range (fewer chords in the right hand, more thirds, fewer wide leaps than his median).
- Against Chopin's own melodic statistics the Nocturne in B minor is still slightly low on repeated notes, wide leaps and chromatic notes, and slightly high on thirds (`examples/nocturne_b_minor/score_proofreading.txt`). The corpus figures include right-hand figuration, so the comparison is approximate.
- Firethorn has not been tried by a pianist. Its playability is checked by rule (hand spans, crossings, and the speed of repeated keys, octaves, chords and leaps against the recordings). The score has no fingerings or slurs.
- "Inside the range of 46 recordings" is a loose test, because the range covers very different pieces and players. Firethorn sits at the cautious end on two measures: 12.9 notes a second against a median of 15.6, and 11 leaps a minute where La Campanella has about 80.
- Firethorn's dynamic range is wide (15 LU). The solo bell notes of the introduction sit about 18–21 dB below the average level.
- The irregular left-hand groups in Firethorn's apotheosis (11 notes in the time of 7, 10 in the time of 6) are engraved literally; a pianist would play them freely.
- The corpus study misreads the bar count of Op. 32 No. 2; its per-bar left-hand figures are unreliable.
- If you distribute the audio, credit the Salamander Grand Piano (Alexander Holm, CC BY 3.0). The NC-licensed datasets were used only to derive statistics.
