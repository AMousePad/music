"""Engrave the rag: notation text -> LilyPond -> PDF.     python engrave_rag.py [out_dir]

Laid out the way rags were published: introduction, each strain once with repeat signs,
the first strain written out again before the trio, key change for the trio.
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "engine"))
import lily                         # shared note/chord/tie writer
import larkspur_rag as piece


def pieces_2_4(pos, d):
    """split a duration (sixteenths) starting at pos into notatable values for 2/4"""
    out = []
    while d > 1e-9:
        inbeat = pos % 4
        if inbeat < 1e-9 and abs(pos % 8) < 1e-9 and d >= 8 - 1e-9:
            v, s = 8, "2"
        elif inbeat < 1e-9 and d >= 4 - 1e-9:
            v, s = 4, "4"
        else:
            room = min(d, 4 - inbeat)
            for v, s in ((3, "8."), (2, "8"), (1, "16")):
                if v <= room + 1e-9:
                    break
        out.append(s); pos += v; d -= v
    return out


lily.pieces = pieces_2_4          # the shared writer asks this function how to spell lengths

it = lambda text: '^\\markup\\italic"%s"' % text
MARKS = {  # (strain, bar, pos) -> postfix on the right hand
    ("Intro", 1, 0): "\\f",
    ("A", 1, 0): "\\mf", ("A", 13, 0): "\\<", ("A", 15, 0): "\\!",
    ("B", 1, 0): "\\f", ("B", 9, 0): it("broadly"),
    ("A2", 1, 0): "\\mf",
    ("C", 1, 0): "\\p" + it("dolce, cantabile"), ("C", 11, 0): "\\<", ("C", 13, 0): "\\mf", ("C", 15, 0): "\\>", ("C", 16, 0): "\\!",
    ("D", 1, 0): "\\f" + it("2nd time ff"), ("D", 9, 0): it("brillante"),
}
LH_MARKS = {("A", 1, 0): '_\\markup\\italic"a touch of pedal with each bass octave"',
            ("C", 1, 0): '_\\markup\\italic"legato pedal"'}


def strain_ly(name, label=None, final=False):
    up, lo = [], []
    label = label or name
    for i, (rh, lh, harm) in enumerate(piece.STRAINS[name]):
        k = i + 1
        rm = {float(p): t for (s, b, p), t in MARKS.items() if s == label and b == k}
        lm = {float(p): t for (s, b, p), t in LH_MARKS.items() if s == label and b == k}
        if final and k == len(piece.STRAINS[name]):
            rm[4.0] = rm.get(4.0, "") + "\\fermata"; lm[4.0] = lm.get(4.0, "") + "\\fermata"
        up.append("    " + lily.voice_to_ly(rh, rm) + f" | % {label} {k}")
        lo.append("    " + lily.voice_to_ly(lh, lm) + f" | % {label} {k}")
    return "\n".join(up), "\n".join(lo)


def build_ly():
    U, Lo = [], []

    def add(name, repeat=False, pre="", label=None, final=False):
        u, l = strain_ly(name, label, final)
        if repeat:
            U.append(f"  {pre}\\repeat volta 2 {{\n{u}\n  }}"); Lo.append(f"  {pre}\\repeat volta 2 {{\n{l}\n  }}")
        else:
            U.append(f"  {pre}\n{u}"); Lo.append(f"  {pre}\n{l}")

    add("Intro")
    add("A", repeat=True)
    add("B", repeat=True)
    add("A", label="A2")
    U.append('  \\bar "||"'); Lo.append('  \\bar "||"')
    add("C", repeat=True, pre='\\key af \\major \\mark \\markup\\bold"Trio" ')
    add("D", repeat=True, pre="\\key ef \\major ", final=True)
    head = r'''\version "2.24.0"
\language "english"
\header {
  title = "Larkspur Rag"
  subtitle = "a classic rag for piano"
  composer = "Claude, 2026"
  poet = "in the manner of Scott Joplin"
  tagline = ##f
}
\paper {
  #(set-paper-size "a4")
  top-margin = 12\mm  bottom-margin = 12\mm  left-margin = 13\mm  right-margin = 13\mm
  system-system-spacing.basic-distance = #16
  ragged-last-bottom = ##f
}
'''
    upper = "upper = {\n  \\clef treble \\key ef \\major \\time 2/4 \\tempo \"Not fast\" 4 = 92\n" + "\n".join(U) + "\n  \\bar \"|.\"\n}\n"
    lower = "lower = {\n  \\clef bass \\key ef \\major \\time 2/4\n" + "\n".join(Lo).replace('\\mark \\markup\\bold"Trio" ', "") + "\n  \\bar \"|.\"\n}\n"
    tail = r'''
\score {
  \new PianoStaff <<
    \new Staff = "up" \upper
    \new Staff = "down" \lower
  >>
  \layout { }
}
'''
    return head + upper + lower + tail


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "out", "ragtime_final")
    os.makedirs(out, exist_ok=True)
    ly = os.path.join(out, "larkspur_rag.ly")
    open(ly, "w", encoding="utf8").write(build_ly())
    r = subprocess.run([lily.LILY, "--pdf", "--png", "-dno-point-and-click", "-dresolution=100", "-o", os.path.join(out, "larkspur_rag"), ly],
                       capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if any(w in l.lower() for w in ("error", "warning", "fatal"))]
    print("\n".join(bad[:20]) if bad else "engraved without warnings")
