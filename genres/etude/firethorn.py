"""Firethorn - Rhapsodie-Etude in F-sharp minor, for piano solo (2026).

An original concert showpiece.  Nothing is quoted; three kinds of keyboard writing are
studied and put to work on one theme:

  * the single running line handed from hand to hand        (C.P.E. Bach, Solfeggietto)
  * a high bell note reached by leaps, and repeated notes   (Liszt, La Campanella)
  * slow rhapsodic opening, stride bass, bravura octaves,
    interlocking octaves and a driven major-key close       (Liszt, Hungarian Rhapsodies)

Notation: see ../../engine/score.py.  Time unit: the sixteenth note; 2/4, 8 units a bar.
A trailing ' marks a bell note.

Form (185 bars)
  Intro    13  Lento a capriccio: the theme's two cells in bare octaves, answered by the bell
  Theme    16  Allegretto capriccioso: 8 + 8, half cadence / Neapolitan / full cadence
  Var. 1   16  Presto: one line relayed between the hands, then right hand against a jump bass
  Var. 2   16  left hand runs, right hand has the theme in chords
  Var. 3   16  Allegretto: every theme note answered by the bell two octaves above
  Var. 4   16  Meno mosso: the theme in repeated notes, first in threes, then in fours
  Trans     2
  Middle   24  Andante cantabile, D major: the theme transformed (augmented, major) as a
               tenor melody inside arpeggios, then in octaves, then an apotheosis that
               moves by major thirds  D - F# - B-flat  and leaves through an augmented sixth
  Retrans   6  dominant pedal, accelerando
  Var. 5   16  Presto con fuoco: both hands in octaves, then octaves over a stride bass
  Coda     44  Vivace, F-sharp major: the theme in major, light, then in octaves; interlocking
               chromatic octaves; hammered cadence; close
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "engine"))
from score import Score, midi, _split, _TAIL, parse_harmony

TITLE = "Firethorn"
SUBTITLE = "Rhapsodie-Étude in F-sharp minor"

# ------------------------------------------------------------------ small tools
_PN = re.compile(r"([A-G](?:##|#|x|bb|b)?)(\d)")


def shift_oct(text, k):
    return _PN.sub(lambda m: m.group(1) + str(int(m.group(2)) + k), text)


def double(text, up=True):
    """every single note becomes an octave (bell notes get their octave below)"""
    out = []
    for tok in _split(text):
        if tok.startswith("("):
            tok = tok.split(")", 1)[1]
        m = _TAIL.match(tok)
        body, d, fl = m.group(1), m.group(2), m.group(3)
        if body == "r" or "+" in body:
            out.append(tok); continue
        other = shift_oct(body, -1 if ("'" in fl or not up) else 1)
        lo, hi = sorted((body, other), key=midi)
        out.append(f"{lo}+{hi}" + (f":{d}" if d else "") + fl.replace("'", ""))
    return " ".join(out)


def repeat32(text):
    """the theme in repeated thirty-seconds (a note before a bell keeps a sixteenth to leap from)"""
    toks, out = _split(text), []
    for i, tok in enumerate(toks):
        m = _TAIL.match(tok)
        body, d, fl = m.group(1), float(m.group(2) or 1), m.group(3)
        if body == "r" or "'" in fl:
            out.append(tok); continue
        n = int(round(d * 2))
        if i + 1 < len(toks) and toks[i + 1].endswith("'") and n >= 4:
            out += [f"{body}:0.5"] * (n - 2) + [f"{body}:1"]
        else:
            out += [f"{body}:0.5"] * n
    return " ".join(out)


def repeat3(text):
    """the theme with every eighth as three repeated notes (the sixteenths stay single)"""
    out = []
    for tok in _split(text):
        m = _TAIL.match(tok)
        body, d, fl = m.group(1), float(m.group(2) or 1), m.group(3)
        out.append(tok if (body == "r" or "'" in fl or d != 2) else "{%s %s %s}:2" % (body, body, body))
    return " ".join(out)


def camp(mel, bell):
    """four theme notes, each answered by the bell"""
    mel = mel.split()
    bell = bell.split() if " " in bell else [bell] * 4
    return " ".join(f"{m} {b}'" for m, b in zip(mel, bell))


SPELL = {"D": "D F# A", "G": "G B D", "A7": "A C# E G", "A": "A C# E", "Bm": "B D F#", "Em": "E G B", "E7": "E G# B D"}


def above(sym, name, n, gap=3):
    """the next n chord tones above a note, none closer than a minor third to the last"""
    names = SPELL[sym.split("/")[0]].split()
    cand = sorted((midi(f"{nm}{o}"), f"{nm}{o}") for nm in names for o in range(2, 8))
    out, last = [], midi(name)
    for p, nm in cand:
        if p >= last + gap:
            out.append(nm); last = p
        if len(out) == n:
            break
    return out


def ripple(mel, harm):
    """the right hand's figure above a tenor melody: silent on the melody note, then up and back"""
    hs = parse_harmony(harm, 8.0)
    at = lambda pos: [s for p, s in hs if p <= pos + 1e-9][-1]
    out, pos = [], 0.0
    for tok in _split(mel):
        m = _TAIL.match(tok)
        d = float(m.group(2) or 1)
        if d == 2:
            a, b = above(at(pos), m.group(1), 2)
            seq = [a, b, a]
        else:
            a, b, c, e = above(at(pos), m.group(1), 4)
            seq = [a, b, c, e, c, b, a]
            if d == 8:
                a, b, c, e, f = above(at(pos + 4), m.group(1), 5)
                seq += [a, b, c, e, f, e, c, b]
        out.append("r:0.5 " + " ".join(f"{x}:0.5" for x in seq))
        pos += d
    return " ".join(out)


def h32(text):
    """a string of thirty-seconds"""
    return " ".join(f"{t}:0.5" for t in text.split())


# ------------------------------------------------------------------ left-hand chords
Fm, C7, Dc, E7, Ac, Bd = "F#3+A3+C#4", "E#3+G#3+B3", "F#3+A3+D4", "E3+G#3+D4", "E3+A3+C#4", "D#3+F#3+A3"
F7, Bm, Gc = "E3+F#3+C#4", "F#3+B3+D4", "G3+B3+D4"
Fs, Bc, Gsm, Fs64, Ger = "A#3+C#4+F#4", "F#3+B3+D#4", "G#3+B3+D#4", "F#3+A#3+C#4", "F#3+A3+B#3"

# harmonic scheme of the theme (one bar each)
HARM = ["F#m", "F#m", "C#7", "C#7", "D", "E7", "A B#dim7", "C#7",
        "F#m", "F#7/A#", "Bm", "G/B", "F#m/C#", "C#7", "F#m", "F#m"]

# ================================================================== INTRODUCTION
INTRO = [
    ("F#3+F#4:4 C#4+C#5:4", "F#1+F#2:4 C#2+C#3:4", "F#m", "recit"),
    ("B3+B4:3 A3+A4:1 G#3+G#4:3 A3+A4:1", "B1+B2:3 A1+A2:1 G#1+G#2:3 A1+A2:1", "F#m", "recit"),
    ("C#4+C#5:1 B#3+B#4:1 C#4+C#5:6", "C#2+C#3:1 B#1+B#2:1 C#2+C#3:6", "F#m", "recit"),
    ("r:2 C#7:2' r:2 C#7:2'", "r:8", "F#m", "bell"),
    ("E#3+E#4:4 B3+B4:4", "E#1+E#2:4 B1+B2:4", "C#7", "recit"),
    ("A3+A4:3 G#3+G#4:1 F#3+F#4:3 G#3+G#4:1", "A1+A2:3 G#1+G#2:1 F#1+F#2:3 G#1+G#2:1", "C#7", "recit"),
    ("B3+B4:1 A#3+A#4:1 B3+B4:6", "B1+B2:1 A#1+A#2:1 B1+B2:6", "C#7", "recit"),
    ("r:2 C#7:2' r:2 C#7:2'", "r:8", "C#7", "bell"),
    ("D5:4 A5:4", f"D2+D3:2 {Dc}:6", "D", "arioso"),
    ("G5:2 F#5:2 E5:2 F#5:2", f"D2+D3:2 {Ger}:6", "DGer6", "arioso"),
    ("A5:3 G#5:1 F#5:4", f"C#2+C#3:2 {Fm}:6", "F#m/C#", "arioso"),
    ("E#5:2 r:2 {A4 B#4 C#5 D5 E#5 F#5 G#5 A5 B#5 C#6 D6 E#6 F#6 G#6 A6 B#6}:4",
     "C#2+C#3:2 {G#3 A3 B#3 C#4 D4 E#4 F#4 G#4}:2 r:4", "C#7", "relay"),
    ("C#7:8'", "r:8", "C#7", "bell"),
]

# ================================================================== THEME
T = [
    "F#5:2 C#6:2 B5 A5 G#5 A5",
    "C#6 B#5 C#6:2 F#5:2 C#7:2'",
    "E#5:2 B5:2 A5 G#5 F#5 G#5",
    "B5 A#5 B5:2 E#5:2 C#7:2'",
    "F#5:2 D6:2 C#6 B5 A5 B5",
    "B5 A#5 B5:2 G#5:2 D6:2",
    "C#6:2 E6:2 D#6 C#6 B#5 A5",
    "G#5:2 C#6:2 E#5:2 C#7:2'",
    "F#5:2 C#6:2 B5 A5 G#5 A5",
    "C#6 B#5 C#6:2 A#5:2 E6:2",
    "D6:2 F#6:2 E6 D6 C#6 D6",
    "D6 C#6 D6:2 B5:2 G5:2",
    "F#5:2 C#6:2 B5 A5 G#5 F#5",
    "G#5 Fx5 G#5:2 B5:2 E#5:2",
    "F#5:2 A5:2 C#6:2 F#6:2",
    "C#6 B#5 C#6:2 F#5:2 C#7:2'",
]
TL = [
    f"F#2:2 {Fm}:2 r:2 {Fm}:2", f"F#2:2 {Fm}:2 r:4",
    f"C#3:2 {C7}:2 r:2 {C7}:2", f"C#3:2 {C7}:2 r:4",
    f"D3:2 {Dc}:2 r:2 {Dc}:2", f"E2:2 {E7}:2 r:2 {E7}:2",
    f"A2:2 {Ac}:2 B#2:2 {Bd}:2", f"C#3:2 {C7}:2 C#2:2 r:2",
    f"F#2:2 {Fm}:2 r:2 {Fm}:2", f"A#2:2 {F7}:2 r:2 {F7}:2",
    f"B2:2 {Bm}:2 r:2 {Bm}:2", f"B2:2 {Gc}:2 r:2 {Gc}:2",
    f"C#3:2 {Fm}:2 r:2 {Fm}:2", f"C#3:2 {C7}:2 C#2:2 {C7}:2",
    f"F#2:2 {Fm}:2 r:2 {Fm}:2", f"F#2:2 {Fm}:2 r:4",
]
THEME = [(T[i], TL[i], HARM[i], "theme") for i in range(16)]

# ================================================================== VAR. 1  the running line
V1_RH = [
    "r:4 C#4 F#4 A4 C#5",
    "F#5 C#6 B5 A5 G#5 F#5 E#5 F#5",
    "r:4 C#4 E#4 G#4 B4",
    "E#5 B5 A5 G#5 F#5 E#5 D#5 E#5",
    "r:4 F#4 A4 D5 F#5",
    "G#5 D6 C#6 B5 A5 G#5 F#5 G#5",
    "r:4 F#4 A4 B#4 D#5",
    "E#5 G#5 F#5 E#5 D#5 C#5 B#4 C#5",
    "F#5 C#5 C#6 A5 B5 A5 G#5 A5",
    "C#6 B#5 C#6 F#5 A#5 F#5 E6 C#6",
    "D6 B5 F#6 D6 E6 D6 C#6 D6",
    "D6 C#6 D6 G5 B5 D5 G5 B4",
    "F#5 C#5 C#6 A5 B5 A5 G#5 F#5",
    "G#5 Fx5 G#5 E#5 B5 E#5 G#5 E#5",
    "F#5 C#5 A5 F#5 C#6 A5 F#6 C#6",
    "C#6 B#5 C#6 A5 F#5 C#5 A4 F#4",
]
V1_LH = [
    "F#2 C#3 F#3 A3 r:4", "r:8",
    "C#3 E#3 G#3 B3 r:4", "r:8",
    "D3 F#3 A3 D4 r:4", "r:8",
    "A2 E3 A3 C#4 r:4", "r:4 C#3:2 C#2:2",
    f"F#2:2 {Fm}:2 C#3:2 {Fm}:2", f"A#2:2 {F7}:2 F#2:2 {F7}:2",
    f"B2:2 {Bm}:2 F#2:2 {Bm}:2", f"B2:2 {Gc}:2 G2:2 {Gc}:2",
    f"C#3:2 {Fm}:2 C#2:2 {Fm}:2", f"C#3:2 {C7}:2 C#2:2 {C7}:2",
    f"F#2:2 {Fm}:2 A2:2 {Fm}:2", f"F#2:2 {Fm}:2 F#2:2 r:2",
]
VAR1 = [(V1_RH[i], V1_LH[i], HARM[i], "relay" if i < 8 else "run_rh") for i in range(16)]

# ================================================================== VAR. 2  the left hand runs
V2_RH = [
    "A4+C#5+F#5:2 F#5+A5+C#6:2 B5 A5 G#5 A5",
    "C#6 B#5 C#6:2 A4+C#5+F#5:2 r:2",
    "G#4+B4+E#5:2 E#5+G#5+B5:2 A5 G#5 F#5 G#5",
    "B5 A#5 B5:2 G#4+B4+E#5:2 r:2",
    "A4+D5+F#5:2 F#5+A5+D6:2 C#6 B5 A5 B5",
    "B5 A#5 B5:2 B4+D5+G#5:2 E5+G#5+D6:2",
    "E5+A5+C#6:2 A5+C#6+E6:2 D#6 C#6 B#5 A5",
    "B4+E#5+G#5:2 E#5+G#5+C#6:2 G#4+B4+E#5:2 r:2",
    "A4+C#5+F#5:2 F#5+A5+C#6:2 B5 A5 G#5 A5",
    "C#6 B#5 C#6:2 C#5+E5+A#5:2 A#5+C#6+E6:2",
    "F#5+B5+D6:2 B5+D6+F#6:2 E6 D6 C#6 D6",
    "D6 C#6 D6:2 D5+G5+B5:2 B4+D5+G5:2",
    "A4+C#5+F#5:2 F#5+A5+C#6:2 B5 A5 G#5 F#5",
    "G#5 Fx5 G#5:2 E#5+G#5+B5:2 G#4+B4+E#5:2",
    "A4+C#5+F#5:2 C#5+F#5+A5:2 F#5+A5+C#6:2 A5+C#6+F#6:2",
    "C#6 B#5 C#6:2 A4+C#5+F#5:2 r:2",
]
V2_LH = [
    "F#2 C#3 F#3 G#3 A3 G#3 F#3 C#3",
    "F#2 C#3 F#3 A3 C#4 A3 F#3 C#3",
    "C#2 G#2 B2 C#3 E#3 C#3 B2 G#2",
    "C#2 G#2 C#3 E#3 G#3 E#3 C#3 G#2",
    "D2 A2 D3 E3 F#3 E3 D3 A2",
    "E2 B2 D3 E3 G#3 E3 D3 B2",
    "A2 E3 A3 E3 B#2 F#3 A3 F#3",
    "C#3 G#3 E#3 C#3 B2 G#2 E#2 C#2",
    "F#2 C#3 A3 C#4 F#4 C#4 A3 C#3",
    "A#2 F#3 C#4 E4 F#4 E4 C#4 F#3",
    "B2 F#3 D4 F#4 B4 F#4 D4 F#3",
    "B2 G3 D4 G4 B4 G4 D4 G3",
    "C#3 A3 C#4 F#4 A4 F#4 C#4 A3",
    "C#3 G#3 B3 E#4 G#4 E#4 B3 G#3",
    "F#2 C#3 F#3 A3 C#4 F#4 A4 C#5",
    "F#4 C#4 A3 F#3 F#2+F#3:2 r:2",
]
VAR2 = [(V2_RH[i], V2_LH[i], HARM[i], "run_lh") for i in range(16)]

# ================================================================== VAR. 3  the bell
V3_RH = [
    camp("F#5 C#6 B5 A5", "C#7"), camp("C#6 B#5 C#6 F#5", "C#7"),
    camp("E#5 B5 A5 G#5", "C#7"), camp("B5 A#5 B5 E#5", "C#7"),
    camp("F#5 D6 C#6 B5", "D7"), camp("B5 A#5 B5 G#5", "D7"),
    camp("C#6 E6 D#6 B#5", "C#7 C#7 D#7 D#7"), camp("G#5 C#6 E#5 G#5", "C#7"),
    "F#5 C#7' C#6 C#7' " + h32("A6 G#6 G6 F#6 F6 E6 D#6 D6"),
    "C#6 C#7' A#5 C#7' " + h32("F#5 G5 G#5 A5 A#5 B5 C6 C#6"),
    "D6 D7' F#6 D7' " + h32("A#6 A6 G#6 G6 F#6 F6 E6 D#6"),
    "D6 D7' B5 D7' " + h32("D6 C#6 C6 B5 A#5 A5 G#5 G5"),
    "F#5 C#7' C#6 C#7' " + h32("E6 D#6 D6 C#6 C6 B5 A#5 A5"),
    "G#5 C#7' B5 C#7' " + h32("D6 C#6 C6 B5 A#5 A5 G#5 G5"),
    "F#5 C#7' C#6 C#7' " + h32("C#6 D6 D#6 E6 E#6 F#6 G6 G#6"),
    camp("A6 F#6 C#6 F#5", "C#7"),
]
VAR3 = [(V3_RH[i], TL[i], HARM[i], "campanella") for i in range(16)]

# ================================================================== VAR. 4  repeated notes
V4_LH = [
    "F#2:2 C#3:2 A3:2 C#3:2", "F#2:2 C#3:2 A3:2 r:2",
    "C#2:2 G#2:2 E#3:2 B2:2", "C#2:2 G#2:2 E#3:2 r:2",
    "D2:2 A2:2 F#3:2 A2:2", "E2:2 B2:2 G#3:2 D3:2",
    "A2:2 E3:2 B#2:2 F#3:2", "C#3:2 G#2:2 C#2:2 r:2",
    "F#2:2 C#3:2 A3:2 C#3:2", "A#2:2 F#3:2 E3:2 C#3:2",
    "B2:2 F#3:2 D4:2 F#3:2", "B2:2 G3:2 D4:2 G3:2",
    "C#3:2 A3:2 F#3:2 A3:2", "C#3:2 G#3:2 B3:2 E#3:2",
    "F#2:2 C#3:2 A3:2 C#3:2", f"F#2:2 C#3:2 {Fm}:2 r:2",
]
VAR4 = [((repeat3 if i < 8 else repeat32)(T[i]), V4_LH[i], HARM[i], "repeat") for i in range(16)]

# ================================================================== TRANSITION
TRANS = [
    ("C#7:2' r:2 C#7:2' r:2", "F#2:2 C#3+A3:6", "F#m", "bell"),
    ("C#7:4' D7:4'", "F#2:2 D3+A3:6", "D/F#", "bell"),
]

# ================================================================== MIDDLE  (D major)
M_MEL = ["D4:4 A4:4", "G4:2 F#4:2 E4:2 F#4:2", "A4:2 G#4:2 A4:4", "D4:8",
         "E4:4 B4:4", "A4:2 G4:2 F#4:2 E4:2", "B4:2 A#4:2 B4:4", "E4:8"]
M_H = ["D", "G/B D/A", "A7", "D/F#", "Em", "Em/G A7", "Bm", "E7/G# A",
       "D", "G/B D/A", "A7", "D7/C", "G/B", "Gm/Bb", "D/A", "A7",
       "D", "G/B D/A", "F#", "B/D# F#/C#", "Bb", "Eb/G Bb/F", "DGer6", "C#7"]
M_LH = [
    "D2 A2 D3 F#3 A2 D3 F#3 A3",
    "B2 D3 G3 B3 A2 D3 F#3 A3",
    "A2 E3 G3 C#4 A2 E3 G3 C#4",
    "F#2 D3 F#3 A3 F#3 D3 F#3 A3",
    "E2 B2 E3 G3 B2 E3 G3 B3",
    "G2 E3 G3 B3 A2 E3 G3 C#4",
    "B2 F#3 B3 D4 B2 F#3 B3 D4",
    "G#2 E3 B3 E3 A2 E3 A3 C#4",
    "{D2 A2 D3 F#3 A3 F#3}:4 {D3 A2 D3 F#3 A3 F#3}:4",
    "{B2 D3 G3 B3 D4 B3}:4 {A2 D3 F#3 A3 D4 A3}:4",
    "{A2 E3 G3 C#4 E4 C#4}:4 {A3 E3 G3 C#4 E4 C#4}:4",
    "{C3 F#3 A3 D4 F#4 D4}:4 {A3 F#3 A3 D4 F#4 D4}:4",
    "{B2 G3 B3 D4 B3 G3}:4 {B2 G3 B3 D4 B3 G3}:4",
    "{Bb2 G3 Bb3 D4 Bb3 G3}:4 {Bb2 G3 Bb3 D4 Bb3 G3}:4",
    "{A2 F#3 A3 D4 A3 F#3}:4 {A2 F#3 A3 D4 A3 F#3}:4",
    "{A2 E3 G3 C#4 G3 E3}:4 {A2 E3 G3 C#4 G3 E3}:4",
    "D1+D2:0.5 {A2 D3 F#3 A3 D4 F#4 A4 F#4 D4 A3 F#3}:3.5 {D3 A2 D3 F#3 A3 D4 F#4 A4 F#4 D4 A3}:3.5 r:0.5",
    "B1+B2:0.5 {G3 B3 D4 G4 B4 G4 D4 B3 G3 D3}:3 r:0.5 A1+A2:0.5 {F#3 A3 D4 F#4 A4 F#4 D4 A3 F#3 D3}:3 r:0.5",
    "F#1+F#2:0.5 {C#3 F#3 A#3 C#4 F#4 A#4 C#5 A#4 F#4 C#4 A#3}:3.5 {F#3 C#3 F#3 A#3 C#4 F#4 A#4 C#5 A#4 F#4 C#4}:3.5 r:0.5",
    "D#2+D#3:0.5 {B3 D#4 F#4 B4 D#5 B4 F#4 D#4 B3 F#3}:3 r:0.5 C#2+C#3:0.5 {A#3 C#4 F#4 A#4 C#5 A#4 F#4 C#4 A#3 F#3}:3 r:0.5",
    "Bb1+Bb2:0.5 " + h32("F3 Bb3 D4 F4 D4 Bb3 F3 Bb3 D4 F4 Bb4 F4 D4 Bb3") + " r:0.5",
    "G1+G2:0.5 " + h32("Eb3 G3 Bb3 Eb4 Bb3 G3") + " r:0.5 F1+F2:0.5 " + h32("D3 F3 Bb3 D4 Bb3 F3") + " r:0.5",
    "D1+D2:0.5 " + h32("A2 D3 F#3 A3 B#3 A3 F#3 D3 A2 D3 F#3 A3 B#3 A3") + " r:0.5",
    "C#1+C#2:8",
]
M_RH = [
    "D4+F#4+D5:4 A4+D5+A5:4",
    "G4+G5:2 F#4+F#5:2 E4+E5:2 F#4+F#5:2",
    "A4+A5:2 G#4+G#5:2 A4+C#5+A5:4",
    "D5+F#5+D6:8",
    "G4+B4+G5:4 D5+G5+D6:4",
    "C5+C6:2 Bb4+Bb5:2 A4+A5:2 Bb4+Bb5:2",
    "A4+D5+A5:4 F#5+A5+F#6:4",
    "E5+G5+E6:4 C#5+G5+C#6:4",
    "D5+F#5+A5+D6:4 A5+D6+F#6+A6:4",
    "G5+B5+D6+G6:2 F#5+F#6:2 E5+E6:2 F#5+A5+D6+F#6:2",
    "F#5+A#5+C#6+F#6:4 C#6+F#6+A#6+C#7:4",
    "B5+D#6+F#6+B6:2 A#5+A#6:2 G#5+G#6:2 A#5+C#6+F#6+A#6:2",
    "Bb4+D5+F5+Bb5:4 F5+Bb5+D6+F6:4",
    "Eb5+G5+Bb5+Eb6:2 D5+D6:2 C5+C6:2 D5+F5+Bb5+D6:2",
    "F#5+A5+B#5:8",
    "E#5+G#5+B5+C#6:8",
]
MIDDLE = ([(ripple(M_MEL[i], M_H[i]), M_LH[i], M_H[i], "sing", M_MEL[i]) for i in range(8)]
          + [(M_RH[i - 8], M_LH[i], M_H[i], "sing8" if i < 16 else "apoth") for i in range(8, 24)])

# ================================================================== RETRANSITION
_TR = "C#2 C#3 C#2 C#3 C#2 C#3 C#2 C#3"
RETRANS = [
    ("r:4 G#5 Fx5 G#5:2", _TR, "C#7", "retrans"),
    ("r:4 B5 A#5 B5:2", _TR, "C#7", "retrans"),
    ("E#6 Dx6 E#6:2 G#6 Fx6 G#6:2", _TR, "C#7", "retrans"),
    (h32("C#7 B#6 A6 G#6 F#6 E#6 D6 C#6 B#5 A5 G#5 F#5 E#5 D5 C#5 B#4"), f"C#2+C#3:2 {C7}:2 r:2 {C7}:2", "C#7", "retrans"),
    (h32("A4 G#4 F#4 E#4 D4 C#4 B#3") + " r:4.5", "r:3.5 " + h32("A3 G#3 F#3 E#3 D3 C#3 B#2 C#3") + " r:0.5", "C#7", "relay"),
    ("C#5 E#5 G#5 C#6 E#6 G#6 C#7:2", "C#2+C#3:2 E#2+E#3:2 G#2+G#3:2 C#2+C#3:2", "C#7", "retrans"),
]

# ================================================================== VAR. 5  octaves
_U = [shift_oct(double(t.replace(" C#7:2'", " r:2"), up=False), 0) for t in T[:8]]     # F#4+F#5 ...
_THUMP = {1: "F#1+F#2", 3: "C#1+C#2", 7: "C#1+C#2"}
V5_RH = _U + [double(t) for t in T[8:15]] + ["C#6+C#7 B#5+B#6 C#6+C#7:2 A5+C#6+F#6:2 r:2"]
V5_LH = [shift_oct(_U[i], -2).replace(" r:2", f" {_THUMP[i]}:2") if i in _THUMP else shift_oct(_U[i], -2) for i in range(8)] + [
    f"F#1+F#2:2 {Fm}:2 C#2+C#3:2 {Fm}:2", f"A#1+A#2:2 {F7}:2 F#2+F#3:2 {F7}:2",
    f"B1+B2:2 {Bm}:2 F#2+F#3:2 {Bm}:2", f"B1+B2:2 {Gc}:2 G2+G3:2 {Gc}:2",
    f"C#2+C#3:2 {Fm}:2 C#2+C#3:2 {Fm}:2", f"C#2+C#3:2 {C7}:2 C#2+C#3:2 {C7}:2",
    f"F#1+F#2:2 {Fm}:2 A1+A2:2 {Fm}:2", "F#2+F#3:2 r:2 F#1+F#2:2 r:2",
]
VAR5 = [(V5_RH[i], V5_LH[i], HARM[i], "unison" if i < 8 else "bravura") for i in range(16)]

# ================================================================== CODA  (F-sharp major)
CA = [
    "(E#5)F#5:2 C#6:2 B5 A#5 G#5 A#5",
    "C#6 B#5 C#6:2 F#5:2 C#7:2'",
    "(Dx5)E#5:2 B5:2 A#5 G#5 F#5 G#5",
    "B5 A#5 B5:2 E#5:2 C#7:2'",
    "(E#5)F#5:2 D#6:2 C#6 B5 A#5 B5",
    "B5 A#5 B5:2 G#5:2 D#6:2",
    "C#6:2 A#5:2 G#5 F#5 E#5 G#5",
    "F#5:2 A#5:2 C#6:2 C#7:2'",
    "(E#5)F#5:2 C#6:2 B5 A#5 G#5 A#5",
    "C#6 B#5 C#6:2 F#5:2 C#7:2'",
    "(Dx5)E#5:2 B5:2 A#5 G#5 F#5 G#5",
    "B5 A#5 B5:2 E#5:2 C#7:2'",
    "D#6:2 F#6:2 E#6 D#6 C#6 D#6",
    "D6 C#6 D6:2 B#5:2 A5:2",
    "A#5:2 C#6:2 B5 G#5 E#5 G#5",
    "F#5:2 C#6:2 F#6:2 C#7:2'",
]
CA_H = ["F#", "F#", "C#7", "C#7", "B", "G#m", "F#/C# C#7", "F#",
        "F#", "F#", "C#7", "C#7", "B", "DGer6", "F#/C# C#7", "F#"]
_ca4 = [f"F#2:2 {Fs}:2 C#3:2 {Fs}:2", f"F#2:2 {Fs}:2 C#3:2 r:2", f"C#3:2 {C7}:2 G#2:2 {C7}:2", f"C#3:2 {C7}:2 G#2:2 r:2"]
CA_LH = _ca4 + [
    f"B2:2 {Bc}:2 F#2:2 {Bc}:2", f"G#2:2 {Gsm}:2 D#3:2 {Gsm}:2", f"C#3:2 {Fs64}:2 C#3:2 {C7}:2", f"F#2:2 {Fs}:2 F#2:2 r:2",
] + _ca4 + [
    f"B2:2 {Bc}:2 F#2:2 {Bc}:2", f"D3:2 {Ger}:2 D2:2 {Ger}:2", f"C#3:2 {Fs64}:2 C#2:2 {C7}:2", f"F#2:2 {Fs}:2 F#2:2 r:2",
]
CA_FIG = [
    "{F#5 A#5 C#6 F#6 A#6 C#7}:4 {B6 A#6 G#6 A#6 F#6 D#6}:4",
    "{C#6 B#5 C#6 F#6 C#6 A#5}:4 {F#5 A#5 C#6 A#5 F#5 C#5}:4",
    "{E#5 G#5 B5 E#6 G#6 B6}:4 {A#6 G#6 F#6 G#6 E#6 C#6}:4",
    "{B5 A#5 B5 E#6 B5 G#5}:4 {E#5 G#5 B5 C#6 E#6 C#6}:4",
    "{D#6 F#6 B6 F#6 D#6 B5}:4 {E#6 D#6 C#6 D#6 B5 F#5}:4",
    "{D6 C#6 D6 F#6 D6 B#5}:4 {A5 B#5 D6 B#5 A5 F#5}:4",
    "{A#5 C#6 F#6 A#6 C#7 A#6}:4 {B6 G#6 E#6 B5 G#5 E#5}:4",
    "{F#5 A#5 C#6 F#6 A#6 C#7}:4 F#6:2 C#7:2'",
]
CODA_A = ([(CA[i], CA_LH[i], CA_H[i], "friska") for i in range(8)]
          + [(CA_FIG[i - 8], CA_LH[i], CA_H[i], "run_rh") for i in range(8, 16)])

_cb4 = [f"F#1+F#2:2 {Fs}:2 C#2+C#3:2 {Fs}:2", f"F#1+F#2:2 {Fs}:2 C#2+C#3:2 r:2",
        f"C#2+C#3:2 {C7}:2 G#1+G#2:2 {C7}:2", f"C#2+C#3:2 {C7}:2 G#1+G#2:2 r:2"]
CB_LH = _cb4 + [
    f"B1+B2:2 {Bc}:2 F#1+F#2:2 {Bc}:2", f"G#1+G#2:2 {Gsm}:2 D#2+D#3:2 {Gsm}:2",
    f"C#2+C#3:2 {Fs64}:2 C#2+C#3:2 {C7}:2", f"F#1+F#2:2 {Fs}:2 F#1+F#2:2 r:2",
] + _cb4 + [
    f"B1+B2:2 {Bc}:2 F#1+F#2:2 {Bc}:2", f"D2+D3:2 {Ger}:2 D1+D2:2 {Ger}:2",
    f"C#2+C#3:2 {Fs64}:2 C#2+C#3:2 {Fs64}:2", f"C#2+C#3:2 {C7}:2 C#2+C#3:2 {C7}:2",
]
CB_RH = [double(t) for t in CA[:14]] + ["A#5+A#6:2 F#5+F#6:2 A#5+A#6:2 C#6+C#7:2", "E#6+E#7:2 C#6+C#7:2 B5+B6:2 G#5+G#6:2"]
CB_H = CA_H[:14] + ["F#/C#", "C#7"]
CODA_B = [(CB_RH[i], CB_LH[i], CB_H[i], "friska8") for i in range(16)]

def interlock(line, first="L"):
    """a single line played as alternating octaves: the left hand takes the note with its
    octave below, the right hand the note with its octave above (thirty-seconds)"""
    rh, lh = [], []
    for i, n in enumerate(line.split()):
        left = (i % 2 == 0) == (first == "L")
        lh.append(f"{shift_oct(n, -1)}+{n}:0.5" if left else "r:0.5")
        rh.append("r:0.5" if left else f"{n}+{shift_oct(n, 1)}:0.5")
    return " ".join(rh), " ".join(lh)


def hammer(chords, octs):
    """left-hand octave, right-hand chord, in alternation (thirty-seconds)"""
    rh = " ".join(f"r:0.5 {c}:0.5" if c else "r:1" for c in chords)
    lh = " ".join(f"{o}:0.5 r:0.5" for o in octs)
    return rh, lh


_C1 = interlock("B#2 C#3 D3 D#3 E3 E#3 F#3 Fx3 G#3 A3 A#3 B3 B#3 C#4 D4 D#4")
_C2 = interlock("E4 E#4 F#4 Fx4 G#4 A4 A#4 B4 B#4 C#5 D5 D#5 E5 E#5")
_C3 = interlock("E#6 D#6 C#6 B5 A#5 G#5 F#5 E#5", first="R")
_C4 = interlock("D#5 C#5 B4 A#4 G#4 F#4 E#4 D#4 C#4 B3 A#3 G#3 F#3", first="R")
_H1 = hammer(["F#4+B4+D#5"] * 2 + ["B4+D#5+F#5"] * 2 + ["F#4+A4+B#4"] * 4, ["D#2+D#3"] * 4 + ["D2+D3"] * 4)
_H2 = hammer(["F#4+A#4+C#5"] * 2 + ["A#4+C#5+F#5"] * 2 + ["C#5+F#5+A#5"] * 2 + ["F#5+A#5+C#6"] * 2, ["C#2+C#3"] * 8)
_H3 = hammer(["G#4+B4+E#5"] * 2 + ["B4+E#5+G#5"] * 2 + ["E#5+G#5+B5"] * 2 + ["G#5+B5+E#6", ""], ["C#2+C#3"] * 8)
CODA_C = [
    # the chromatic scale from B#2 to E#5, the thumbs carrying the line
    (_C1[0], _C1[1], "C#7", "interlock"),
    (_C2[0] + " r:1", _C2[1] + " r:1", "C#7", "interlock"),
    # arrival, then the scale of F-sharp falls three octaves through both hands
    ("A#5+C#6+F#6:4 " + _C3[0], "F#1+F#2:4 " + _C3[1], "F#", "interlock"),
    (_C4[0] + " r:1.5", _C4[1] + " r:1.5", "F#", "interlock"),
    # hammered cadence: IV6 - German sixth - I64 - V7
    (_H1[0], _H1[1], "B/D# DGer6", "martel"),
    (_H2[0], _H2[1], "F#/C#", "martel"),
    (_H3[0], _H3[1], "C#7", "martel"),
    ("G#5+B5+E#6+G#6:2 G#5+B5+E#6+G#6:2 G#5+B5+E#6+G#6:2 r:2", "C#2+C#3:2 C#2+C#3:2 C#1+C#2:2 r:2", "C#7", "final"),
]
CODA_D = [
    ("A#5+C#6+F#6:2 C#5 F#5 A#5 C#6 F#6 A#6", "F#1+F#2:2 C#3 F#3 A#3 C#4 F#4 A#4", "F#", "unison"),
    ("F#6+A#6+C#7:2 r:2 A#5+C#6+F#6:2 r:2", "F#3+A#3+C#4:2 r:2 F#2+C#3+F#3:2 r:2", "F#", "final"),
    ("G#5+B5+C#6+E#6:4 F#5+A#5+C#6+F#6:4", "C#2+C#3:4 F#1+F#2:4", "C#7 F#", "final"),
    ("F#4+A#4+C#5+F#5:8", "F#1+F#2:8", "F#", "final"),
]
CODA = CODA_A + CODA_B + CODA_C + CODA_D

SECTIONS = [("Intro", INTRO), ("Theme", THEME), ("Var1", VAR1), ("Var2", VAR2), ("Var3", VAR3), ("Var4", VAR4),
            ("Trans", TRANS), ("Middle", MIDDLE), ("Retrans", RETRANS), ("Var5", VAR5), ("Coda", CODA)]
KEYS = {"Intro": "F#m", "Middle": "D", "Retrans": "F#m", "Coda": "F#"}

BELL_TX = ("bell", "theme", "campanella", "repeat", "friska", "cadenza", "run_rh")
LINE_TX = ("relay", "interlock")           # one line shared by the hands
ARP_TX = ("sing", "sing8", "apoth")


class VScore(Score):
    """2/4 with the sixteenth as unit; every bar carries a texture that decides the roles."""
    beat = 4.0

    def assign_roles(self):
        for b in self.bars:
            tx = b.texture
            lh_tok = {}
            for n in b.notes:
                if n.hand == "L":
                    lh_tok.setdefault(round(n.s, 4), []).append(n.pitch)
            hpos = {round(p, 4) for p, _ in b.harmony} | {0.0}
            for n in b.notes:
                top = n.chord_rank == n.chord_size - 1
                if n.hand == "R":
                    if "'" in n.flags and tx in BELL_TX:
                        n.role = "bell"
                    elif n.voice == "rh2":
                        n.role = "melody"
                    elif tx in LINE_TX or tx == "run_rh":
                        n.role = "run"
                    elif tx == "sing":
                        n.role = "arp"
                    elif tx == "retrans" and n.chord_size == 1 and n.dur <= 1 and b.notes and len([m for m in b.notes if m.hand == "R"]) >= 8:
                        n.role = "run"
                    else:
                        n.role = "melody" if top else "rh_inner"
                else:
                    ps = sorted(lh_tok[round(n.s, 4)])
                    octave = len(ps) == 2 and ps[1] - ps[0] == 12
                    lowest = n.pitch == ps[0]
                    if tx in LINE_TX or tx == "run_lh":
                        n.role = "run"
                    elif tx in ARP_TX:
                        n.role = "bass" if (round(n.pos, 4) in hpos and (lowest or octave)) else "arp"
                    elif tx == "repeat":
                        n.role = "bass" if abs(n.pos) < 1e-6 else "acc"
                    elif tx in ("recit", "unison"):
                        n.role = "bass"
                    elif octave or len(ps) == 1:
                        n.role = "bass"
                    elif lowest and round(n.pos, 4) in hpos and n.pitch <= 50 and tx in ("final", "bell"):
                        n.role = "bass"
                    else:
                        n.role = "acc"


def build():
    sc = VScore(TITLE, bar_len=8.0)
    sc.tags, sc.where = [], {}
    for name, bars in SECTIONS:
        for i, b in enumerate(bars):
            rh, lh, h, tx = b[:4]
            sc.bar(rh, lh, h, rh2=b[4] if len(b) > 4 else None, texture=tx)
            sc.tags.append((name, i + 1)); sc.where[(name, i + 1)] = len(sc.bars)
    return sc


def span_curve(sc, spans, s):
    """value at score positions s (sixteenths) of a (section, first bar, last bar, v0, v1) table"""
    import numpy as np
    s = np.asarray(s, float)
    out = np.full(s.shape, np.nan)
    for name, b0, b1, v0, v1 in spans:
        a, b = (sc.where[(name, b0)] - 1) * sc.bar_len, sc.where[(name, b1)] * sc.bar_len
        m = (s >= a) & (s < b)
        out[m] = v0 + (v1 - v0) * (s[m] - a) / (b - a)
    bad = np.isnan(out)
    bad[-1:] = False if not bad[-1:].any() else bad[-1:]
    if np.isnan(out[:-1]).any():
        k = int(np.nonzero(np.isnan(out))[0][0])
        raise ValueError(f"no value for bar {int(s[k] // sc.bar_len) + 1}")
    out[np.isnan(out)] = spans[-1][4]
    return out


# ================================================================== the performer's plan
# (section, first bar, last bar, value at the start, value at the end)
TEMPO = [   # quarter notes per minute
    ("Intro", 1, 3, 50, 48), ("Intro", 4, 4, 44, 44), ("Intro", 5, 7, 52, 50), ("Intro", 8, 8, 44, 44),
    ("Intro", 9, 10, 54, 56), ("Intro", 11, 11, 54, 46), ("Intro", 12, 12, 40, 58), ("Intro", 13, 13, 44, 40),
    ("Theme", 1, 7, 96, 97), ("Theme", 8, 8, 95, 91), ("Theme", 9, 15, 97, 98), ("Theme", 16, 16, 96, 88),
    ("Var1", 1, 8, 150, 153), ("Var1", 9, 16, 153, 156),
    ("Var2", 1, 15, 150, 154), ("Var2", 16, 16, 150, 132),
    ("Var3", 1, 15, 108, 112), ("Var3", 16, 16, 108, 96),
    ("Var4", 1, 13, 76, 80), ("Var4", 14, 16, 79, 70),
    ("Trans", 1, 2, 66, 50),
    ("Middle", 1, 8, 56, 57), ("Middle", 9, 15, 60, 62), ("Middle", 16, 16, 60, 54),
    ("Middle", 17, 20, 54, 55), ("Middle", 21, 22, 54, 48), ("Middle", 23, 24, 46, 36),
    ("Retrans", 1, 3, 72, 100), ("Retrans", 4, 5, 104, 112), ("Retrans", 6, 6, 120, 126),
    ("Var5", 1, 8, 130, 133), ("Var5", 9, 15, 136, 140), ("Var5", 16, 16, 136, 118),
    ("Coda", 1, 16, 144, 148), ("Coda", 17, 30, 150, 156), ("Coda", 31, 32, 156, 150),
    ("Coda", 33, 34, 130, 136), ("Coda", 35, 36, 136, 140), ("Coda", 37, 39, 134, 142), ("Coda", 40, 40, 126, 108),
    ("Coda", 41, 41, 150, 150), ("Coda", 42, 42, 132, 120), ("Coda", 43, 43, 96, 80), ("Coda", 44, 44, 80, 80),
]
LEVEL = [   # dynamic level 0 (ppp) .. 1 (fff)
    ("Intro", 1, 3, 0.80, 0.84), ("Intro", 4, 4, 0.36, 0.34), ("Intro", 5, 7, 0.84, 0.90), ("Intro", 8, 8, 0.34, 0.31),
    ("Intro", 9, 10, 0.40, 0.50), ("Intro", 11, 11, 0.48, 0.38), ("Intro", 12, 12, 0.34, 0.62), ("Intro", 13, 13, 0.36, 0.32),
    ("Theme", 1, 4, 0.34, 0.36), ("Theme", 5, 8, 0.38, 0.42), ("Theme", 9, 10, 0.36, 0.42), ("Theme", 11, 12, 0.50, 0.46),
    ("Theme", 13, 16, 0.42, 0.34),
    ("Var1", 1, 8, 0.42, 0.52), ("Var1", 9, 12, 0.52, 0.64), ("Var1", 13, 16, 0.66, 0.74),
    ("Var2", 1, 8, 0.76, 0.80), ("Var2", 9, 12, 0.80, 0.88), ("Var2", 13, 16, 0.86, 0.90),
    ("Var3", 1, 8, 0.28, 0.32), ("Var3", 9, 12, 0.32, 0.40), ("Var3", 13, 16, 0.36, 0.26),
    ("Var4", 1, 8, 0.30, 0.38), ("Var4", 9, 12, 0.42, 0.60), ("Var4", 13, 16, 0.52, 0.26),
    ("Trans", 1, 2, 0.30, 0.24),
    ("Middle", 1, 4, 0.32, 0.36), ("Middle", 5, 8, 0.36, 0.34), ("Middle", 9, 12, 0.48, 0.60), ("Middle", 13, 14, 0.58, 0.52),
    ("Middle", 15, 16, 0.62, 0.80), ("Middle", 17, 20, 0.93, 0.96), ("Middle", 21, 22, 0.80, 0.60), ("Middle", 23, 24, 0.36, 0.24),
    ("Retrans", 1, 3, 0.20, 0.44), ("Retrans", 4, 6, 0.55, 0.90),
    ("Var5", 1, 8, 0.92, 0.94), ("Var5", 9, 16, 0.94, 0.99),
    ("Coda", 1, 8, 0.38, 0.44), ("Coda", 9, 16, 0.46, 0.62), ("Coda", 17, 24, 0.86, 0.90), ("Coda", 25, 32, 0.90, 0.97),
    ("Coda", 33, 34, 0.82, 1.00), ("Coda", 35, 36, 1.00, 0.94), ("Coda", 37, 40, 0.94, 1.00), ("Coda", 41, 44, 1.00, 1.00),
]
BREATHS = [  # (section, bar, pos, seconds of extra time before that point)
    ("Intro", 4, 0, 0.30), ("Intro", 5, 0, 0.70), ("Intro", 8, 0, 0.30), ("Intro", 9, 0, 0.80), ("Intro", 12, 0, 0.12),
    ("Intro", 13, 0, 0.10), ("Theme", 1, 0, 1.50), ("Theme", 9, 0, 0.06),
    ("Var1", 1, 0, 0.22), ("Var2", 1, 0, 0.08), ("Var3", 1, 0, 0.45), ("Var4", 1, 0, 0.28), ("Trans", 1, 0, 0.18),
    ("Middle", 1, 0, 0.40), ("Middle", 5, 0, 0.05), ("Middle", 9, 0, 0.12), ("Middle", 17, 0, 0.16), ("Middle", 19, 0, 0.07),
    ("Middle", 21, 0, 0.07), ("Middle", 23, 0, 0.10), ("Retrans", 1, 0, 1.20),
    ("Var5", 1, 0, 0.18), ("Var5", 9, 0, 0.04), ("Coda", 1, 0, 0.55), ("Coda", 17, 0, 0.10), ("Coda", 35, 0, 0.08),
    ("Coda", 41, 0, 0.14), ("Coda", 43, 0, 0.16), ("Coda", 44, 0, 0.22),
]
UNA_CORDA = [(("Var3", 1), ("Var3", 8)), (("Trans", 1), ("Trans", 2)), (("Middle", 23), ("Middle", 24))]
PLAN = dict(tempo=TEMPO, level=LEVEL, breaths=BREATHS, una_corda=UNA_CORDA, final_hold=2.2,
            arch={"Middle": 0.045, "Intro": 0.02})
