"""Larkspur Rag  -  a classic rag in E-flat, 2/4, "Not fast"

An original composition in the manner of Scott Joplin's rags (no strain is quoted or
adapted from any of them).  Time unit of the notation: the sixteenth note, 8 to the bar.

Form (the classic rag layout)      INTRO  A A  B B  A  C C  D D
    Intro  4 bars   both hands in octaves, a rising sequence, stop on the dominant seventh
    A     16 bars   E-flat.  The "rocking" motif  (G-Eb-G~ Eb-Bb)  with the tie over the
                    middle of the bar, answered by scale figures.
                    I I V7 V7 | V7 V7 I I | I I7 IV iv | I6/4 VI7 II7-V7 I
    B     16 bars   E-flat, starting on the dominant.  A three-note cell repeated across
                    the beats (short-long-short); excursion to the relative minor
                    (V7/vi - vi); a broad phrase in thirds over IV - #iv dim; the rocking
                    motif returns in a falling sequence for the cadence.
    C     16 bars   Trio, A-flat (subdominant).  Lyrical; the syncopation is now a held
                    note inside a singing line.  The phrase is restated a fourth higher
                    over IV and darkens to iv (D-flat minor) before the cadence.
    D     16 bars   back in E-flat, entered through its subdominant - the A-flat chord the
                    trio ended on.  IV #iv-dim I6/4 VI7 ii II7 V7: the rocking motif over
                    the circle of fifths, first in the middle register, then an octave
                    higher in full octaves.

The performer's plan is PLAN at the bottom; perform_rag.py reads it.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
from score import Score

TITLE = "Larkspur Rag"

# ------------------------------------------------------------------ left-hand vocabulary
def march(b1, chord, b2, chord2=None):
    """bass octave - chord - bass octave - chord, in eighths"""
    return f"{b1}:2 {chord}:2 {b2}:2 {chord2 or chord}:2"

def oom_pah_oom(b1, chord, b2):
    return f"{b1}:2 {chord}:2 {b2}:4"

def broad(b1, chord):
    return f"{b1}:4 {chord}:4"

# after-beat chords
cEb, cBb7, cAb, cAbm = "G3+Bb3+Eb4", "Ab3+Bb3+D4", "Ab3+C4+Eb4", "Ab3+Cb4+Eb4"
cEb7, cC7, cF7, cG7, cCm = "G3+Bb3+Db4", "G3+Bb3+E4", "A3+C4+Eb4", "F3+G3+B3", "G3+C4+Eb4"
cAdim, cFm, cAb7, cDb, cDbm = "Gb3+C4+Eb4", "Ab3+C4+F4", "Gb3+C4+Eb4", "Ab3+Db4+F4", "Ab3+Db4+Fb4"
# bass octaves
oEb, oBb, oBbLow, oAb, oF, oC, oG = "Eb2+Eb3", "Bb2+Bb3", "Bb1+Bb2", "Ab2+Ab3", "F2+F3", "C2+C3", "G2+G3"
oD, oE, oA, oDb, oB = "D2+D3", "E2+E3", "A2+A3", "Db2+Db3", "B2+B3"

END_LH = "Eb2+Eb3:2 Bb1+Bb2:2 Eb2+Eb3:4"
END_RH = "G4+Bb4+Eb5:2 Ab4+Bb4+D5:2 G4+Bb4+Eb5:4"
END_H = "Eb@0 Bb7@2 Eb@4"

INTRO = [
    ("Eb4+Eb5 G4+G5 Bb4+Bb5 C5+C6:2 Bb4+Bb5 G4+G5 Eb4+Eb5", "Eb3 G3 Bb3 C4:2 Bb3 G3 Eb3", "Eb6"),
    ("F4+F5 Ab4+Ab5 Bb4+Bb5 D5+D6:2 Bb4+Bb5 Ab4+Ab5 F4+F5", "F3 Ab3 Bb3 D4:2 Bb3 Ab3 F3", "Bb7"),
    ("G4+G5 Bb4+Bb5 Eb5+Eb6 F5+F6:2 Eb5+Eb6 C5+C6 A4+A5", "G3 Bb3 Eb4 F4:2 Eb4 C4 A3", "Eb@0 F7@3"),
    ("Ab4+Bb4+D5:2 r:2 Ab4+Bb4+D5+F5:2 r:2", "Bb1+Bb2:2 r:2 Bb1+Bb2:2 r:2", "Bb7"),
]

STRAIN_A = [
    ("G4+G5:2 Eb5 G4+G5:2 Eb5 G4+Bb4:2", march(oEb, cEb, oBb), "Eb"),                              # 1
    ("C5 D5 Eb5 C5+C6:2 Bb5 G5 Eb5", march(oEb, cEb, oBb), "Eb6"),                                  # 2
    ("F4+F5:2 D5 F4+F5:2 D5 Ab4:2", march(oBb, cBb7, oF), "Bb7"),                                  # 3
    ("Bb4 C5 D5 Bb4+Bb5:2 Ab5 F5 D5", march(oBb, cBb7, oF), "Bb7"),                                # 4
    ("F5 E5 Eb5 D5 C5 Bb4 Ab4 G4", f"{oBb}:2 {oD}:2 {oF}:2 {oAb}:2", "Bb7"),                       # 5
    ("F4+Ab4:2 Bb4 Ab4+D5:2 F5 Eb5 D5", march(oF, cBb7, oBb), "Bb7"),                                     # 6
    ("G4+Eb5:2 Bb4 G4+Eb5:2 Bb4 G4:2", march(oEb, cEb, oBb), "Eb"),                                      # 7
    ("G4+Bb4+Eb5:4 r E5 F5 Gb5", f"{oEb}:2 {cEb}:2 {oBbLow}:2 {oD}:2", "Eb@0 Bb7@4"),              # 8
    ("G4+G5:2 Eb5 G4+G5:2 Eb5 G4+Bb4:2", march(oEb, cEb, oBb), "Eb"),                              # 9
    ("Db5 Eb5 F5 Db5+G5:2 F5 Eb5 Db5", march(oEb, cEb7, oBb), "Eb7"),                               # 10
    ("Ab4+Ab5:2 Eb5 Ab4+Ab5:2 Eb5 C5:2", march(oAb, cAb, oEb), "Ab"),                              # 11
    ("Ab4+Ab5:2 Cb5+Gb5:2 Ab4+Fb5:2 Ab4+Eb5:2", broad(oAb, cAbm), "Abm"),                                      # 12
    ("Bb4 Eb5 G5 Bb4+Bb5:2 Ab5 G5 Eb5", march(oBbLow, cEb, oBb), "Eb/Bb"),                         # 13
    ("E5 G5:2 Bb5 E5+C6 Bb5:2 G5", f"{oC}:2 {cC7}:2 {oG}:2 {oE}:2", "C7"),                            # 14
    ("F5 G5 A5 C6 Bb5 Ab5 F5 D5", f"{oF}:2 {cF7}:2 {oBbLow}:2 {cBb7}:2", "F7 Bb7"),                # 15
    (END_RH, END_LH, END_H),                                                                       # 16
]

STRAIN_B = [
    ("Ab4+Ab5 F5:2 D5 Ab4+Ab5 F5:2 D5", march(oBb, cBb7, oF), "Bb7"),                              # 1
    ("C5 D5 F5 Bb4+Bb5:2 Ab5 G5 F5", march(oBb, cBb7, oD), "Bb7"),                                 # 2
    ("G4+G5 Eb5:2 Bb4 G4+G5 Eb5:2 Bb4", march(oEb, cEb, oBb), "Eb"),                               # 3
    ("G5 F5 Eb5 D5 G4+Bb4+Eb5:4", f"{oEb}:2 {cEb}:2 {oEb}:2 {oF}:2", "Eb"),                        # 4
    ("G4+G5 D5:2 B4 G4+G5 D5:2 B4", march(oG, cG7, oD), "G7"),                                     # 5
    ("A4 B4 D5 G4+G5:2 F5 Eb5 D5", march(oG, cG7, oB), "G7"),                                      # 6
    ("G4+G5 Eb5:2 C5 G4+G5 Eb5:2 C5", march(oC, cCm, oEb), "Cm"),                                   # 7
    ("G4+C5:4 r G4 A4 B4", f"{oC}:2 {cCm}:2 {oC}:2 {oG}:2", "Cm"),                             # 8
    ("Ab4+C5:3 Bb4 Ab4+C5:2 C5+Eb5:2", broad(oAb, cAb), "Ab"),                                     # 9
    ("C5+Eb5:3 D5 C5+Eb5:2 Eb5+Gb5:2", broad(oA, cAdim), "Adim7"),                                 # 10
    ("G4+G5:2 Eb5 G4+G5:2 Eb5 Bb4:2", march(oBbLow, cEb, oBb), "Eb/Bb"),                           # 11
    ("E4+E5:2 C5 E5:2 C5 Bb4:2", march(oC, cC7, oG), "C7"),                                        # 12
    ("Eb4+Eb5:2 C5 Eb5:2 C5 A4:2", march(oF, cF7, oC), "F7"),                                      # 13
    ("Bb4 C5 D5 F5 Ab5 G5 F5 D5", f"{oBbLow}:2 {cBb7}:2 {oF}:2 {oD}:2", "Bb7"),                    # 14
    ("Eb5 F5 G5 Eb5+Eb6:2 D6 C6 Bb5", march(oEb, cEb, oBb), "Eb"),                               # 15
    (END_RH, END_LH, END_H),                                                                       # 16
]

STRAIN_C = [  # trio, A-flat major
    ("C5:2 Ab4+Eb5:3 Eb5 F5 G5", march(oAb, cAb, oC), "Ab"),                                      # 1
    ("C5+Ab5:3 G5 F5:2 Eb5:2", oom_pah_oom(oAb, cAb, oEb), "Ab"),                                  # 2
    ("Bb4:2 G4+Db5:3 Db5 Eb5 F5", march(oEb, cEb7, oBb), "Eb7"),                                   # 3
    ("Bb4+G5:3 F5 Eb5:2 Db5:2", oom_pah_oom(oEb, cEb7, oBb), "Eb7"),                               # 4
    ("G4 Bb4 Db5 G5:2 F5 Eb5 Db5", march(oEb, cEb7, oG), "Eb7"),                                   # 5
    ("Bb4 Db5 Eb5 Bb5:2 Ab5 G5 Eb5", march(oBb, cEb7, oEb), "Eb7"),                                # 6
    ("Ab4+C5:3 Bb4 C5:2 Eb5:2", march(oAb, cAb, oEb), "Ab"),                                       # 7
    ("C5+Eb5+Ab5:4 r Ab4 Bb4 B4", f"{oAb}:2 {cAb}:2 {oEb}:2 {oG}:2", "Ab@0 Eb7@4"),                # 8
    ("C5:2 Ab4+Eb5:3 Eb5 F5 G5", march(oAb, cAb, oC), "Ab"),                                      # 9
    ("C5+Ab5:3 Gb5 F5:2 Eb5:2", oom_pah_oom(oAb, cAb7, oC), "Ab7"),                                # 10
    ("F5:2 Db5+Ab5:3 Ab5 Bb5 C6", march(oDb, cDb, oAb), "Db"),                                     # 11
    ("Fb5+Db6:3 Cb6 Bbb5:2 Ab5:2", broad(oDb, cDbm), "Dbm"),                                        # 12
    ("Eb5 Ab5 C6 Eb5+Eb6:2 Db6 C6 Ab5", march(oEb, cAb, oEb), "Ab/Eb"),                            # 13
    ("F5 A5 C6 Eb6:2 D6 C6 A5", march(oF, cF7, oC), "F7"),                                         # 14
    ("D5 F5 Ab5 Bb5 Db5 Eb5 G5 Bb5", f"{oBbLow}:2 {cBb7}:2 {oEb}:2 {cEb7}:2", "Bb7 Eb7"),          # 15
    ("C5+Eb5+Ab5:2 Db5+Eb5+G5:2 C5+Eb5+Ab5:4", "Ab2+Ab3:2 Eb2+Eb3:2 Ab1+Ab2:4", "Ab@0 Eb7@2 Ab@4"),  # 16
]

STRAIN_D = [
    ("Eb4+Eb5:2 C5 Ab4+Eb5:2 C5 Ab4:2", march(oAb, cAb, oEb), "Ab"),                                   # 1
    ("A4 C5:2 D5 Eb5:2 C5:2", march(oA, cAdim, oEb), "Adim7"),                                    # 2
    ("G4+G5:2 Eb5 G4+G5:2 Eb5 Bb4:2", march(oBbLow, cEb, oBb), "Eb/Bb"),                           # 3
    ("G4 Bb4:2 C5 E5:2 C5:2", f"{oC}:2 {cC7}:2 {oG}:2 {oE}:2", "C7"),                              # 4
    ("Ab4+F5:2 C5 Ab4+F5:2 C5 Ab4:2", march(oF, cFm, oC), "Fm"),                                           # 5
    ("F5 Eb5 D5 C5 Bb4 A4 C5 Eb5", f"{oF}:2 {oEb}:2 {oC}:2 {oA}:2", "F7"),                         # 6
    ("F4+D5:2 Bb4 F4+D5:2 Bb4 Ab4:2", march(oBb, cBb7, oF), "Bb7"),                                      # 7
    ("Ab4+Bb4+D5:4 r Bb5 C6 D6", f"{oBbLow}:2 {cBb7}:2 {oBbLow}:2 r:2", "Bb7"),                    # 8
    ("Eb5+Eb6:2 C6 Eb5+Eb6:2 C6 Ab5:2", march(oAb, cAb, oEb), "Ab"),                               # 9
    ("A5 C6:2 D6 Eb5+Eb6:2 C6:2", march(oA, cAdim, oEb), "Adim7"),                                # 10
    ("G5+G6:2 Eb6 G5+G6:2 Eb6 Bb5:2", march(oBbLow, cEb, oBb), "Eb/Bb"),                           # 11
    ("G5 Bb5:2 C6 E5+E6:2 C6:2", f"{oC}:2 {cC7}:2 {oG}:2 {oE}:2", "C7"),                           # 12
    ("A5 C6:2 Eb6 F5+F6 Eb6:2 C6", march(oF, cF7, oC), "F7"),                                      # 13
    ("D6 C6 Bb5 Ab5 F5 G5 Ab5 Bb5", f"{oBbLow}:2 {cBb7}:2 {oF}:2 {oD}:2", "Bb7"),                  # 14
    ("G5 Ab5 Bb5 G5+G6:2 F6 Eb6 Bb5", march(oEb, cEb, oBb), "Eb"),                                 # 15
    ("G5+Bb5+Eb6:2 Ab5+Bb5+D6:2 G5+Bb5+Eb6:4", "Eb2+Eb3:2 Bb1+Bb2:2 Eb1+Eb2:4", END_H),            # 16
]

STRAINS = {"Intro": INTRO, "A": STRAIN_A, "B": STRAIN_B, "C": STRAIN_C, "D": STRAIN_D}
ORDER = ["Intro", "A", "A", "B", "B", "A", "C", "C", "D", "D"]      # as performed
KEY_OF = {"Intro": "Eb", "A": "Eb", "B": "Eb", "C": "Ab", "D": "Eb"}


class RagScore(Score):
    """2/4 with the sixteenth as unit: beats fall on 0 and 4."""
    beat = 4.0

    def assign_roles(self):
        for b in self.bars:
            for n in b.notes:
                if n.hand == "R":
                    n.role = "melody" if n.chord_rank == n.chord_size - 1 else "rh_inner"
                else:
                    ps = sorted(m.pitch for m in b.notes if m.hand == "L" and abs(m.s - n.s) < 1e-6)
                    octave = len(ps) == 2 and ps[1] - ps[0] == 12
                    n.role = "bass" if (octave or len(ps) == 1) else "acc"


def build(order=None, written=False):
    """written=True: each strain once (for the engraving and the style statistics);
    otherwise the piece as performed, repeats unfolded.  Every bar is tagged with
    (strain, bar-in-strain, pass)."""
    sc = RagScore(TITLE, bar_len=8.0)
    sc.tags = []
    seq = ["Intro", "A", "B", "C", "D"] if written else (order or ORDER)
    seen = {}
    for name in seq:
        seen[name] = seen.get(name, 0) + 1
        for i, (rh, lh, harm) in enumerate(STRAINS[name]):
            sc.bar(rh, lh, harm)
            sc.tags.append((name, i + 1, seen[name]))
    return sc


# =============================================================== the performer's plan
PLAN = dict(
    bpm=92.0,                      # quarter notes per minute: "Not fast" / slow march tempo
    # (strain, pass) -> tempo factor, dynamic level 0..1, pedal style
    sections={
        ("Intro", 1): dict(tempo=0.975, level=0.72, pedal="none"),
        ("A", 1): dict(tempo=1.00, level=0.60, pedal="dab"),
        ("A", 2): dict(tempo=1.00, level=0.52, pedal="dab"),
        ("B", 1): dict(tempo=1.015, level=0.70, pedal="dab"),
        ("B", 2): dict(tempo=1.02, level=0.77, pedal="dab"),
        ("A", 3): dict(tempo=1.00, level=0.58, pedal="dab"),
        ("C", 1): dict(tempo=0.965, level=0.37, pedal="legato"),
        ("C", 2): dict(tempo=0.975, level=0.50, pedal="legato"),
        ("D", 1): dict(tempo=1.02, level=0.70, pedal="dab"),
        ("D", 2): dict(tempo=1.03, level=0.82, pedal="dab"),
    },
    # shape of the dynamics inside a 16-bar strain (added to the level): four phrases,
    # the last one carrying the high point and a firm cadence
    strain_shape=[0.00, 0.02, 0.01, 0.00, 0.02, 0.04, 0.02, -0.02,
                  0.00, 0.03, 0.05, 0.01, 0.09, 0.08, 0.06, 0.04],
    breath_between_strains=0.07,   # seconds
    breath_before_trio=0.16,
    final_rit=[1.0, 0.96, 0.88, 0.72],   # tempo factor over the last four beats
    final_hold=1.6,                # extra seconds on the last chord
)
