"""Engrave this piece with the existing notation primitives and local LilyPond."""
from pathlib import Path
import subprocess
import sys

import piece
from score import _split, _TAIL, dur

# Only the shared conversion functions are imported: no other build or output is executed or read.
from lily import voice_to_ly, ly_pitch, LILY as _LILY
LILY = Path(_LILY)

KEYS = {1: r"\key f \minor", 19: r"\key af \major",
        41: r"\key f \minor", 53: r"\key f \major"}
PRE = {19: r'\tempo "Poco piu mosso, dolce" 4. = 53',
       27: r'\tempo "Poco a poco agitato" 4. = 58',
       37: r'\tempo "Allargando" 4. = 43',
       39: r'\tempo "Quasi cadenza"', 41: r'\tempo "Tempo I" 4. = 49',
       53: r'\tempo "Tranquillo" 4. = 47'}
MARKS = {
    (2, 9): r'\p^\markup\italic "cantabile"',
    (3, 0): r'\p', (5, 0): r'\<', (6, 0): r'\mp', (6, 9): r'\>',
    (7, 0): r'\p', (9, 0): r'^\markup\italic "poco rit."', (10, 6): r'\pp\breathe',
    (11, 0): r'\p^\markup\italic "a tempo"', (12, 0): r'\mp',
    (15, 0): r'\<', (16, 0): r'\mp', (17, 0): r'\>', (18, 0): r'\p\breathe',
    (19, 0): r'\pp^\markup\italic "due voci"', (21, 0): r'\<',
    (22, 6): r'\mp', (23, 0): r'\p', (24, 6): r'\mp',
    (25, 0): r'\>', (26, 0): r'\pp\breathe', (27, 0): r'\p',
    (29, 0): r'\mp^\markup\italic "cresc. e stringendo"',
    (31, 0): r'\mf', (33, 0): r'\f', (35, 0): r'\f\<',
    (37, 0): r'\ff->', (38, 0): r'\f\>', (38, 9): r'\p',
    (39, 0): r'\mp\fermata', (39, 3): r'^\markup\italic "leggiero, dim."',
    (40, 0): r'\pp', (40, 3): r'\breathe', (41, 0): r'\pp^\markup\italic "sotto voce"',
    (43, 0): r'\p', (44, 0): r'\mp', (45, 0): r'\p',
    (47, 0): r'\>', (48, 6): r'\pp', (48, 9): r'\breathe', (49, 0): r'\p^\markup\italic "come un ricordo"',
    (51, 0): r'\pp^\markup\italic "rit."', (52, 0): r'\pp\breathe',
    (53, 0): r'\pp^\markup\italic "dolcissimo"',
    (57, 0): r'^\markup\italic "perdendosi"', (59, 0): r'\ppp',
    (60, 0): r'\ppp\arpeggio\fermata',
}
DOUBLE = {18, 26, 40, 52}
SLURS = [(3, 6), (7, 9), (11, 14), (15, 17), (19, 22), (23, 25),
         (27, 30), (31, 34), (35, 38), (41, 44), (45, 47),
         (49, 51), (53, 56), (57, 59)]

HEAD = r'''\version "2.24.4"
\language "english"
#(set-global-staff-size 17)
\header {
  title = "The Last Lamp"
  subtitle = "Nocturne in F minor"
  subsubtitle = "Concert version for solo piano"
  composer = "Composed with Codex, 2026"
  poet = "In the manner of Chopin"
  tagline = ##f
}
\paper {
  #(set-paper-size "a4")
  page-count = #6
  top-margin = 13\mm bottom-margin = 13\mm
  left-margin = 14\mm right-margin = 14\mm
  system-system-spacing.basic-distance = #20
  ragged-last-bottom = ##f
}
'''


def build_ly(sc):
    upper, lower, pedal = [], [], []
    for b in sc.bars:
        n = b.number
        marks = {float(p): v for (bb, p), v in MARKS.items() if bb == n}
        starts = any(a == n for a, _ in SLURS)
        ends = any(z == n for _, z in SLURS)
        if starts:
            first = min(q.pos for q in b.notes if q.voice == "rh" and q.grace is None)
            marks[first] = marks.get(first, "") + "("
        rh = voice_to_ly(b.raw["rh"], marks)
        if ends:
            rh += ")"
        if marks:
            raise ValueError(f"Unplaced score directions in bar {n}: {marks}")
        if b.raw["rh2"]:
            rh = r"<< { \voiceOne " + rh + r" } \new Voice { \voiceTwo " + voice_to_ly(b.raw["rh2"], {}, True) + r" } >> \oneVoice"
        lm = {}
        if n == 1:
            lm[0.] = r'\pp_\markup\italic "legato, con pedale; sempre delicato"'
        if n == 60:
            lm[0.] = r"\arpeggio\fermata"
        # Keep the arpeggiated left hand legato, with a slur for each wave.
        if n not in (10, 18, 26, 39, 40, 52, 59, 60):
            lm[0.] = lm.get(0., "") + "("
        lh = voice_to_ly(b.raw["lh"], lm)
        if n == 40:
            # A bass-to-treble-to-bass response: change clefs inside the run
            # rather than asking the pianist to read five ledger lines.
            names = b.raw["lh"].split("}")[0][1:].split()
            rendered = []
            for i, name in enumerate(names):
                if i in (6, 13):
                    rendered.append(r"\clef " + ("treble" if i == 6 else "bass"))
                rendered.append(ly_pitch(name) + ("32" if i == 0 else ""))
            lh = r"\tuplet 19/24 { " + " ".join(rendered) + r" } r2."
        if n not in (10, 18, 26, 39, 40, 52, 59, 60):
            lh += ")"
        prefix = KEYS.get(n, "") + " " + PRE.get(n, "")
        dbl = r' \bar "||"' if n in DOUBLE else ""
        # Explicit breaks keep sections from starting halfway through a system.
        br = r" \break" if n in (2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 40, 44, 48, 52, 56) else ""
        if n in (40, 48):
            br = r" \pageBreak"
        elif n == 39:
            br = r" \noPageBreak"
        upper.append(f"  {prefix} {rh} |{dbl}{br} % {n}")
        lower.append(f"  {KEYS.get(n, '')} {lh} |{dbl}{br} % {n}")
        pedal.append(r"s1.")
    return HEAD + (r'''
upper = {
  \clef treble \time 12/8 \tempo "Lento espressivo" 4. = 49
  \override TupletBracket.bracket-visibility = ##f
''' + "\n".join(upper) + '\n  \\bar "|."\n}\n' + r'''
lower = {
  \clef bass \time 12/8
''' + "\n".join(lower) + '\n  \\bar "|."\n}\n' + r'''
\score {
  \new PianoStaff \with { connectArpeggios = ##t } <<
    \new Staff = "upper" \upper
    \new Staff = "lower" \lower
  >>
  \layout {
    \context { \Score \override SpacingSpanner.common-shortest-duration = #(ly:make-moment 1/16) }
  }
  \midi { }
}
''')


def engrave(sc, directory):
    directory = Path(directory)
    ly = directory / f"{piece.STEM}.ly"
    ly.write_text(build_ly(sc), encoding="utf-8")
    result = subprocess.run([str(LILY), "--pdf", "--png", "-dno-point-and-click", "-dresolution=100", "-o",
                             str(directory / piece.STEM), str(ly)],
                            capture_output=True, text=True)
    (directory / "engraving.log").write_text(result.stdout + result.stderr, encoding="utf-8")
    print(result.stderr[-3500:])
    result.check_returncode()
    midi = directory / f"{piece.STEM}.mid"
    if midi.exists():
        midi.replace(directory / f"{piece.STEM}_score.mid")


if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "recording"
    target.mkdir(parents=True, exist_ok=True)
    engrave(piece.build(), target)
