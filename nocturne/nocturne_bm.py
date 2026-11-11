"""Nocturne in B minor  -  Lento sostenuto, 12/8

An original composition in the manner of Chopin's nocturnes (not a quotation or
arrangement of any of them).  Everything here is the *text*: notes, harmony, phrase
structure and the performer's plan (tempo, dynamics, pedal).  perform.py turns the
plan into a performance.

Form
    bar  1        introduction (left hand alone)
    A    2-17     a (2-5) half cadence | a' (6-9) cadence in D | b (10-13) rising
                  chromatic bass D-D#-E-E#-F# to the dominant | a'' (14-17) ornamented,
                  perfect cadence in B minor
    B   18-33     G major, sotto voce duet in thirds and sixths (18-25);
                  the duet theme is driven up over a chromatic bass G-G#-A-A#-B-C-C#-D-D#-E
                  (26-31) to the climax: German sixth with the raised 4th in the bass, the outer
                  voices G/E# closing by semitones onto the octave F# (32) -> cadenza (33)
    A'  34-40     theme with fioriture; iv turns into the Neapolitan sixth over a held bass E
                  (38-39, the 5-6 motion B->C) -> V7 (40)
    Coda 41-47    tonic pedal; the theme remembered in B minor, then answered in B major;
                  plagal minor-subdominant sighs; closing arpeggio

Motivic threads
    x  three rising eighths into a long appoggiatura            (E F# B | A-G)
    y  the diminished third closing in on a goal note:  G - E# - F#  (bars 5, 13, 31-32, 37)
       and, at the very end of the argument, around the tonic:  C - A# - B  (bars 39-41)
    z  minor ninth over the dominant falling to the root        (bars 3, 10, 11, 13, 26, 27)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from score import Score

TITLE = "Nocturne in B minor"


def build():
    sc = Score(TITLE)
    B = sc.bar

    # waves for the left hand (six eighths each): root - 5th - 10th - 12th - 15th - 12th
    Bm = "B1 F#2 D3 F#3 B3 F#3"
    Bm2 = "B1 F#2 D3 F#3 D4 F#3"
    iio = "B1 G2 E3 G3 C#4 G3"          # C# half-diminished over the tonic pedal
    V65 = "A#1 F#2 E3 F#3 C#4 F#3"
    VI = "G1 D2 B2 D3 G3 D3"
    HC = "G1 E3 B3 G2 B2 G3 F#1 C#2 A#2 C#3 F#3 C#3"   # iv6 - It+6 - V

    # ---------------------------------------------------------------- introduction
    B("r:12", f"{Bm} {Bm2}", "Bm")                                                              # 1

    # ---------------------------------------------------------------- A  (2-17)
    B("F#5:6 G5:2 F#5:1 E5:1 F#5:1 B5:1", f"{Bm} {Bm}", "Bm")                                   # 2
    B("A5:3 G5:2 F#5:1 E5:3 G5:2_ E5:1", f"{iio} {V65}", "C#m7b5/B F#7/A#")                      # 3
    B("D5:2 C#5:1 D5:1 F#5:1 B5:1 D6:3 B5:1.5 A#5:0.5 A5:1", f"{Bm} {VI}", "Bm G")              # 4
    B("G5:3 E#5:3 F#5:2 D5:1 C#5:2.5 F#5:0.5", HC, "Em/G@0 GIt6@3 F#@6")                       # 5

    B("F#5:5 F#5:1 (A5)G5:2 F#5:1 E5:1.5 F#5:0.5 B5:1", f"{Bm} {Bm2}", "Bm")                        # 6
    B("A5:3 G5:2 F#5:1 E5:2 {F#5 E5 D#5 E5}:1 G5:2_ E5:1", f"{iio} {V65}", "C#m7b5/B F#7/A#")    # 7
    B("D5:2 C#5:1 D5:1 F#5:1 B5:1 E6:3 D6:2 B5:1", f"{Bm} G#1 E2 D3 E3 B3 E3", "Bm E7/G#")      # 8
    B("A5:2 G5:0.5 F#5:0.5 tr(E5 F#5):2.5 {D5 E5}:0.5 D5:3 F#5:1 G5:1 G#5:1",
      "A1 D3 F#3 A2 C#3 G3 D2 A2 F#3 A3 D4 A3", "D/A@0 A7@3 D@6")                               # 9

    B("A5:3 A4:1 F#5:1 D6:1 C6:2_ B5:1 A5:2 F#5:1",
      "D2 A2 F#3 A3 D4 A3 D#2 B2 F#3 A3 B3 A3", "D B7b9/D#")                                    # 10
    B("B5:3 B4:1 G5:1 E6:1 D6:2_ C#6:1 B5:2 G#5:1",
      "E2 B2 G3 B3 E4 B3 E#2 C#3 G#3 B3 C#4 B3", "Em C#7b9/E#")                                 # 11
    B("D6:3 B5:1 C#6:1 D6:1 E6:3_ D6:1 C#6:1 B5:1",
      "F#1 F#2 D3 F#3 B3 F#3 F#1 C#2 A#2 E3 F#3 E3", "Bm/F# F#7")                               # 12
    B("A#5:3 C#6:2 A#5:1 E5:3 G5:2_ E#5:1",
      "F#1 C#2 A#2 E3 G3 E3 F#1 C#2 A#2 E3 C#3 A#2", "F#7b9")                                   # 13

    B("(F#4)F#5:6 G5:2 F#5:1 {E5 F#5 A#5 B5 C#6 B5}:3", f"{Bm} {Bm2}", "Bm")                         # 14
    B("A5:3 G5:2 F#5:1 {E5 F#5 G#5 A#5 B5 C#6 D6 E6 F#6 E6 D6 C#6 B5 A#5 G5 F#5 E5}:6",
      f"{iio} {V65}", "C#m7b5/B F#7b9/A#")                                                      # 15
    B("D5:2 C#5:1 B4:1 F#5:1 B5:1 C#6:3 B5:1 A5:1 G5:1",
      "B1 F#2 D3 D#2 B2 A3 E2 B2 G3 B3 E4 B3", "Bm@0 B7/D#@3 Em@6")                                                # 16
    B("F#5:2 E5:0.5 D5:0.5 C#5:1.5 A#4:1 B4:0.5 B4:6",
      f"F#1 D3 B3 F#2 C#3 E3 {Bm}", "Bm/F#@0 F#7@3 Bm@6")                                       # 17

    # ---------------------------------------------------------------- B  (18-33)
    G = "G2 D3 B3 D3 B3 D3"
    B("G4+B4:2 B4+D5:1 B4+G5:3 D5+F#5:2 C5+E5:1 B4+D5:3",
      f"{G} G2 D3 C4 G2 D3 B3", "G@0 D7/G@6 G@9", texture="duet")                               # 18
    B("B4+D5:2 B4+E5:1 D5+B5:3 C5+A5:2 C5+E5:1 A4+C5:3",
      "G#2 E3 B3 E3 D4 E3 A2 E3 C4 E3 C4 E3", "E7/G# Am", texture="duet")                       # 19
    B("A4+C5:2 A4+D5:1 (B5)C5+A5:3 B4+G5:2 B4+D5:1 G4+B4:3",
      f"F#2 D3 C4 D3 A3 D3 {G}", "D7/F# G", texture="duet")                                     # 20
    B("C5+E5:2 E5+G5:1 E5+A5:1.5 G#5:0.5 E5+G5:1 F#5:6",
      "C3 G3 E4 C#3 G3 E4 D3 A3 F#4 A3 C4 A3", "C@0 A7/C#@3 D@6 D7@9",
      rh2="r:6 D5:3 C5:3", texture="duet")                                                      # 21
    B("G4+B4:2 B4+D5:1 D5+B5:3 C5+A5:2 C5+F#5:1 B4+G5:3",
      f"{G} G2 D3 C4 G2 D3 B3", "G@0 D7/G@6 G@9", texture="duet")                               # 22
    B("B4+D5:2 B4+E5:1 D5+B5:3 C5+A5:2 E5+C6:0.5 D#6:0.5 A5+E6:3",
      "G#2 E3 B3 E3 D4 E3 A2 E3 C4 E3 C4 E3", "E7/G# Am", texture="duet")                       # 23
    B("B5+D6:3 A5+C6:1 G5+B5:1 D5+G5:1 C5+A5:3 C5+B5:1 C5+A5:1 D5+F#5:0.5 G5:0.5",
      "D2 B2 G3 B3 D4 B3 D2 A2 F#3 C4 F#3 A2", "G/D D7", texture="duet")                        # 24
    B("B4+G5:6 r:2 D6:1 G6:3", f"{G} G2 D3 B3 D3 G3 D3", "G", texture="duet")                   # 25

    B("G4+B4:2 B4+D5:1 B4+G5:3 D5+F5:2 B4+E5:1 B4+D5:3",
      f"{G} G#2 E3 B3 E3 D4 E3", "G E7b9/G#", texture="duet")                                   # 26
    B("A4+C5:2 C5+E5:1 C5+A5:3 E5+G5:2 C#5+F#5:1 C#5+E5:3",
      "A2 E3 C4 E3 C4 E3 A#2 F#3 C#4 F#3 E4 F#3", "Am F#7b9/A#", texture="duet")                # 27
    B("B4+D5:2 D5+F#5:1 D5+B5:3 B5+D6:3 D6+F6:3",
      "B2 F#3 D4 F#3 D4 F#3 B2 G3 F4 G3 D4 G3", "Bm G7/B", texture="duet")                      # 28
    B("E5+G5+E6:3 C5+C6:2 E5+E6:1 E5+G5+E6:3 C#5+C#6:2 E5+E6:1",
      "C2 G2 E3 G3 C4 G3 C#2 A#2 E3 G3 C#4 G3", "C A#dim7/C#")                                  # 29
    B("F#5+B5+F#6:3 D5+D6:2 F#5+F#6:1 A5+F#6+A6:3 F#5+F#6:2 A5+A6:1",
      "D2 B2 F#3 B3 D4 B3 D#2 B2 F#3 A3 B3 A3", "Bm/D B7/D#")                                   # 30
    B("G5+B5+E6+G6:3 E5+E6:2 G5+G6:1 G5+B5+D6+G6:3 G5+B5+D6+G6:3",
      "E1+E2 B2 G3 B3 E4 B3 E#1+E#2 B2 D3 G3 B3 D4", "Em G7/F")                               # 31
    B("F#5+B5+D6+F#6:3 E5+E6:1 D5+D6:1 C#5+C#6:1 B4+E5+B5:2 A#4+E5+A#5:1 C#5+E5+C#6:2 E5+A#5+E6:1",
      "F#1+F#2 D3 F#3 B3 D4 B3 F#1+F#2 C#3 E3 A#3 C#4 A#3", "Bm/F# F#7")                        # 32
    B("A#5+C#6+E6+G6:3 {F#6 E#6 F#6 G6 F#6 E6 D6 C#6 B5 A#5 G5 F#5 E5 D5 C#5 B4 A#4 B4 C#5 D5 D#5 E5 E#5}:9",
      "F#1+F#2 C#3 E3 G3 A#3 r:7", "F#7b9", ped=[0.0])                                          # 33

    # ---------------------------------------------------------------- A' (34-40)
    B("F#5:5 F#5:1 G5:1.5 A5:0.5 F#5:1 {E5 F#5 A#5 B5 D6 C#6 B5}:3", f"{Bm} {Bm2}", "Bm")       # 34
    B("A5:3 G5:2 F#5:1 {E5 G5 F#5 E#5 F#5 G#5 A#5 B5 C#6 D6 E6 G6 F#6 E#6 F#6 E6 D6 C#6 B5 A#5 G5 F#5 E5}:6",
      f"{iio} {V65}", "C#m7b5/B F#7b9/A#")                                                      # 35
    B("D5:2 C#5:1 D5:1 F#5:1 B5:1 tr(D6 E6):2.5 {C#6 D6}:0.5 B5:2 A5:1", f"{Bm} {VI}", "Bm G")  # 36
    B("G5:2 {A5 G5 F#5 G5}:1 E#5:3 F#5:2 D5:1 C#5:3", HC, "Em/G@0 GIt6@3 F#@6")                # 37
    B("D5:2 C#5:1 B4:1 B5:1 E6:1 E6:3 D6:2 B5:1",
      "B1 F#2 D3 D#2 B2 A3 E2 B2 G3 B3 E4 B3", "Bm@0 B7/D#@3 Em@6")         # 38
    B("G5:3 G4:1 E5:1 C6:1 E6:3 {D6 C6 B5 C6 E6 D6 C6}:3",
      "E2 C3 G3 C4 E4 C4 E2 C3 G3 C4 E4 C4", "C/E")                                             # 39
    B("A#5:3 C#6:2 E6:1 D6:3_ C#6:2 A#5:0.5 B5:0.5",
      "F#1 C#2 A#2 E3 F#3 E3 F#1 C#2 A#2 E3 F#3 C#3", "F#7")                                    # 40

    # ---------------------------------------------------------------- Coda (41-47)
    B("B5:6 r:3 E5:1 F#5:1 B5:1", f"{Bm} {Bm}", "Bm")                                           # 41
    B("A5:3 G5:2 F#5:1 E5:3 G5:2_ E5:1", f"{iio} B1 F#2 E3 A#3 C#4 A#3", "C#m7b5/B F#7b9/B")     # 42
    B("D#5:2 C#5:1 D#5:1 F#5:1 B5:1 D#6:3 B5:2 G#5:1",
      "B1 F#2 D#3 F#3 B3 F#3 B1 F#2 D#3 F#3 D#4 F#3", "B")                                      # 43
    B("G#5:3 E5:3 F#5:2 D#5:1 B4:3",
      "B1 G#2 E3 G#3 B3 G#3 B1 F#2 D#3 F#3 B3 F#3", "E/B B")                                    # 44
    B("E5+G5:3 D#5+F#5:3 E4+G4:3 D#4+F#4:3",
      "B1 G2 E3 B2 F#3 D#4 B1 G2 E3 B2 F#3 D#3", "Em/B@0 B@3 Em/B@6 B@9", texture="duet")       # 45
    B("r:1 B4 D#5 F#5 B5 D#6 F#6 B6:5'", "B1 F#2 D#3 B3 r:8", "B", ped=[0.0])                    # 46
    B("F#4+B4+D#5:6 D#4+F#4+B4:6", "B2+F#3:6 B1+F#2+B2:6", "B", ped=[0.0, 6.0])                 # 47
    return sc


# =============================================================== the performer's plan
# phrases (bar, pos) -> (bar, pos): used for the breathing of tempo and tone
PHRASES = [
    ((1, 0), (2, 0)), ((2, 0), (6, 0)), ((6, 0), (9, 9)), ((9, 9), (14, 0)), ((14, 0), (18, 0)),
    ((18, 0), (22, 0)), ((22, 0), (26, 0)), ((26, 0), (29, 0)), ((29, 0), (32, 0)), ((32, 0), (34, 0)),
    ((34, 0), (38, 0)), ((38, 0), (41, 6)), ((41, 6), (45, 0)), ((45, 0), (48, 0)),
]

# tempo in dotted quarters per minute at (bar, pos); linear in between
TEMPO = [
    (1, 0, 44), (1, 9, 43),
    (2, 0, 47), (3, 0, 49), (4, 0, 50), (4, 6, 48), (5, 0, 46), (5, 6, 43), (5, 11, 40),
    (6, 0, 48), (7, 0, 50), (8, 0, 51), (8, 6, 47), (9, 0, 46), (9, 3, 42), (9, 6, 44), (9, 9, 47),
    (10, 0, 51), (11, 0, 54), (12, 0, 53), (12, 6, 48), (13, 0, 46), (13, 6, 41), (13, 11, 36),
    (14, 0, 46), (15, 0, 48), (15, 6, 43), (15, 11, 40), (16, 0, 48), (16, 6, 46),
    (17, 0, 43), (17, 3, 39), (17, 6, 40), (17, 11, 38),
    (18, 0, 53), (19, 0, 56), (20, 0, 56), (21, 0, 54), (21, 9, 50), (22, 0, 55), (23, 0, 57), (23, 9, 54),
    (24, 0, 52), (24, 6, 48), (25, 0, 50), (25, 11, 48),
    (26, 0, 55), (27, 0, 58), (28, 0, 61), (29, 0, 63), (30, 0, 65), (30, 9, 62),
    (31, 0, 54), (31, 6, 46), (31, 11, 40), (32, 0, 46), (32, 6, 44), (32, 11, 40),
    (33, 0, 38), (33, 3, 31), (33, 5.5, 54), (33, 8.5, 58), (33, 10.5, 42), (33, 11.7, 25),
    (34, 0, 45), (35, 0, 47), (35, 6, 41), (35, 11, 37), (36, 0, 47), (36, 6, 44),
    (37, 0, 44), (37, 6, 41), (37, 11, 37),
    (38, 0, 47), (38, 6, 45), (39, 0, 42), (39, 9, 40), (40, 0, 43), (40, 6, 40), (40, 11, 34),
    (41, 0, 43), (42, 0, 44), (43, 0, 43), (44, 0, 42), (44, 9, 39), (45, 0, 40), (45, 9, 36),
    (46, 0, 42), (46, 7, 39), (47, 0, 35), (47, 11, 29),
]

# time that is simply taken: breaths, placements, fermatas (bar, pos, seconds)
BREATHS = [
    (2, 0, 0.22), (6, 0, 0.12), (10, 0, 0.10), (14, 0, 0.35), (18, 0, 0.45), (22, 0, 0.12), (26, 0, 0.15),
    (32, 0, 0.20), (33, 0, 0.12), (33, 3, 0.85), (34, 0, 0.80), (38, 0, 0.10), (39, 0, 0.32), (41, 0, 0.25),
    (43, 0, 0.32), (45, 0, 0.20), (46, 0, 0.30), (47, 0, 0.30), (47, 6, 0.55),
]

# dynamic level 0..1 at (bar, pos):  .15 ppp  .25 pp  .38 p  .50 mp  .62 mf  .78 f  .92 ff
DYNAMICS = [
    (1, 0, .22), (1, 6, .26), (1, 11, .22),
    (2, 0, .36), (2, 9, .38), (3, 0, .45), (3, 6, .38), (3, 11, .36), (4, 0, .40), (4, 6, .55), (4, 11, .44),
    (5, 0, .42), (5, 6, .34), (5, 11, .28),
    (6, 0, .38), (7, 0, .47), (7, 6, .40), (8, 0, .44), (8, 6, .63), (8, 11, .50), (9, 0, .48), (9, 6, .38), (9, 9, .40),
    (10, 0, .46), (10, 6, .50), (11, 0, .55), (11, 6, .60), (12, 0, .70), (12, 6, .75), (12, 11, .62),
    (13, 0, .55), (13, 6, .40), (13, 11, .30),
    (14, 0, .30), (14, 9, .34), (15, 0, .38), (15, 6, .36), (15, 9, .42), (15, 11, .34),
    (16, 0, .38), (16, 6, .50), (16, 11, .42), (17, 0, .40), (17, 6, .30), (17, 11, .25),
    (18, 0, .30), (18, 3, .34), (18, 11, .30), (19, 3, .42), (19, 11, .34), (20, 3, .40), (20, 11, .32),
    (21, 3, .42), (21, 6, .38), (21, 11, .32),
    (22, 0, .34), (22, 3, .38), (22, 11, .34), (23, 3, .46), (23, 9, .56), (24, 0, .54), (24, 6, .44), (24, 11, .38),
    (25, 0, .34), (25, 11, .28),
    (26, 0, .38), (26, 6, .44), (27, 0, .46), (27, 6, .52), (28, 0, .56), (28, 6, .64), (28, 11, .72),
    (29, 0, .74), (29, 6, .78), (30, 0, .82), (30, 6, .86), (31, 0, .90), (31, 6, .92), (32, 0, .95), (32, 6, .88),
    (32, 11, .84), (33, 0, .88), (33, 3, .62), (33, 7, .46), (33, 10, .34), (33, 11.9, .26),
    (34, 0, .26), (34, 9, .30), (35, 0, .34), (35, 6, .30), (35, 9, .38), (35, 11, .28),
    (36, 0, .32), (36, 6, .44), (36, 11, .36), (37, 0, .36), (37, 6, .30), (37, 11, .26),
    (38, 0, .36), (38, 6, .58), (38, 11, .46), (39, 0, .26), (39, 6, .34), (39, 11, .30),
    (40, 0, .36), (40, 6, .47), (40, 11, .32),
    (41, 0, .30), (41, 6, .24), (41, 9, .28), (42, 0, .34), (42, 6, .30), (42, 11, .26),
    (43, 0, .26), (43, 6, .36), (43, 11, .30), (44, 0, .32), (44, 6, .27), (44, 11, .22),
    (45, 0, .24), (45, 6, .17), (45, 11, .15), (46, 0, .19), (46, 4, .23), (46, 7, .18), (47, 0, .17), (47, 6, .10),
]

# una corda (soft pedal) regions (bar, pos) -> (bar, pos)
UNA_CORDA = [((1, 0), (2, 0)), ((14, 0), (15, 0)), ((18, 0), (19, 0)), ((34, 0), (36, 0)),
             ((39, 0), (40, 0)), ((41, 0), (42, 0)), ((43, 0), (43, 6)), ((45, 0), (48, 0))]

# places where the bass sounds a moment before the melody (old-school "dislocation"),
# reserved for the points of greatest weight (bar, pos, milliseconds)
BASS_FIRST = [(2, 0, 35), (14, 0, 45), (32, 0, 60), (34, 0, 50), (39, 0, 55), (43, 0, 50), (47, 0, 40)]

# rolled chords (bar, pos) -> spread per note in ms
ROLLS = {(31, 0): 26, (31, 6): 22, (32, 0): 28, (33, 0): 32, (47, 0): 36, (47, 6): 46}

# half-changes of the pedal (bar, pos, depth): thin out a wash of passing notes, keep the bass
FLUTTER = [(15, 9.5, 0.44), (33, 5.5, 0.42), (33, 7.5, 0.40), (33, 9.5, 0.40), (33, 11.0, 0.42),
           (35, 8.5, 0.44), (35, 10.5, 0.44), (39, 10.5, 0.46), (46, 5.0, 0.50)]
