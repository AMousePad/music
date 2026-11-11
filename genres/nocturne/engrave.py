"""Engrave the score: notation text -> LilyPond -> PDF.

python engrave.py [out_dir]
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "engine"))
from lily import LILY, voice_to_ly, it
import nocturne_bm as piece


# expressive text of the score (bar, pos) -> LilyPond postfix, attached to the right hand
RH_MARKS = {
    (2, 0): "\\p" + it("cantabile"), (4, 0): "\\<", (4, 6): "\\!", (4, 9): "\\>", (5, 6): "\\!",
    (6, 0): "\\p", (8, 0): "\\<", (8, 6): "\\mf", (9, 0): "\\>", (9, 6): "\\!",
    (10, 0): "\\mp" + it("poco animato"), (11, 0): "\\<", (12, 6): "\\f", (13, 0): "\\>",
    (13, 6): "\\!" + it("rit."),
    (14, 0): "\\pp" + it("a tempo, sotto voce"), (15, 6): it("leggiero"),
    (16, 6): "\\mp", (17, 0): "\\>" + it("rit."), (17, 6): "\\!",
    (18, 0): '\\pp^\\markup{\\bold"Poco più mosso" \\italic" dolce"}', (23, 6): "\\<", (24, 0): "\\mf",
    (24, 6): "\\>", (25, 0): "\\p",
    (26, 0): "\\p" + it("poco a poco cresc. e stringendo"), (29, 0): "\\f", (30, 6): "\\<",
    (31, 0): "\\ff" + it("allargando"), (32, 0): it("largamente"),
    (33, 0): "\\fermata\\>", (33, 3): "\\!" + it("dim. e rall."),
    (34, 0): '\\pp^\\markup{\\bold"Tempo I"}', (35, 6): it("leggierissimo"),
    (38, 0): "\\p\\<", (38, 6): "\\mf", (39, 0): "\\pp" + it("sotto voce"), (40, 6): "\\>" + it("rit."),
    (41, 0): "\\pp" + it("a tempo, tranquillo"), (43, 0): "\\pp" + it("dolcissimo"),
    (45, 0): "\\>" + it("perdendosi"), (45, 9): "\\!", (46, 1): "\\ppp", (47, 6): "\\fermata",
}
LH_MARKS = {(1, 0): '\\pp_\\markup\\italic"con pedale"', (47, 6): "\\fermata"}
KEYS = {1: "\\key b \\minor", 18: "\\key g \\major", 34: "\\key b \\minor", 43: "\\key b \\major"}
ARPEGGIO = {(31, 0), (31, 6), (32, 0), (33, 0), (47, 0), (47, 6)}
DOUBLE_BAR_AFTER = (17, 33, 40)

HEAD = r'''\version "2.24.0"
\language "english"
\header {
  title = "Nocturne"
  subtitle = "in B minor"
  composer = "Claude, 2026"
  poet = "in the manner of Chopin's nocturnes"
  tagline = ##f
}
\paper {
  #(set-paper-size "a4")
  top-margin = 12\mm  bottom-margin = 12\mm  left-margin = 13\mm  right-margin = 13\mm
  system-system-spacing.basic-distance = #17
  ragged-last-bottom = ##f
}
'''
TAIL = r'''
\score {
  \new PianoStaff \with { connectArpeggios = ##t } <<
    \new Staff = "up" \upper
    \new Staff = "down" \lower
  >>
  \layout {
    \context { \Score \override SpacingSpanner.common-shortest-duration = #(ly:make-moment 1/12) }
  }
}
'''


def build_ly(sc):
    up, lo = [], []
    for b in sc.bars:
        n = b.number
        rm = {float(p): t for (bb, p), t in RH_MARKS.items() if bb == n}
        lm = {float(p): t for (bb, p), t in LH_MARKS.items() if bb == n}
        for (bb, p) in ARPEGGIO:
            if bb == n:
                rm[float(p)] = rm.get(float(p), "") + "\\arpeggio"
                lm[float(p)] = lm.get(float(p), "") + "\\arpeggio"
        rh = voice_to_ly(b.raw["rh"], rm)
        if rm:
            print(f"  note: bar {n} marks not placed at {sorted(rm)}")
        if b.raw["rh2"]:
            rh = ("<< { \\voiceOne " + rh + " } \\new Voice { \\voiceTwo "
                  + voice_to_ly(b.raw["rh2"], {}, True) + " } >> \\oneVoice")
        lh = voice_to_ly(b.raw["lh"], lm)
        k = KEYS.get(n, "")
        dbl = ' \\bar "||"' if n in DOUBLE_BAR_AFTER else ""
        up.append(f"  {k} {rh}{dbl} | % {n}")
        lo.append(f"  {k} {lh}{dbl} | % {n}")
    upper = ("upper = {\n  \\clef treble \\time 12/8 \\tempo \"Lento sostenuto\" 4. = 46\n"
             "  \\override TupletBracket.bracket-visibility = ##f\n"
             + "\n".join(up) + "\n  \\bar \"|.\"\n}\n")
    lower = ("lower = {\n  \\clef bass \\time 12/8\n  \\override TupletBracket.bracket-visibility = ##f\n"
             + "\n".join(lo) + "\n  \\bar \"|.\"\n}\n")
    return HEAD + upper + lower + TAIL


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "out", "nocturne_final")
    os.makedirs(out, exist_ok=True)
    sc = piece.build()
    ly = os.path.join(out, "nocturne_b_minor.ly")
    open(ly, "w", encoding="utf8").write(build_ly(sc))
    r = subprocess.run([LILY, "--pdf", "--png", "-dno-point-and-click", "-dresolution=100", "-o", os.path.join(out, "nocturne_b_minor"), ly],
                       capture_output=True, text=True)
    print(r.stderr[-2500:])
