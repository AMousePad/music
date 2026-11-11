# Examples

The finished outputs of each piece, as built from the code in this repository.

| Folder | Piece | Made by |
|---|---|---|
| [nocturne_b_minor/](nocturne_b_minor) | Nocturne in B minor | [genres/nocturne/](../genres/nocturne/README.md) |
| [the_last_lamp/](the_last_lamp) | The Last Lamp, Nocturne in F minor | [genres/nocturne/last_lamp/](../genres/nocturne/last_lamp/README.md) |
| [larkspur_rag/](larkspur_rag) | Larkspur Rag | [genres/ragtime/](../genres/ragtime/README.md) |
| [firethorn/](firethorn) | Firethorn, Rhapsodie-Étude in F-sharp minor | [genres/etude/](../genres/etude/README.md) |

What the files are:

| File | Content |
|---|---|
| `<piece>.mp3` | The recording |
| `<piece>.pdf`, `<piece>-pageN.png` | The engraved score |
| `<piece>.ly` | The score's LilyPond source |
| `<piece>_performance.mid` | The performance: every key stroke, with continuous sustain pedal and una corda |
| `interpretation.png` | Picture of the performance: notes, tempo, key velocity, pedal |
| `spectrogram.png`, `audio_diagnostics.txt` | Measurements of the recording |
| `score_proofreading.txt` | The composition check: harmony, voice leading, playability |
| `audio_pitch_verification.txt` | The audio compared with the score, passage by passage |
| `evaluation_vs_pianists.txt`, `comparison_with_pianists.txt` | The performance compared with recorded pianists |
| `validation.json` (The Last Lamp) | That piece's combined check report |

The builds also write lossless FLAC and 48 kHz / 24-bit WAV. Those are not stored here
because of their size; rebuild a piece to get them.

The recordings are played on the Salamander Grand Piano V3 by Alexander Holm
([CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)). Keep that credit if you
redistribute them.
