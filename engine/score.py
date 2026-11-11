"""A small text notation for two-hand piano music and its parser.

Time unit: the eighth note.  A voice is a string of tokens:

    F#5:6            note, 6 eighths long            (default length 1)
    B4+G5:3          chord (top note is the melody)
    r:3              rest
    (A5)G5:2         grace note(s) before a note      (played on the beat, Chopin's way)
    {E5 F#5 B5}:3    fioritura: n notes spread over 3 eighths, timing left to the player
    tr(E5 F#5):2.5   trill on E5 with F#5
    D5:3~            tie into the next token
    suffix flags after the duration:  !  accent    _  tenuto    '  lighter
"""
import re
from dataclasses import dataclass, field

PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
ACC = {None: 0, "": 0, "#": 1, "##": 2, "x": 2, "b": -1, "bb": -2}
_PITCH = re.compile(r"([A-G])(##|#|x|bb|b)?(-?\d)$")


def midi(name):
    m = _PITCH.match(name)
    if not m:
        raise ValueError(f"bad pitch {name!r}")
    return 12 * (int(m.group(3)) + 1) + PC[m.group(1)] + ACC[m.group(2)]


def dur(text):
    if "/" in text:
        a, b = text.split("/")
        return float(a) / float(b)
    return float(text)


@dataclass
class Note:
    s: float                 # onset, eighths from the start of the piece
    dur: float               # notated length in eighths
    pitch: int
    name: str
    hand: str                # 'R' or 'L'
    voice: str               # rh, rh2, lh, lh2
    bar: int = 0
    pos: float = 0.0         # onset inside the bar
    role: str = ""           # melody, duet, rh_inner, bass, acc
    chord_size: int = 1
    chord_rank: int = 0      # 0 = lowest note of its chord
    grace: tuple = None      # (k, n): k-th of n grace notes before the main note at s
    group: tuple = None      # (gid, k, n, s0, D): k-th of n fioritura notes over D eighths
    trill: int = None        # upper-note pitch if this note is trilled
    flags: frozenset = frozenset()
    after_grace: int = 0     # number of grace notes that precede this note


def _split(text):
    out, depth, cur = [], 0, ""
    for ch in text.strip():
        if ch in "({":
            depth += 1
        elif ch in ")}":
            depth -= 1
        if ch.isspace() and depth == 0:
            if cur:
                out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out


_TAIL = re.compile(r"^(.*?)(?::([0-9./]+))?([~!_']*)$")
_gid = [0]


def parse_voice(text, bar, hand, voice, bar_len=12.0, s0=0.0):
    """-> list of Note for one voice of one bar."""
    notes, pos, tie = [], 0.0, {}
    for tok in _split(text):
        graces = []
        if tok.startswith("("):
            g, tok = tok[1:].split(")", 1)
            graces = g.split()
        if tok.startswith("{"):
            body, rest = tok[1:].split("}", 1)
            m = _TAIL.match(rest)
            d = dur(m.group(2)) if m.group(2) else 1.0
            names = body.split()
            _gid[0] += 1
            for k, nm in enumerate(names):
                notes.append(Note(s0 + pos + d * k / len(names), d / len(names), midi(nm), nm, hand, voice, bar,
                                  pos + d * k / len(names), group=(_gid[0], k, len(names), s0 + pos, d),
                                  flags=frozenset(m.group(3))))
            pos += d
            continue
        if tok.startswith("tr("):
            body, rest = tok[3:].split(")", 1)
            m = _TAIL.match(rest)
            d = dur(m.group(2)) if m.group(2) else 1.0
            main, upper = body.split()
            notes.append(Note(s0 + pos, d, midi(main), main, hand, voice, bar, pos, trill=midi(upper),
                              flags=frozenset(m.group(3))))
            pos += d
            continue
        m = _TAIL.match(tok)
        body, d, fl = m.group(1), (dur(m.group(2)) if m.group(2) else 1.0), frozenset(m.group(3))
        if body == "r":
            pos += d
            tie = {}
            continue
        names = body.split("+")
        ps = sorted((midi(n), n) for n in names)
        for k, gname in enumerate(graces):
            notes.append(Note(s0 + pos, 0.0, midi(gname), gname, hand, voice, bar, pos, grace=(k, len(graces))))
        new_tie = {}
        for rank, (p, nm) in enumerate(ps):
            if p in tie:                       # tied continuation: lengthen the earlier note
                tie[p].dur += d
                if "~" in fl:
                    new_tie[p] = tie[p]
                continue
            n = Note(s0 + pos, d, p, nm, hand, voice, bar, pos, chord_size=len(ps), chord_rank=rank,
                     flags=fl - {"~"}, after_grace=len(graces) if rank == len(ps) - 1 else 0)
            notes.append(n)
            if "~" in fl:
                new_tie[p] = n
        tie = new_tie
        pos += d
    if abs(pos - bar_len) > 1e-6:
        raise ValueError(f"bar {bar} {voice}: adds up to {pos} eighths, expected {bar_len}")
    return notes


# ---------------------------------------------------------------- chord symbols
QUAL = {
    "": (0, 4, 7), "m": (0, 3, 7), "6": (0, 4, 7, 9), "7": (0, 4, 7, 10), "m7": (0, 3, 7, 10), "maj7": (0, 4, 7, 11),
    "dim": (0, 3, 6), "dim7": (0, 3, 6, 9), "m7b5": (0, 3, 6, 10), "7b9": (0, 4, 7, 10, 13),
    "sus4": (0, 5, 7), "It6": (0, 4, 10), "Ger6": (0, 4, 7, 10), "Fr6": (0, 4, 6, 10),
}
_CH = re.compile(r"([A-G](?:#|b)?)(It6|Ger6|Fr6|maj7|m7b5|dim7|dim|7b9|m7|sus4|7|6|m)?(?:/([A-G](?:#|b)?))?$")


def chord_pcs(sym):
    """'F#7b9/A#' -> (set of pitch classes, bass pitch class, root pitch class)."""
    m = _CH.match(sym)
    if not m:
        raise ValueError(f"bad chord symbol {sym!r}")
    root = (PC[m.group(1)[0]] + ACC[m.group(1)[1:] or None]) % 12
    q = m.group(2) or ""
    if q in ("It6", "Ger6", "Fr6"):
        # written from the bass note (flat 6th degree): G It6 = G B E#
        pcs = {(root + i) % 12 for i in QUAL[q]}
    else:
        pcs = {(root + i) % 12 for i in QUAL[q]}
    bass = root if not m.group(3) else (PC[m.group(3)[0]] + ACC[m.group(3)[1:] or None]) % 12
    return pcs | {bass}, bass, root


def parse_harmony(text, bar_len=12.0):
    """'Bm G' -> the two halves of the bar;  'Em/G@0 GIt6@3 F#@6' -> explicit positions."""
    toks = text.split()
    if all("@" in t for t in toks):
        return [(float(t.split("@")[1]), t.split("@")[0]) for t in toks]
    if len(toks) == 1:
        return [(0.0, toks[0])]
    if len(toks) == 2:
        return [(0.0, toks[0]), (bar_len / 2, toks[1])]
    if len(toks) == 4:
        return [(bar_len / 4 * i, t) for i, t in enumerate(toks)]
    raise ValueError(f"give positions for harmony {text!r}")


@dataclass
class Bar:
    number: int
    notes: list
    harmony: list            # [(pos, symbol)]
    pedal: list              # positions of pedal changes inside the bar
    texture: str = ""
    raw: dict = None         # the voice strings as written (for engraving)


class Score:
    def __init__(self, title, bar_len=12.0):
        self.title, self.bar_len, self.bars = title, bar_len, []

    def bar(self, rh, lh, harm, rh2=None, lh2=None, ped=None, texture=""):
        n = len(self.bars) + 1
        s0 = (n - 1) * self.bar_len
        notes = parse_voice(rh, n, "R", "rh", self.bar_len, s0) + parse_voice(lh, n, "L", "lh", self.bar_len, s0)
        if rh2:
            notes += parse_voice(rh2, n, "R", "rh2", self.bar_len, s0)
        if lh2:
            notes += parse_voice(lh2, n, "L", "lh2", self.bar_len, s0)
        harmony = parse_harmony(harm, self.bar_len)
        if ped is None:
            ped = sorted({p for p, _ in harmony} | {0.0, self.bar_len / 2})
        self.bars.append(Bar(n, notes, harmony, list(ped), texture, dict(rh=rh, lh=lh, rh2=rh2, lh2=lh2)))
        return self

    def s(self, bar, pos=0.0):
        return (bar - 1) * self.bar_len + pos

    @property
    def length(self):
        return len(self.bars) * self.bar_len

    def all_notes(self):
        self.assign_roles()
        return sorted((n for b in self.bars for n in b.notes), key=lambda n: (n.s, n.pitch))

    def harmony_at(self, s):
        b = self.bars[min(len(self.bars) - 1, int(s // self.bar_len))]
        pos = s - (b.number - 1) * self.bar_len
        cur = b.harmony[0][1]
        for p, sym in b.harmony:
            if p <= pos + 1e-9:
                cur = sym
        return cur

    def assign_roles(self):
        for b in self.bars:
            rh = [n for n in b.notes if n.voice == "rh"]
            for n in rh:
                top = n.chord_rank == n.chord_size - 1
                if n.grace is not None or n.group is not None or top:
                    n.role = "melody"
                elif b.texture == "duet":
                    n.role = "duet"
                else:
                    n.role = "rh_inner"
            for n in b.notes:
                if n.voice == "rh2":
                    n.role = "duet"
            lh = [n for n in b.notes if n.hand == "L"]
            for n in lh:
                beat = int(n.pos // 3)
                same_beat = [m for m in lh if int(m.pos // 3) == beat]
                low = min(m.pitch for m in same_beat)
                on_beat = abs(n.pos - 3 * beat) < 1e-6
                is_low = n.pitch == low or (n.chord_size > 1 and (n.pitch - low) == 12 and n.chord_rank == 1)
                # a bass note opens a beat and lies below the tenor register
                at_change = any(abs(n.pos - p) < 1e-6 for p, _ in b.harmony) or n.pos in (0.0, 6.0)
                n.role = "bass" if (on_beat and is_low and (n.pitch <= 47 or (at_change and n.pitch <= 50))) else "acc"
                if n.chord_size > 1 and n.dur >= 4 and n.chord_rank == 0:
                    n.role = "bass"
