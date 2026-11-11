"""The Last Lamp: an original nocturne in F minor (2026).

Authored score and interpretation, revised for advanced concert difficulty.
The formal framework below is developed in concert.py. No material from ../out is used.
Durations are eighth notes; the inherited Score/Performance tools use 12/8.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "nocturne"))
sys.path.insert(0, str(ROOT / "engine"))
from score import Score

TITLE = "The Last Lamp"
STEM = "the_last_lamp"

# Six-note waves, explicitly voiced. Harmonic inversions carry the bass line.
VOICINGS = {
    "Fm": "F2 C3 F3 Ab3 C4 Ab3", "Fm/Ab": "Ab2 C3 F3 Ab3 C4 F3",
    "Fm/C": "C3 F3 Ab3 C4 Ab3 F3", "F": "F2 C3 F3 A3 C4 A3",
    "F/A": "A2 C3 F3 A3 C4 F3", "F/C": "C3 F3 A3 C4 A3 F3",
    "F7": "F2 C3 Eb3 A3 C4 A3", "F7/A": "A2 C3 Eb3 F3 C4 A3",
    "F7/C": "C3 Eb3 F3 A3 C4 F3",
    "Bbm": "Bb2 F3 Bb3 Db4 Bb3 F3", "Bbm7": "Bb2 F3 Ab3 Db4 F4 Db4",
    "Bbm/Db": "Db3 F3 Bb3 Db4 F4 Bb3", "Bbm7/F": "F2 Bb2 Db3 Ab3 Bb3 Db3",
    "Bbm7/Db": "Db3 F3 Ab3 Bb3 Db4 Ab3",
    "Bbm/F": "F2 Bb2 Db3 F3 Bb3 Db3",
    "C7": "C2 G2 C3 E3 Bb3 E3", "C7/G": "G2 C3 E3 G3 Bb3 E3",
    "C7/E": "E2 G2 C3 E3 Bb3 G3",
    "C7b9": "C2 G2 Db3 E3 Bb3 E3",
    "Db": "Db2 Ab2 Db3 F3 Ab3 F3", "Db/F": "F2 Ab2 Db3 F3 Ab3 Db3",
    "DbGer6": "Db2 Ab2 B2 F3 Ab3 F3",
    "Ddim7": "D2 Ab2 B2 F3 Ab3 F3",
    "Ab": "Ab2 Eb3 Ab3 C4 Eb4 C4", "Ab/C": "C3 Eb3 Ab3 C4 Eb4 Ab3",
    "Ab/Eb": "Eb2 Ab2 C3 Eb3 Ab3 C3", "Ab7/C": "C3 Eb3 Gb3 Ab3 Eb4 Gb3",
    "Eb7": "Eb2 Bb2 Eb3 G3 Db4 G3", "Eb7/G": "G2 Bb2 Db3 Eb3 Bb3 Db3",
    "Eb7/Bb": "Bb2 Eb3 G3 Bb3 Db4 G3", "Eb7/Db": "Db3 Eb3 G3 Bb3 Db4 G3",
    "Ebm7": "Eb2 Bb2 Db3 Gb3 Bb3 Gb3",
    "Gb": "Gb2 Db3 Gb3 Bb3 Db4 Bb3", "Gb/Bb": "Bb2 Db3 Gb3 Bb3 Db4 Gb3",
    "Gdim7/Bb": "Bb2 Db3 E3 G3 Bb3 E3",
    "Gm7/Bb": "Bb2 D3 F3 G3 Bb3 D3", "Dm": "D2 A2 D3 F3 A3 F3",
    "Bb": "Bb2 F3 Bb3 D4 F4 D4",
    "Bb/D": "D3 F3 Bb3 D4 F4 Bb3",
}


def wave(chord, variation=0):
    p = VOICINGS[chord].split()
    if variation % 4 == 1:
        p = [p[i] for i in (0, 1, 3, 4, 3, 2)]
    elif variation % 4 == 2:
        p = [p[i] for i in (0, 2, 3, 4, 3, 1)]
    return " ".join(p)


def build():
    sc = Score(f"{TITLE} - Nocturne in F minor")

    def bar(rh, harmony, inner=None, lh=None, ped=None):
        n = len(sc.bars) + 1
        chords = harmony.split()
        if lh is None:
            c0, c1 = (chords * 2)[:2] if len(chords) == 1 else chords
            lh = wave(c0, n // 3) + " " + wave(c1, n // 3 + 1)
        sc.bar(rh, lh, harmony, rh2=inner, ped=ped,
               texture="duet" if inner else "")

    # 1-2. A room before the singer enters. The pickup belongs to the theme.
    bar("r:12", "Fm")
    bar("r:9 C5:2 Db5:1", "Fm C7b9")

    # 3-10. A falling sigh, then a leap to the upper dominant. Half cadence.
    bar("Ab5:3 Ab5:2 G5:1 C6:3 C6:2 Ab5:1", "Fm")
    bar("G5:3 F5:3 E5:3 Db5:2 Bb4:1", "Bbm/Db C7b9")
    bar("C5:3 C5:1 Ab4:2 F5:3 A5:2 A5:1", "Fm F7")
    bar("Bb5:3 Bb5:2 Ab5:1 F5:3 Eb5:2 Db5:1", "Bbm/Db Eb7/Db")
    bar("C5:3 Eb5:2 C5:1 Ab5:3 G5:2 F5:1", "Ab/C Db")
    bar("E5:3 G5:2 G5:1 Bb5:3 A5:1 G5:1 E5:1", "C7")
    bar("Ab5:3 F5:3 Db5:2 C5:1 B4:1 C5:2", "Db C7b9")
    bar("G4:3 E5:2 G5:1 G5:3 r:3", "C7")

    # 11-18. Answer, reaching higher; Neapolitan colour before the minor close.
    bar("Ab5:3 Ab5:2 G5:1 C6:3 Eb6:2 C6:1", "Fm Ab/Eb")
    bar("C6:3 C6:2 Ab5:1 G5:3 (Ab5)F5:2 Eb5:1", "Ab/C Eb7/Bb")
    bar("Db5:3 Db5:2 F5:1 Bb5:3 Ab5:2 F5:1", "Bbm/Db Bbm7")
    bar("A5:3 C6:1 Bb5:1 A5:1 G5:3 Eb5:2 F5:1", "F7/C Eb7/G")
    bar("E5:3 G5:2 E5:1 C6:3 Ab5:2 G5:1", "C7 Fm/C")
    bar("Gb5:3 Gb5:2 F5:1 E5:3 Db5:2 Bb4:1", "Gb/Bb Gdim7/Bb")
    bar("C5:3 (Db5)C5:2 Bb4:1 E5:3 E5:2 G5:1", "C7")
    bar("F5:6 r:3 Eb5:1 F5:1 G5:1", "Fm Eb7")

    # 19-26. Relative-major duet. The second voice has its own rhythm.
    bar("Ab5:3 Ab5:2 Bb5:1 C6:3 Eb6:2 C6:1", "Ab/C Eb7/G", "C5:6 Eb5:3 G5:3")
    bar("Bb5:3 G5:2 Eb5:1 C6:3 Bb5:2 Ab5:1", "Eb7/G Ab", "Eb5:3 Db5:2 Bb4:1 Eb5:3 C5:3")
    bar("C5:3 Eb5:3 Ab5:3 G5:2 F5:1", "Ab/C Db", "Ab4:6 F5:3 Eb5:2 Db5:1")
    bar("Eb5:3 G5:3 Bb5:4 Bb5:1 G5:1", "Eb7/Bb Eb7", "Bb4:6 Db5:6")
    bar("F5:3 F5:1 G5:1 Ab5:1 Db6:3 C6:2 Bb5:1", "Db F7/A", "Db5:6 F5:6")
    bar("A5:3 A5:2 F5:1 Bb5:3 Db6:2 Bb5:1", "F7/A Bbm7/Db", "C5:6 Db5:6")
    bar("Ab5:3 C6:2 Ab5:1 G5:3 Eb5:2 Bb4:1", "Ab/C Eb7", "Eb5:3 Db5:3 Bb4:3 G4:3")
    bar("Ab4:6 r:3 C5:1 Db5:1 Eb5:1", "Ab Ab7/C")

    # 27-34. The duet opens into a more urgent, sequential solo.
    bar("F5:3 F5:2 Db5:1 Ab5:3 C6:2 Ab5:1", "Db Ab7/C", "Ab4:6 Eb5:6")
    bar("Eb5:3 Db5:2 C5:1 Bb4:3 Db5:2 Eb5:1", "Ab7/C Bbm", "Gb4:6 F4:6")
    bar("F5:3 Ab5:3 Db6:3 C6:2 Bb5:1", "Db/F Gb")
    bar("A5:3 C6:2 A5:1 G5:3 E5:2 E5:1", "F7/A C7/E")
    bar("F5:3 Ab5:2 F5:1 Db6:3 Ab5:2 Ab5:1", "Bbm7/F Db/F")
    bar("C5:2 Db5:1 E5:3 G5:2 Ab5:1 Bb5:3", "C7/E C7b9")
    bar("Bb5:3 Db6:2 C6:1 Bb5:3 Ab5:2 Gb5:1", "Gb/Bb Gdim7/Bb")
    bar("F5:3 Ab5:2 F5:1 C6:3 C6:2 Db6:1", "Fm/C C7b9")

    # 35-38. Chromatic approach; the augmented sixth resolves through i6/4.
    bar("Ab4+Ab5:3 Ab5:1 Bb5:1 C6:1 B4+D5+B5:3 D6:2 C6:1", "Db Ddim7")
    bar("Db5+Gb5+Db6:3 C6:2 Bb5:1 C5+Eb5+G5+C6:3 Eb6:2 E6:1", "Ebm7 Eb7/G")
    bar("Ab5+B5+F6:3! Eb6:2 Db6:1 Ab5+C6:3 Bb5:2 Ab5:1", "DbGer6 Fm/C",
        lh=wave("DbGer6") + " C2 Ab2 C3 F3 Ab3 F3")
    bar("E5+G5:3 F5:2 E5:1 Bb4+Db5:3 C5:3", "C7b9")

    # 39-40. A measured cadenza over one sustained dominant, then a breath.
    bar("tr(C6 Db6):3 {C6 Bb5 Ab5 G5 F5 E5 F5 G5 Ab5 Bb5 B5 C6 Db6 C6 Bb5 Ab5 G5 F5 E5 Db5 C5 Bb4 Ab4 G4 F4 E4 G4 Bb4 C5 Db5 E5 G5}:9",
        "C7b9", lh="C3+G3+Bb3:12", ped=[0])
    bar("Db5:3 C5:3 r:6", "C7b9", lh="C3+E3+Bb3:6 r:6", ped=[0, 6])

    # 41-48. Same melodic skeleton; the ornamentation now remembers the storm.
    bar("Ab5:3 {Ab5 Bb5 Ab5 G5 F5 G5}:3 C6:3 C6:2 Ab5:1", "Fm")
    bar("G5:3 F5:3 E5:2 {F5 E5 Db5 C5 Bb4 Db5}:4", "Bbm/Db C7b9")
    bar("C5:3 C5:1 Ab4:2 F5:3 {G5 A5 Bb5 A5 C6 A5}:3", "Fm F7")
    bar("Bb5:3 {Bb5 C6 Bb5 Ab5 G5 Ab5}:3 F5:3 Eb5:2 Db5:1", "Bbm/Db Eb7/Db")
    bar("C5:3 Eb5:2 C5:1 Ab5:2 {Bb5 Ab5 G5 F5 E5 F5}:4", "Ab/C Db")
    bar("E5:3 {F5 G5 Ab5 G5 F5 E5}:3 G5:3 tr(E5 F5):2 Db5:1", "C7b9")
    bar("C5:3 Ab4:3 Bb4:2 Ab4:1 G4:1 F4:2", "Fm/Ab Bbm/F")
    bar("E4:3 G4:2 Bb4:1 C5:3 F5:3", "C7 Fm")

    # 49-52. The Neapolitan returns as an echo, without a second climax.
    bar("Ab5:6 G5:3 F5:3", "Db/F Fm/C")
    bar("Gb5:3 Gb5:2 F5:1 E5:3 Db5:2 Bb4:1", "Gb/Bb Gdim7/Bb")
    bar("E5:3 G5:2 F5:1 E5:3 Db5:3", "C7b9")
    bar("C5:6 r:6", "C7", lh="C3+E3+Bb3:6 r:6", ped=[0, 6])

    # 53-60. The theme in the parallel major; a minor plagal shadow survives.
    bar("A5:3 A5:2 G5:1 C6:3 C6:2 A5:1", "F")
    bar("G5:3 F5:3 E5:3 C5:3", "Gm7/Bb C7")
    bar("D5:3 F5:2 D5:1 Bb5:3 A5:2 F5:1", "Dm Bb/D")
    bar("A4:3 C5:3 F5:3 E5:2 D5:1", "F/A Bbm/Db")
    bar("Db5:3 C5:3 Bb4:3 Ab4:3", "Bbm7/Db")
    bar("A4:3 G4:2 F4:1 E4:3 C5:3", "F/C C7")
    bar("F5:3 {E5 F5 G5 A5 C6 Bb5 A5 G5 F5 E5 F5}:6 C5:3", "F",
        lh="F2:3 C3:3 A3:3 C4:3", ped=[0])
    bar("A4+C5+F5:12", "F", lh="F2+C3+F3:12", ped=[0])
    assert len(sc.bars) == 60
    from concert import rewrite
    return rewrite(sc)


# Tempi are dotted quarters per minute. Structural tension, not a random walk.
TEMPO = [(1, 0, 46), (2, 6, 49), (3, 0, 49), (5, 0, 51), (7, 0, 49),
         (9, 0, 46), (10, 6, 40), (11, 0, 50), (13, 0, 51), (15, 0, 48),
         (16, 0, 44), (18, 0, 40), (18, 9, 49), (19, 0, 53), (21, 0, 55),
         (23, 0, 54), (25, 0, 50), (26, 0, 45), (27, 0, 58), (29, 0, 62),
         (31, 0, 65), (33, 0, 67), (35, 0, 62), (36, 6, 54), (37, 0, 43),
         (38, 0, 43), (38, 9, 36), (39, 0, 39), (39, 3, 52), (39, 9, 42),
         (40, 0, 40), (41, 0, 50), (43, 0, 52), (45, 0, 50), (47, 0, 46),
         (48, 6, 40), (49, 0, 47), (50, 0, 44), (51, 0, 41), (52, 0, 36),
         (53, 0, 47), (55, 0, 47), (57, 0, 43), (58, 0, 40), (59, 0, 38),
         (59, 9, 32), (60, 0, 28), (60, 12, 23)]

DYNAMICS = [(1, 0, .12), (3, 0, .25), (3, 6, .34), (4, 9, .23), (5, 6, .32),
            (6, 0, .41), (7, 0, .30), (9, 0, .24), (10, 6, .16),
            (11, 0, .30), (12, 0, .46), (13, 0, .32), (15, 6, .44),
            (16, 0, .36), (18, 0, .18), (19, 0, .22), (21, 6, .35),
            (22, 9, .24), (23, 0, .32), (24, 6, .44), (26, 0, .18),
            (27, 0, .29), (29, 0, .43), (31, 0, .48), (33, 0, .64),
            (35, 0, .68), (36, 6, .78), (37, 0, .90), (38, 0, .59),
            (38, 9, .32), (39, 0, .38), (39, 6, .30), (40, 0, .15),
            (41, 0, .18), (41, 6, .29), (43, 0, .25), (44, 0, .35),
            (45, 0, .24), (47, 0, .21), (48, 6, .14), (49, 0, .24),
            (50, 0, .27), (51, 0, .20), (52, 0, .11), (53, 0, .22),
            (54, 6, .24), (55, 0, .19), (57, 0, .16), (59, 0, .12),
            (60, 0, .07), (60, 12, .04)]

PHRASES = [((3, 0), (7, 0)), ((7, 0), (10, 9)), ((11, 0), (15, 0)),
           ((15, 0), (18, 6)), ((19, 0), (23, 0)), ((23, 0), (26, 6)),
           ((27, 0), (31, 0)), ((31, 0), (35, 0)), ((35, 0), (39, 0)),
           ((41, 0), (45, 0)), ((45, 0), (49, 0)), ((49, 0), (52, 6)),
           ((53, 0), (57, 0)), ((57, 0), (60, 12))]
BREATHS = [(3, 0, .08), (6, 12, .06), (10, 9, .18), (11, 0, .10), (18, 6, .16),
           (19, 0, .12), (26, 6, .16), (35, 0, .08), (37, 0, .22),
           (39, 0, .28), (40, 6, .42), (41, 0, .12), (48, 9, .16),
           (52, 6, .28), (53, 0, .10), (60, 12, 1.20)]
BASS_FIRST = [(3, 0, 16), (19, 0, 18), (37, 0, 24), (41, 0, 20), (53, 0, 15)]
ROLLS = {(39, 0): 15, (52, 0): 12, (60, 0): 16}
UNA_CORDA = [((1, 0), (3, 0)), ((18, 0), (23, 0)), ((40, 0), (43, 0)),
             ((49, 0), (60, 12))]
FLUTTER = [(39, p, .43) for p in (3, 6, 9)]

# Finger rests with continuing resonance. The pedal clears on the next attack.
PEDAL_BREATHS = [((10, 9), (11, 0)), ((18, 6), (18, 9)),
                ((26, 6), (26, 9)), ((40, 6), (41, 0)),
                ((52, 6), (53, 0))]
