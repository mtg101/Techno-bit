"""
xm_to_makecode.py - turn a Techno:bit tune (.xm) into a MakeCode Python program.

    python tools/xm_to_makecode.py mods/my_tune.xm
    python tools/xm_to_makecode.py mods/my_tune.xm --base main.py --out mods/my_tune_main.py

Run it from the techno-bit folder (where main.py is).

It takes the base program (main.py: the tracker code with the Tetris tune in it), throws away the base's tune
and puts the tune from the .xm file in its place. Everything else - playing notes, the radio, the buttons,
the LEDs - stays exactly the same. Paste the result into a new MakeCode project and switch to Blocks.

The .xm file has to follow the Techno:bit rules (start from tools/template.xm and you will).
In short (the full rules are in the converter's documentation):
  - 4 or 8 channels. Channels 1-4 = tracks 1-4 (lead, acid, vox, drums). Channels 5-8 = tracks 5-8 (extras).
    With 4 channels, tracks 5-8 play the same as tracks 1-4.
  - 32 rows in every pattern. Speed 12, tempo 150 (one row = 200 ms).
  - Instruments 1-10 as in the template: 1 tone, 2 kick, 3 snare, 4 clap, 5 hat, 6 open hat, 7 crash,
    8 tom (C-4 low / G-4 high), 9 pew (C-4 low / C-5 high), 10 hoover (E-4 / A-4).
  - Tones from C-4 to B-6. No volume column, no effects.
Any problem is reported with its place in the tune (pattern, row, channel) so you can fix it in OpenMPT.
"""
import argparse
import ast
import re
import struct
import sys

TRACKS = ["lead", "acid", "vox", "drums", "bass2", "kit2", "perc", "hits"]     # track 1 = channel 1, ...
LETTERS = ["C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#", "A-", "A#", "B-"]
NOTE_OFF = 97
LOWEST, HIGHEST = 49, 84                         # C-4 and B-6 (XM note numbers: C-0 = 1)
WAVES = {2: "kick", 3: "snare", 4: "clap", 5: "hat", 6: "openhat", 7: "crash"}
TWO_PITCH_WAVES = {8: {49: "tom_lo", 56: "tom_hi"},        # C-4 / G-4
                   9: {49: "pew_lo", 61: "pew_hi"},        # C-4 / C-5
                   10: {53: "hoover_e", 58: "hoover_a"}}   # E-4 / A-4
MAX_CELLS = 10000      # about how many cells fit in the micro:bit V2's flash with the tracker code


class TuneProblem(Exception):
    pass


def note_name(n):
    return LETTERS[(n - 1) % 12] + str((n - 1) // 12)


# ------------------------------------------------------------------ reading the .xm file
def read_xm(path):
    data = open(path, "rb").read()
    if not data.startswith(b"Extended Module: "):
        raise TuneProblem(f"{path} is not an .xm file")
    header_size = struct.unpack("<I", data[60:64])[0]
    song_len, _restart, channels, n_patterns, n_instruments, _flags, speed, tempo = \
        struct.unpack("<8H", data[64:80])
    order = list(data[80:80 + song_len])
    problems, warnings = [], []
    if channels not in (4, 8):
        problems.append(f"the tune has {channels} channels: it needs 4 or 8")
    if (speed, tempo) != (12, 150):
        warnings.append(f"speed {speed} / tempo {tempo}: the micro:bits always play speed 12 / tempo 150")
    pos = 60 + header_size
    patterns = []
    for p in range(n_patterns):
        head_len, _packing, rows, size = struct.unpack("<IBHH", data[pos:pos + 9])
        pos += head_len
        end = pos + size
        grid = [[(0, 0, 0, 0)] * channels for _ in range(rows)]
        r = c = 0
        while pos < end:                              # packed pattern data
            b = data[pos]; pos += 1
            note = inst = vol = fx = fxp = 0
            if b & 0x80:
                if b & 1: note = data[pos]; pos += 1
                if b & 2: inst = data[pos]; pos += 1
                if b & 4: vol = data[pos]; pos += 1
                if b & 8: fx = data[pos]; pos += 1
                if b & 16: fxp = data[pos]; pos += 1
            else:
                note, inst, vol, fx, fxp = b, data[pos], data[pos + 1], data[pos + 2], data[pos + 3]
                pos += 4
            if r < rows:
                grid[r][c] = (note, inst, vol, fx or fxp)
            c += 1
            if c == channels:
                c, r = 0, r + 1
        if size == 0:                                 # an empty pattern is stored with no data
            grid = [[(0, 0, 0, 0)] * channels for _ in range(rows)]
        if rows != 32:
            problems.append(f"pattern {p} has {rows} rows: every pattern needs 32")
        patterns.append(grid)
        pos = end
    for k, p in enumerate(order):
        if p >= n_patterns:
            problems.append(f"order list position {k} plays pattern {p}, which doesn't exist")
    return dict(channels=channels, order=order, patterns=patterns, problems=problems, warnings=warnings)


def to_cell(note, inst, vol, fx, where, problems):
    """One XM cell -> one Techno:bit cell: 'tone D-6', 'wave kick', 'x' or '-'."""
    if vol or fx:
        problems.append(f"{where}: volume or effect used (the micro:bits have neither)")
    if note == 0 and inst == 0:
        return "-"
    if note == NOTE_OFF:
        return "x"
    if note == 0:
        problems.append(f"{where}: an instrument with no note")
        return "-"
    if inst == 0:
        problems.append(f"{where}: note {note_name(note)} has no instrument")
        return "-"
    if inst == 1:
        if not LOWEST <= note <= HIGHEST:
            problems.append(f"{where}: tone {note_name(note)} is out of range (C-4 to B-6)")
            return "-"
        return "tone " + note_name(note)
    if inst in WAVES:
        return "wave " + WAVES[inst]
    if inst in TWO_PITCH_WAVES:
        names = TWO_PITCH_WAVES[inst]
        if note not in names:
            allowed = " or ".join(note_name(n) for n in names)
            problems.append(f"{where}: instrument {inst} only plays {allowed}, not {note_name(note)}")
            return "-"
        return "wave " + names[note]
    problems.append(f"{where}: instrument {inst} isn't one of the 10 Techno:bit instruments")
    return "-"


def tune_cells(xm):
    """cells[track][pattern] = list of 32 cells, for the channels in the file."""
    problems = xm["problems"]
    cells = []
    for ch in range(xm["channels"]):
        track = []
        for p, grid in enumerate(xm["patterns"]):
            column = []
            for r, row in enumerate(grid[:32]):
                where = f"pattern {p}, row {r}, channel {ch + 1}"
                column.append(to_cell(*row[ch], where, problems))
            column += ["-"] * (32 - len(column))
            track.append(column)
        cells.append(track)
    return cells


# ------------------------------------------------------------------ writing the MakeCode Python
def as_list(items, quote=True):
    items = [f'"{i}"' if quote else str(i) for i in items]
    return "[" + ",\n        ".join(items) + "]"


def song_code(xm, cells):
    n = len(xm["patterns"])
    own = xm["channels"]                     # tracks with their own arrays: 4 or 8
    names = lambda t: [f"{TRACKS[t]}_{p:02d}" for p in range(n)]
    funcs = []
    for t in range(own):
        f = f"def create_{TRACKS[t]}_patterns():\n    global {', '.join(names(t))}\n"
        for p in range(n):
            f += f"    {names(t)[p]} = {as_list(cells[t][p])}\n"
        funcs.append(f)
    lists = [f"    patterns_metronome = {as_list(['track_metronome'] * n, quote=False)}\n"]
    for t in range(8):
        source = t if t < own else t - 4     # with 4 channels: track 5 plays track 1's patterns, and so on
        lists.append(f"    patterns_{TRACKS[t]} = {as_list(names(source), quote=False)}\n")
    all_lists = ["patterns_metronome"] + [f"patterns_{t}" for t in TRACKS]
    f = "def create_patterns():\n    global " + ", ".join(all_lists + ["song_tracks"]) + "\n"
    f += "    create_track_metronome()\n"
    f += "".join(f"    create_{TRACKS[t]}_patterns()\n" for t in range(own))
    f += "".join(lists)
    f += f"    song_tracks = {as_list(all_lists, quote=False)}\n"
    funcs.append(f)
    funcs.append(f"def create_song():\n    global song\n    song = {as_list(xm['order'], quote=False)}\n")
    decls = "".join(f"{v}: List[str] = []\n" for t in range(own) for v in names(t))
    decls += "".join(f"{v}: List[List[str]] = []\n" for v in all_lists)
    decls += "song_tracks: List[List[List[str]]] = []\nsong: List[number] = []\n"
    return "".join(funcs), decls


SONG_FUNC = re.compile(r"^create_(\w+_patterns|patterns|song)$")
SONG_VAR = re.compile(r"^((%s)_\d+|patterns_\w+|song_tracks|song)$" % "|".join(TRACKS))
KEEP = {"create_track_metronome"}


def is_song_part(node):
    if isinstance(node, ast.FunctionDef):
        return node.name not in KEEP and bool(SONG_FUNC.match(node.name))
    if isinstance(node, ast.AnnAssign):
        return bool(SONG_VAR.match(getattr(node.target, "id", "")))
    return False


def put_song_in(base, funcs, decls):
    """Remove the base's song (functions and declarations) and put the new one in its place."""
    lines = base.replace("\r\n", "\n").split("\n")
    tree = ast.parse("\n".join(lines))
    remove = set()
    first_decl = None
    for node in tree.body:
        if is_song_part(node):
            remove.update(range(node.lineno - 1, node.end_lineno))
        if first_decl is None and isinstance(node, (ast.Assign, ast.AnnAssign)):
            first_decl = node.lineno - 1
    out = []
    for i, line in enumerate(lines):
        if i == first_decl:
            out.append(funcs + decls.rstrip("\n"))
        if i not in remove:
            out.append(line)
    code = "\n".join(out)
    ast.parse(code)                          # still valid Python
    return code


def convert(xm_path, base_path, out_path):
    xm = read_xm(xm_path)
    cells = tune_cells(xm)
    for w in xm["warnings"]:
        print("warning:", w)
    if xm["problems"]:
        print(f"{xm_path}: {len(xm['problems'])} problem(s) to fix first:")
        for p in xm["problems"][:40]:
            print("  -", p)
        if len(xm["problems"]) > 40:
            print(f"  ... and {len(xm['problems']) - 40} more")
        return False
    n_cells = xm["channels"] * len(xm["patterns"]) * 32
    if n_cells > MAX_CELLS:
        print(f"warning: {n_cells} cells - more than about {MAX_CELLS} may not fit on the micro:bit")
    funcs, decls = song_code(xm, cells)
    code = put_song_in(open(base_path).read(), funcs, decls)
    open(out_path, "w", newline="").write(code.replace("\n", "\r\n"))      # Windows line endings, like MakeCode
    print(f"wrote {out_path}: {xm['channels']} tracks, {len(xm['patterns'])} patterns, "
          f"song of {len(xm['order'])} patterns ({len(xm['order']) * 32 * 0.2 / 60:.1f} minutes)")
    return True


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Turn a Techno:bit .xm tune into a MakeCode Python program.")
    ap.add_argument("xm", help="the tune (.xm)")
    ap.add_argument("--base", default="main.py", help="the base program (default: main.py)")
    ap.add_argument("--out", help="where to write (default: the tune's name with _main.py)")
    a = ap.parse_args()
    out = a.out or re.sub(r"\.xm$", "", a.xm, flags=re.I) + "_main.py"
    try:
        ok = convert(a.xm, a.base, out)
    except TuneProblem as e:
        print("problem:", e)
        ok = False
    sys.exit(0 if ok else 1)
