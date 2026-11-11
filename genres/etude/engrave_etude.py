"""Engrave Firethorn: notation text -> LilyPond -> PDF.     python engrave_etude.py [out_dir]

The engraver reads the same text the performer reads.  What it adds is layout only:
note values in 2/4 down to the thirty-second, irregular groups as tuplets, clef changes
when a hand leaves its staff, 8va brackets for the bell register, key changes, tempo
headings, dynamics and the few words a pianist needs.
"""
import math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "engine"))
from score import _split, _TAIL, dur as _dur, midi
from lily import ly_pitch, chord_text, LILY
import firethorn as piece

VALS = ((8, "2"), (6, "4."), (4, "4"), (3, "8."), (2, "8"), (1.5, "16."), (1, "16"), (0.5, "32"), (0.25, "64"))


def pieces(pos, d, rest=False):
    """split a length (sixteenths) starting at pos into values that respect the beat of 2/4"""
    out = []
    while d > 1e-9:
        inbeat = pos % 4
        room = d if inbeat < 1e-9 else min(d, 4 - inbeat)
        for v, s in VALS:
            if v > room + 1e-9:
                continue
            if v == 8 and pos % 8 > 1e-9:
                continue
            if v == 6 and (rest or pos % 8 > 1e-9):
                continue
            if v == 4 and inbeat > 1e-9:
                continue
            if v == 3 and not (inbeat < 1e-9 or abs(inbeat - 1) < 1e-9):
                continue
            if v in (2, 1.5, 1) and pos % 1 > 1e-9:
                continue
            if v == 0.5 and pos % 0.5 > 1e-9:
                continue
            break
        out.append(s); pos += v; d -= v
    return out


def items(text):
    out, pos = [], 0.0
    for tok in _split(text):
        graces = []
        if tok.startswith("("):
            g, tok = tok[1:].split(")", 1)
            graces = g.split()
        if tok.startswith("{"):
            body, rest = tok[1:].split("}", 1)
            m = _TAIL.match(rest)
            d = _dur(m.group(2)) if m.group(2) else 1.0
            out.append(dict(kind="group", pos=pos, d=d, names=body.split(), graces=[], flags=m.group(3)))
        else:
            m = _TAIL.match(tok)
            d = _dur(m.group(2)) if m.group(2) else 1.0
            rest = m.group(1) == "r"
            out.append(dict(kind="rest" if rest else "note", pos=pos, d=d, names=[] if rest else m.group(1).split("+"),
                            graces=graces, flags=m.group(3)))
        pos += d
    return out


def tuplet(n, d):
    """(notes it replaces, value) for n notes in d sixteenths: the conventional choice has
    more notes than the plain group but fewer than twice as many (3:2, 6:4, 11:7 ...)"""
    best = None
    for unit, sym in ((2.0, "8"), (1.0, "16"), (0.5, "32"), (0.25, "64")):
        mm = d / unit
        if abs(mm - round(mm)) > 1e-9 or mm < 1:
            continue
        mm = int(round(mm))
        score = 0 if n == mm else (1 if mm < n < 2 * mm else 2 + abs(math.log(n / mm)))
        if best is None or score < best[0]:
            best = (score, mm, sym)
    return best[1], best[2]


def voice_ly(its, marks=None, prefix=None, stacc=False, grace_spacers=(), spacer_rests=False):
    """marks {pos: postfix} go to the first note at or after pos; prefix {item index: text}"""
    marks, prefix = dict(marks or {}), prefix or {}
    mk = {}
    for p in sorted(marks):
        idx = [i for i, it in enumerate(its) if it["kind"] != "rest" and it["pos"] >= p - 1e-9]
        if not idx and its:
            idx = [0]
        mk[idx[0]] = mk.get(idx[0], "") + marks[p]
    out = []
    for i, it in enumerate(its):
        pre = prefix.get(i, "")
        if any(abs(it["pos"] - g) < 1e-9 for g in grace_spacers):
            pre += "\\grace s8 "
        m = mk.get(i, "")
        if it["kind"] == "rest":
            if it["d"] >= 8 - 1e-9 and it["pos"] < 1e-9:
                out.append(pre + ("s2" if spacer_rests else "R2") + m)
            else:
                out.append(pre + " ".join(("s" if spacer_rests else "r") + s for s in pieces(it["pos"], it["d"], rest=True)))
        elif it["kind"] == "group":
            n = len(it["names"])
            mm, sym = tuplet(n, it["d"])
            inner = " ".join(ly_pitch(nm) + (sym + m if j == 0 else "") for j, nm in enumerate(it["names"]))
            out.append(pre + (inner if n == mm else "\\tuplet %d/%d { %s }" % (n, mm, inner)))
        else:
            ch = chord_text(it["names"])
            ps = pieces(it["pos"], it["d"])
            art = "-." if (stacc and it["d"] == 2 and "'" not in it["flags"]) else ""
            g = "".join("\\acciaccatura %s8 " % ly_pitch(x) for x in it["graces"])
            out.append(pre + g + " ".join(ch + s + ("~" if j < len(ps) - 1 else "") + ((art + m) if j == 0 else "")
                                          for j, s in enumerate(ps)))
    return " ".join(out)


# ------------------------------------------------------------------ clefs and 8va
HIGH = 93          # A6: from here up the right hand is written an octave lower under an 8va bracket
LOW = 28           # E1: from here down the left hand is written an octave higher under an 8va bassa


def pitches(its):
    return [midi(nm) for it in its if it["kind"] != "rest" for nm in it["names"]]


def plan(its, st, upper, extra=()):
    """prefixes for one voice of one bar; st carries clef and ottava across bars"""
    pre = {}
    key_c, key_o = ("up_clef", "up_ott") if upper else ("lo_clef", "lo_ott")
    # clef, decided beat by beat
    for beat in (0, 1):
        idx = [i for i, it in enumerate(its) if beat * 4 - 1e-9 <= it["pos"] < beat * 4 + 4 - 1e-9]
        ps = pitches([its[i] for i in idx]) + (list(extra) if beat == 0 else [])
        if not ps:
            continue
        mean = sum(ps) / len(ps)
        want = st[key_c]
        if upper:
            if st[key_c] == "treble" and max(ps) <= 68 and (mean < 57 or (mean < 60 and min(ps) < 52)): want = "bass"
            elif st[key_c] == "bass" and mean > 60: want = "treble"
        else:
            if st[key_c] == "bass" and mean > 64 and min(ps) >= 52: want = "treble"
            elif st[key_c] == "treble" and mean < 60: want = "bass"
        if want != st[key_c]:
            pre[idx[0]] = pre.get(idx[0], "") + f"\\clef {want} "
            st[key_c] = want
    # ottava
    allp = pitches(its)
    want = []
    if upper and not extra:
        n_high = len([p for p in allp if p >= HIGH])
        # a bar that lives up there is written under one bracket; a bracket already open stays open
        whole = bool(allp) and min(allp) >= 72 and (n_high >= 2 or (st[key_o] == 1 and max(allp) >= 88))
        for it in its:
            ps = pitches([it])
            want.append((want[-1] if want else st[key_o]) if not ps else int(whole or (max(ps) >= HIGH and min(ps) >= 72)))
    else:
        for it in its:
            ps = pitches([it])
            want.append(0 if (upper or not ps) else (-1 if min(ps) <= LOW else 0))
    for i, w in enumerate(want):
        if w != st[key_o]:
            pre[i] = f"\\ottava #{w} " + pre.get(i, "")
            st[key_o] = w
    return pre


# ------------------------------------------------------------------ words and signs
it_ = lambda text: '^\\markup\\italic"%s"' % text
under = lambda text: '_\\markup\\italic"%s"' % text
TEMPI = {
    ("Intro", 1): ("Lento a capriccio", 48), ("Theme", 1): ("Tema.  Allegretto capriccioso", 96),
    ("Var1", 1): ("Var. 1.  Presto", 152), ("Var2", 1): ("Var. 2.  L'istesso tempo", None),
    ("Var3", 1): ("Var. 3.  Allegretto", 108), ("Var4", 1): ("Var. 4.  Meno mosso", 78),
    ("Middle", 1): ("Andante cantabile", 56), ("Middle", 17): ("Largamente", 54),
    ("Retrans", 1): ("Poco a poco accelerando", None),
    ("Var5", 1): ("Var. 5.  Presto con fuoco", 132), ("Coda", 1): ("Coda.  Vivace", 146), ("Coda", 17): ("Più mosso", 152),
    ("Coda", 33): ("Martellato", 132), ("Coda", 43): ("Largamente", 88),
}
RH_MARKS = {
    ("Intro", 1, 0): "\\f" + it_("pesante"), ("Intro", 4, 0): "\\pp" + it_("quasi campanella"), ("Intro", 5, 0): "\\f",
    ("Intro", 8, 0): "\\pp", ("Intro", 9, 0): "\\p" + it_("espressivo"), ("Intro", 12, 0): "\\mp",
    ("Intro", 12, 4): it_("accelerando"), ("Intro", 13, 0): "\\pp\\fermata",
    ("Theme", 1, 0): "\\p" + it_("leggiero"), ("Theme", 11, 0): "\\mp", ("Theme", 13, 0): "\\>", ("Theme", 16, 0): "\\p",
    ("Var1", 1, 0): "\\mp" + it_("leggiero, non legato"), ("Var1", 9, 0): "\\mf" + it_("cresc."), ("Var1", 13, 0): "\\f",
    ("Var2", 1, 0): "\\f" + it_("marcato il tema"), ("Var2", 13, 0): "\\ff",
    ("Var3", 1, 0): "\\pp" + it_("leggierissimo"), ("Var3", 9, 0): "\\p", ("Var3", 13, 0): "\\>", ("Var3", 16, 0): "\\pp",
    ("Var4", 1, 0): "\\p" + it_("non legato"), ("Var4", 9, 0): "\\mp\\<", ("Var4", 13, 0): "\\mf\\>", ("Var4", 16, 0): "\\p",
    ("Trans", 1, 0): "\\pp" + it_("ritenuto"),
    ("Middle", 1, 0): "\\pp" + it_("dolcissimo"), ("Middle", 9, 0): "\\mf" + it_("con anima"), ("Middle", 15, 0): "\\<",
    ("Middle", 17, 0): "\\ff" + it_("grandioso"), ("Middle", 21, 0): "\\>", ("Middle", 23, 0): "\\p" + it_("ritardando"),
    ("Middle", 24, 0): "\\pp\\fermata",
    ("Retrans", 1, 0): "\\pp", ("Retrans", 4, 0): "\\mf\\<", ("Retrans", 6, 0): "\\f\\<",
    ("Var5", 1, 0): "\\ff" + it_("marcatissimo"), ("Var5", 9, 0): it_("con fuoco"),
    ("Coda", 1, 0): "\\p" + it_("scherzando"), ("Coda", 9, 0): "\\mp" + it_("leggiero, crescendo"),
    ("Coda", 17, 0): "\\ff" + it_("con bravura"), ("Coda", 33, 0): "\\f\\<", ("Coda", 35, 0): "\\fff",
    ("Coda", 41, 0): "\\fff", ("Coda", 44, 0): "\\fermata",
}
RH2_MARKS = {("Middle", 1, 0): under("il canto ben marcato")}
LH_MARKS = {
    ("Intro", 1, 0): under("con Ped."), ("Intro", 13, 0): "\\fermata",
    ("Theme", 1, 0): under("a touch of pedal with each bass note"),
    ("Var1", 1, 0): under("senza Ped."), ("Var1", 9, 0): under("poco Ped."),
    ("Var3", 1, 0): under("una corda"), ("Var3", 9, 0): under("tre corde"),
    ("Trans", 1, 0): under("una corda"), ("Middle", 1, 0): under("tre corde, con Ped."),
    ("Middle", 24, 0): "\\fermata", ("Coda", 44, 0): "\\fermata",
}
KEY_LY = {"F#m": "\\key fs \\minor", "D": "\\key d \\major", "F#": "\\key fs \\major"}
STACC_RH = ("theme", "friska")
STACC_LH = ("theme", "campanella", "friska", "repeat", "run_rh")

HEAD = r'''\version "2.24.0"
\language "english"
#(set-global-staff-size 18)
\header {
  title = "Firethorn"
  subtitle = "Rhapsodie-Étude in F-sharp minor"
  composer = "Claude, 2026"
  poet = "for piano solo"
  tagline = ##f
}
\paper {
  #(set-paper-size "a4")
  top-margin = 12\mm  bottom-margin = 12\mm  left-margin = 12\mm  right-margin = 12\mm
  system-system-spacing.basic-distance = #17
  ragged-last-bottom = ##f
}
'''
TAIL = r'''
\score {
  \new PianoStaff <<
    \new Staff = "up" \upper
    \new Staff = "down" \lower
  >>
  \layout { }
}
'''


def build_ly(sc):
    up, lo = [], []
    st = dict(up_clef="treble", lo_clef="bass", up_ott=0, lo_ott=0)
    for b in sc.bars:
        name, k = sc.tags[b.number - 1]
        tx = b.texture
        rh, lh = items(b.raw["rh"]), items(b.raw["lh"])
        rh2 = items(b.raw["rh2"]) if b.raw.get("rh2") else None
        rm = {float(p): t for (s, bb, p), t in RH_MARKS.items() if s == name and bb == k}
        lm = {float(p): t for (s, bb, p), t in LH_MARKS.items() if s == name and bb == k}
        graces = [x["pos"] for x in rh if x["graces"]]
        r = voice_ly(rh, rm, plan(rh, st, True, extra=pitches(rh2) if rh2 else ()), stacc=tx in STACC_RH)
        if rh2:
            m2 = {float(p): t for (s, bb, p), t in RH2_MARKS.items() if s == name and bb == k}
            r = "<< { \\voiceOne " + r + " } \\new Voice { \\voiceTwo " + voice_ly(rh2, m2) + " } >> \\oneVoice"
        l = voice_ly(lh, lm, plan(lh, st, False), stacc=tx in STACC_LH, grace_spacers=graces)
        head = ""
        if k == 1 and name in piece.KEYS:
            head += KEY_LY[piece.KEYS[name]] + " "
        lhead = head
        if (name, k) in TEMPI:
            text, bpm = TEMPI[(name, k)]
            head += '\\tempo "%s"%s ' % (text, f" 4 = {bpm}" if bpm else "")
        last = b.number == len(sc.bars)
        end = ' \\bar "|."' if last else (' \\bar "||"' if sc.tags[b.number][1] == 1 else "")
        up.append(f"  {head}{r}{end} | % {name} {k}")
        lo.append(f"  {lhead}{l}{end} | % {name} {k}")
    common = "  \\override TupletBracket.bracket-visibility = ##f\n  \\set Staff.ottavationMarkups = #ottavation-simple-ordinals\n"
    upper = "upper = {\n  \\clef treble \\time 2/4\n" + common + "\n".join(up) + "\n}\n"
    lower = "lower = {\n  \\clef bass \\time 2/4\n" + common + "\n".join(lo) + "\n}\n"
    return HEAD + upper + lower + TAIL


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "out", "etude_final")
    os.makedirs(out, exist_ok=True)
    ly = os.path.join(out, "firethorn.ly")
    open(ly, "w", encoding="utf8").write(build_ly(piece.build()))
    r = subprocess.run([LILY, "--pdf", "--png", "-dno-point-and-click", "-dresolution=100", "-o", os.path.join(out, "firethorn"), ly],
                       capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if any(w in l.lower() for w in ("error", "warning", "fatal"))]
    print("\n".join(bad[:30]) if bad else "engraved without warnings")
