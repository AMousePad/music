"""Authored concert revision: independent voices, double notes and 7/11/13 tuplets.

The quiet theme and formal cadences remain the structural framework. These are
explicitly composed replacements, not random ornament generation.
"""
from score import Score

# Twelve sixteenths per half-bar. The register is chosen for each inversion,
# keeping the two hands apart even when the right hand has a low inner voice.
ARPS = {
    "Fm": "F2 C3 F3 Ab3 C4 F4 C4 Ab3 F3 C3 Ab2 C3",
    "Fm/Ab": "Ab2 C3 F3 Ab3 C4 F4 C4 Ab3 F3 C3 Ab2 C3",
    "Fm/C": "C2 Ab2 C3 F3 Ab3 C4 F4 C4 Ab3 F3 C3 Ab2",
    "F7": "F2 C3 Eb3 A3 C4 Eb4 C4 A3 F3 Eb3 C3 A2",
    "F7/A": "A2 C3 Eb3 F3 A3 C4 Eb4 C4 A3 F3 Eb3 C3",
    "F7/C": "C2 A2 C3 Eb3 F3 A3 C4 A3 F3 Eb3 C3 A2",
    "Bbm": "Bb1 F2 Bb2 Db3 F3 Bb3 F3 Db3 Bb2 F2 Db2 F2",
    "Bbm7": "Bb1 F2 Ab2 Db3 F3 Ab3 F3 Db3 Bb2 Ab2 F2 Db2",
    "Bbm/Db": "Db2 Bb2 Db3 F3 Bb3 Db4 F4 Db4 Bb3 F3 Db3 Bb2",
    "Bbm7/F": "F2 Bb2 Db3 F3 Ab3 Db4 F4 Db4 Ab3 F3 Db3 Bb2",
    "Db": "Db2 Ab2 Db3 F3 Ab3 Db4 F4 Db4 Ab3 F3 Db3 Ab2",
    "Db/F": "F2 Ab2 Db3 F3 Ab3 Db4 F4 Db4 Ab3 F3 Db3 Ab2",
    "Gb": "Gb2 Db3 Gb3 Bb3 Db4 Gb4 Db4 Bb3 Gb3 Db3 Bb2 Db3",
    "Gb/Bb": "Bb1 Gb2 Bb2 Db3 Gb3 Bb3 Db4 Bb3 Gb3 Db3 Bb2 Gb2",
    "Ab/C": "C2 Ab2 C3 Eb3 Ab3 C4 Eb4 C4 Ab3 Eb3 C3 Ab2",
    "Ab/Eb": "Eb2 Ab2 C3 Eb3 Ab3 C4 Eb4 C4 Ab3 Eb3 C3 Ab2",
    "Ab7/C": "C2 Ab2 C3 Eb3 Gb3 Ab3 C4 Ab3 Gb3 Eb3 C3 Ab2",
    "Eb7/G": "G2 Bb2 Db3 Eb3 G3 Bb3 Db4 Bb3 G3 Eb3 Db3 Bb2",
    "Eb7/Bb": "Bb1 G2 Bb2 Db3 Eb3 G3 Bb3 G3 Eb3 Db3 Bb2 G2",
    "Eb7/Db": "Db2 Bb2 Db3 Eb3 G3 Bb3 Db4 Bb3 G3 Eb3 Db3 Bb2",
    "Ebm7": "Eb2 Bb2 Db3 Gb3 Bb3 Db4 Gb4 Db4 Bb3 Gb3 Db3 Bb2",
    "C7": "C2 G2 C3 E3 G3 Bb3 C4 Bb3 G3 E3 C3 G2",
    "C7/E": "E2 G2 Bb2 C3 E3 G3 C4 G3 E3 C3 Bb2 G2",
    "C7b9": "C2 G2 Bb2 Db3 E3 G3 Bb3 G3 E3 Db3 Bb2 G2",
    "Gdim7/Bb": "Bb1 G2 Bb2 Db3 E3 G3 Bb3 G3 E3 Db3 Bb2 G2",
    "Ddim7": "D2 Ab2 B2 D3 F3 Ab3 B3 Ab3 F3 D3 B2 Ab2",
    "DbGer6": "Db2 Ab2 B2 Db3 F3 Ab3 B3 Ab3 F3 Db3 B2 Ab2",
}


def fast_half(chord):
    return " ".join(p + ":0.5" for p in ARPS[chord].split())


# Whole-bar right-hand replacements; the durations always total 12 eighths.
RIGHT = {
    3: "Ab5:3 Ab5:2 G5:1 C6:3 {C6 Db6 C6 Bb5 Ab5 G5 Ab5}:3",
    4: "G5:3 F5:3 E5:3 {Db5 E5 F5 E5 Db5 C5 Bb4}:3",
    5: "C5:3 C5:1 Ab4:2 F5:3 {A5 Bb5 A5 G5 F5 E5 F5 G5 A5}:3",
    7: "C5:3 Eb5:2 C5:1 Ab5:3 {G5 Ab5 G5 F5}:3",
    8: "E5:3 G5:2 G5:1 Bb5:3 {A5 G5 F5 E5 G5 F5 E5}:3",
    10: "G4:3 {Bb4 C5 E5 G5 Bb5 A5 G5 E5 G5}:3 G5:3 r:3",
    11: "Ab4+Ab5:3 Ab5:2 G5:1 C5+C6:3 {Eb6 Db6 C6 Bb5 Ab5 G5 Ab5 C6}:3",
    12: "Eb5+C6:3 Eb5+C6:2 C5+Ab5:1 Bb4+G5:3 (Ab5)Ab4+F5:2 G4+Eb5:1",
    13: "Db5:3 {Db5 Eb5 Db5 C5 Bb4 C5 Db5 F5}:3 Bb5:3 {Ab5 Bb5 Ab5 Gb5 F5 Eb5 Db5 F5}:3",
    14: "C5+A5:3 Eb5+C6:1 D5+Bb5:1 C5+A5:1 Bb4+G5:3 G4+Eb5:2 Ab4+F5:1",
    15: "E5:3 {G5 Ab5 G5 F5 E5 G5}:3 C6:3 {Ab5 Bb5 Ab5 G5 F5 G5}:3",
    16: "Gb5:3 {Gb5 Ab5 Gb5 F5 Eb5 Db5 C5 Db5}:3 E5:3 {Db5 E5 Db5 C5 Bb4 Ab4 G4 Bb4}:3",
    17: "C5:3 {Db5 C5 Bb4 G4 E4 G4 Bb4 C5 Db5 E5 F5 E5}:3 E5:3 {E5 F5 E5 D5 C5 Bb4 G4 E5}:3",
    27: "Db5+F5:3 Eb5+Gb5:0.5 F5+Ab5:0.5 Eb5+Gb5:0.5 Db5+F5:0.5 C5+Eb5:0.5 Bb4+Db5:0.5 Eb5+Ab5:3 Gb5+Bb5:1 F5+Ab5:1 Eb5+Gb5:1",
    28: "C5+Eb5:3 Bb4+Db5:2 Ab4+C5:1 F4+Bb4:3 Bb4+Db5:1 C5+Eb5:1 Db5+F5:1",
    29: "F5:3 Ab5:3 Db6:3 {C6 Db6 C6 Bb5 Ab5 Gb5 F5 Ab5}:3",
    30: "C5+A5:3 Eb5+C6:2 C5+A5:1 Bb4+G5:3 G4+E5:2 G4+E5:1",
    31: "Db5+F5:3 F5+Ab5:2 Db5+F5:1 F5+Db6:3 C5+Ab5:2 C5+Ab5:1",
    32: "E4+C5:2 F4+Db5:1 G4+E5:3 E5+G5:2 F5+Ab5:1 G5+Bb5:3",
    33: "Gb5+Bb5:3 Bb5+Db6:2 Ab5+C6:1 G5+Bb5:3 F5+Ab5:2 E5+Gb5:1",
    34: "C5+F5:3 Eb5+Ab5:2 C5+F5:1 E5+C6:3 E5+C6:2 E5+Db6:0.5 E5+C6:0.5",
    35: "Ab4+Ab5:3 F5+Ab5:0.5 G5+Bb5:0.5 Ab5+C6:1 F5+Ab5:1 B4+D5+B5:3 F5+D6:1.5 E5+C6:0.5 D5+B5:1",
    36: "Db5+Gb5+Db6:2.5 Db5+Gb5+Db6:0.5 C5+Eb5+C6:2 Bb4+Db5+Bb5:1 C5+Eb5+G5+C6:3 G5+Eb6:2 G5+E6:1",
    37: "B5+F6:3! Ab5+Eb6:1.5 F5+Db6:0.5 Ab5+B5:1 F5+Ab5+C6:3 Ab5+Bb5:2 F5+Ab5:1",
    38: "E5+G5:3 Db5+F5:2 C5+E5:1 Bb4+Db5:3 G4+C5:3",
    39: "tr(C6 Db6):3 {C6 Db6 C6 Bb5 G5 E5 Db5 E5 G5 Bb5 Db6 E6 G6 F6 E6 Db6 C6 Bb5 Ab5 G5 F5 E5 Db5 C5 Bb4 G4 E4 G4 Bb4 Db5 E5 G5 Bb5 Db6 C6 Bb5 Ab5 G5 F5 E5 Db5 C5 Bb4 G4 E4 G4 Bb4 C5 Db5 E5 G5 C6}:9",
    41: "Ab5:3 Ab5:2 G5:1 C6:3 {C6 Db6 C6 Bb5 Ab5 G5 Ab5 C6 Bb5 G5 Ab5}:3",
    42: "G5:3 F5:3 E5:3 {Db5 E5 G5 Bb5 Db6 C6 Bb5 G5 E5 Db5 C5 Bb4 C5}:3",
    43: "C5:3 C5:1 Ab4:2 F5:3 {A5 Bb5 A5 G5 F5 E5 F5 G5 A5 C6 Bb5 A5 F5}:3",
    44: "Bb5:3 Bb5:2 Ab5:1 F5:3 {Eb5 F5 Eb5 Db5 C5 Db5 Eb5 F5 Eb5 Db5 C5 Bb4 Db5}:3",
    45: "C5:3 Eb5:2 C5:1 Ab5:3 {G5 Ab5 Bb5 Ab5 G5 F5 E5 F5 G5 Ab5 G5 F5 Db5}:3",
    46: "E5:3 {G5 Ab5 G5 F5 E5 G5 Bb5 Ab5 G5 E5 G5}:3 G5:3 tr(E5 F5):2 Db5:1",
}

INNER = {
    3: "C5:3 Eb5:3 F5:3 E5:1 F5:1 C5:1",
    4: "Db5:3 Bb4:3 Bb4:3 r:3",
    5: "r:6 C5:3 Eb5:3",
    6: "Db5:6 Bb4:6",
    7: "r:6 F5:3 Db5:3",
    8: "Bb4:3 C5:3 E5:3 r:3",
    19: "C5:2 Eb5:1 F5:2~ F5:1 Eb5:2 G5:1 Bb5:2 G5:1",
    20: "Eb5:2 Db5:1 Bb4:2 G4:1 Eb5:2 C5:1 Eb5:2 C5:1",
    21: "Ab4:3 Bb4:2 C5:1 F5:3 Eb5:2 Db5:1",
    22: "Bb4:2 Db5:1 Eb5:2 Db5:1 F5:3 Eb5:2 Db5:1",
    23: "Db5:3 Eb5:2 F5:1 F5:2 Eb5:1 C5:3",
    24: "C5:2 Eb5:1 Eb5:3 Db5:3 F5:2 Db5:1",
    25: "Eb5:3 Db5:2 C5:1 Bb4:3 G4:3",
    27: None, 28: None, 29: "r:6 Bb5:3 r:3",
    41: "C5:1 Eb5:0.5 F5:0.5 Eb5:0.5 Db5:0.5 C5:1 Db5:0.5 Eb5:0.5 F5:1 F5:1 E5:0.5 F5:0.5 Ab5:1 r:3",
    42: "Db5:3 Bb4:3 r:6",
    43: "r:6 C5:3 r:3",
    44: "Db5:3 F5:3 Bb4:3 r:3",
    45: "Ab4:6 F5:3 r:3",
    46: "Bb4:3 r:9",
    53: "C5:3 D5:2 E5:1 F5:3 E5:1 D5:1 C5:1",
    54: "D5:3 Bb4:3 G4:3 Bb4:3",
    55: "A4:6 D5:3 F5:2 D5:1",
    56: "F4:3 A4:3 Db5:3 C5:2 Bb4:1",
    57: "Ab4:3 F4:3 Db4:3 F4:3",
    59: "C5:3 r:9",
}


def rewrite(framework):
    out = Score(framework.title)
    fast_bars = set(range(11, 18)) | set(range(27, 39)) | set(range(41, 47))
    for b in framework.bars:
        n = b.number
        rh = RIGHT.get(n, b.raw["rh"])
        inner = INNER.get(n, b.raw["rh2"])
        lh = b.raw["lh"]
        harmony_changes = [(0., "Db"), (6., "Gb")] if n == 29 else b.harmony
        if n in fast_bars:
            chords = [sym for _, sym in harmony_changes]
            if len(chords) == 1:
                chords *= 2
            lh = fast_half(chords[0]) + " " + fast_half(chords[1])
        if n == 37:
            # Both augmented-sixth tendencies resolve by semitone: Db -> C,
            # B -> C. C2 is essential here; an octave transfer would obscure it.
            lh = fast_half("DbGer6") + " " + fast_half("Fm/C")
        if n == 38:
            lh = fast_half("C7b9") + " C3+E3+Bb3:6"
        if n == 40:
            lh = "{C2 G2 C3 E3 G3 Bb3 Db4 E4 G4 Bb4 G4 E4 Db4 Bb3 G3 E3 C3 G2 C2}:6 r:6"
        if n == 10:
            lh = "C2 G2 C3 E3 Bb3 E3 C2 E3 Bb3 r:3"
        if n == 18:
            lh = "F2:3 C3+Ab3:3 r:3 Eb3 G3 Bb3"
        if n == 26:
            lh = "Ab2 Eb3 Ab3 C4 Eb4 C4 r:3 C3 Eb3 Gb3"
        if n == 48:
            lh = "C2 G2 C3 E3 G3 Bb3 F2:3 C3+Ab3:3"
        harmony = " ".join(f"{sym}@{pos:g}" for pos, sym in harmony_changes)
        # Rests release the fingers, not all the piano's resonance. Retain the
        # last harmony across each breath; the next attack gets the normal
        # syncopated pedal change. Never clear an otherwise silent rest.
        pedal = {
            10: [0, 3, 6], 18: [0, 9], 26: [0, 9],
            40: [0], 52: [0],
        }.get(n, b.pedal)
        out.bar(rh, lh, harmony, rh2=inner, ped=pedal,
                texture="duet" if inner else "")
    return out
