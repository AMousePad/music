"""LilyPond helpers shared by every engraver: pitch names, note values, and one voice of
notation text turned into LilyPond.

`pieces` spells note lengths for 12/8 with the eighth as unit (the nocturnes).  An
engraver for another metre replaces it:  lily.pieces = my_function.

LilyPond itself is looked for in this order: the LILYPOND environment variable, a copy
unpacked under tools/lilypond/ (see the README), then `lilypond` on the PATH.
"""
import math, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from score import _split, _TAIL, dur as _dur


def find_lilypond():
    if os.environ.get("LILYPOND"):
        return os.environ["LILYPOND"]
    tools = os.path.join(HERE, "..", "tools", "lilypond")
    if os.path.isdir(tools):
        for d in sorted(os.listdir(tools), reverse=True):
            for exe in ("lilypond.exe", "lilypond"):
                p = os.path.join(tools, d, "bin", exe)
                if os.path.isfile(p):
                    return p
    return shutil.which("lilypond") or "lilypond"


LILY = find_lilypond()
_P = re.compile(r"([A-G])(##|#|x|bb|b)?(-?\d)$")
ACC = {None: "", "#": "s", "##": "ss", "x": "ss", "b": "f", "bb": "ff"}


def ly_pitch(name):
    m = _P.match(name)
    o = int(m.group(3))
    return m.group(1).lower() + ACC[m.group(2)] + ("'" * (o - 3) if o >= 3 else "," * (3 - o))


def pieces(pos, d):
    """split a duration (eighths) starting at pos into notatable values for 12/8"""
    out = []
    while d > 1e-9:
        inbeat = pos % 3
        if inbeat < 1e-9 and abs(pos % 12) < 1e-9 and d >= 12 - 1e-9:
            v, s = 12, "1."
        elif inbeat < 1e-9 and abs(pos % 6) < 1e-9 and d >= 6 - 1e-9:
            v, s = 6, "2."
        elif inbeat < 1e-9 and d >= 3 - 1e-9:
            v, s = 3, "4."
        else:
            room = min(d, 3 - inbeat)
            for v, s in ((2, "4"), (1.5, "8."), (1, "8"), (0.75, "16."), (0.5, "16"), (0.25, "32"), (0.125, "64")):
                if v <= room + 1e-9:
                    break
        out.append(s); pos += v; d -= v
    return out


def chord_text(names):
    ps = [ly_pitch(n) for n in names]
    return ps[0] if len(ps) == 1 else "<" + " ".join(ps) + ">"


def voice_to_ly(text, marks, spacer_rests=False):
    """marks: {pos: 'text appended to the first note at that position'}"""
    out, pos = [], 0.0
    for tok in _split(text):
        graces = []
        if tok.startswith("("):
            g, tok = tok[1:].split(")", 1)
            graces = g.split()
        mk = marks.pop(pos, "") if marks else ""
        if tok.startswith("{"):
            body, rest = tok[1:].split("}", 1)
            m = _TAIL.match(rest); d = _dur(m.group(2)) if m.group(2) else 1.0
            names = body.split(); n = len(names)
            best = None
            for unit, sym in ((0.5, "16"), (0.25, "32"), (1.0, "8")):
                mm = d / unit
                if abs(mm - round(mm)) > 1e-9:
                    continue
                sc_ = abs(math.log(n / mm))
                if best is None or sc_ < best[0] - 1e-9:
                    best = (sc_, int(round(mm)), sym)
            _, mm, sym = best
            inner = " ".join(ly_pitch(nm) + (sym if i == 0 else "") + (mk if i == 0 else "") for i, nm in enumerate(names))
            out.append(inner if n == mm else "\\tuplet %d/%d { %s }" % (n, mm, inner))
            pos += d
            continue
        trill = ""
        if tok.startswith("tr("):
            body, rest = tok[3:].split(")", 1)
            tok = body.split()[0] + rest
            trill = "\\trill"
        m = _TAIL.match(tok)
        body, d = m.group(1), (_dur(m.group(2)) if m.group(2) else 1.0)
        ps = pieces(pos, d)
        if body == "r":
            if d >= 12 - 1e-9:
                out.append("s1." if spacer_rests else "R1.")
            else:
                out.append(" ".join(("s" if spacer_rests else "r") + s for s in ps))
            pos += d
            continue
        ch = chord_text(body.split("+"))
        pre = ("\\acciaccatura " + " ".join(ly_pitch(g) + "8" for g in graces) + " ") if graces else ""
        tie = "~" if "~" in m.group(3) else ""
        parts = [ch + s + ("~" if i < len(ps) - 1 else tie) + ((trill + mk) if i == 0 else "") for i, s in enumerate(ps)]
        out.append(pre + " ".join(parts))
        pos += d
    return " ".join(out)


def it(text):
    return '^\\markup\\italic"%s"' % text
