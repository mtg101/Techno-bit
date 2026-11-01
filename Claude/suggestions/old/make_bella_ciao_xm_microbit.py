"""
BELLA CIAO - chiptune techno, for 4 micro:bits. Same setup and the same 10 instruments as the other tunes.

"Bella Ciao" is a traditional Italian folk song; only the traditional melody is used here (no lyrics, no modern
arrangement). The melody was checked against 8notes.com's violin MIDI (there in B minor) and moved to A minor,
so the Hoover's two pitches (A and E) are the key note and its fifth. Every note of the verse falls on the
eighth-note grid, so nothing is rounded.

The verse is 8 bars = 2 patterns. The hook ("bella ciao, bella ciao, bella ciao ciao ciao") is bars 3-4.
Chords per half bar (8 per pattern): Am x7, A7 | A7, Dm, Dm, Am, Am, E7, E7, Am.

Setup (unchanged): 4 channels, 32 rows per pattern = 4 bars of eighth notes, speed 12 / tempo 150,
16 patterns, a 64-slot order list, no volume column, no effects, 10 instruments:
  1 Tone  2 Kick  3 Snare  4 Clap  5 Hat  6 Open hat  7 Crash  8 Tom (C-4 low / G-4 high)
  9 Pew zap (C-4 / C-5)  10 Hoover (E-4 / A-4)
Pitched parts between C-4 and B-6; lead and voice Tone no lower than E-4 (micro:bit V2 speaker).
Pattern names and the song order follow Korobeiniki's: INT1 INT2 VA1 VA2 A1 A2 A1x A2x B1 B2 BR1 BR2 BU1 BU2 RLD OUT.

Channels: 1 LEAD (tune)  2 ACID (bass)  3 VOX (second percussion lane, Hoover stabs, pings)  4 DRUMS

Usage: python3 make_bella_ciao_xm_microbit.py [output.xm]
"""
import math
import random
import struct
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "bella_ciao_techno_4ch_microbit.xm"

# ------------------------------------------------------------------ config
SPEED, BPM = 12, 150          # 12 ticks/row @ tempo 150 => 1 row = 1 eighth note (0.2 s)
BASS_OCT = 4                 # micro:bit V2 speaker has no real bass: lowest bass note = C4 (262 Hz)
CHANNELS = 4
ROWS_PER_BAR = 8              # eighth-note resolution
ROWS_PER_PATTERN = 32        # = 4 bars at eighth-note resolution
TOTAL_ROWS = ROWS_PER_PATTERN      # scratch grid = one pattern at a time

LEAD, ACID, VOX, DRUMS = range(4)
(I_SQ, I_KICK, I_SNARE, I_CLAP, I_HAT,
 I_OHAT, I_CRASH, I_TOM, I_ZAP, I_HOOVER) = range(1, 11)
I_KCLAP, I_KCRASH = I_CLAP, I_CRASH            # beats 2/4 = clap alone; drop downbeat = crash alone
I_P12 = I_SAW = I_ACID = I_ACID_ACC = I_SQ     # every pitched part uses the one Tone instrument

# volume-column levels (0-64)
V_LEAD, V_HOOVER, V_ACID, V_ACID_ACC = 52, 40, 50, 64
V_KICK, V_SNARE, V_HAT, V_OHAT, V_CRASH = 64, 52, 28, 32, 60

# ------------------------------------------------------------------ notes
NOTE_OFF = 97
SEMI = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def N(name):
    """'C4' -> XM note number (C-0 = 1, C-4 = 49). Supports sharps: 'G#4'."""
    i, sharp = 1, 0
    if name[1] == "#":
        sharp, i = 1, 2
    return int(name[i:]) * 12 + SEMI[name[0]] + sharp + 1


# ------------------------------------------------------------------ samples
DRUM_RATE = 16726            # drums are rendered at 2x 8363 Hz and played with relative note +12
rng = random.Random(1985)


def clamp8(v):
    return max(-127, min(127, int(round(v))))


def normalise(vals, peak):
    m = max(abs(v) for v in vals) or 1
    return [clamp8(v * peak / m) for v in vals]


def fade_tail(vals, n):
    n = min(n, len(vals))
    for i in range(n):
        vals[len(vals) - 1 - i] *= i / n
    return vals


def cycle(kind, n=32, peak=100):
    """One-cycle looping waveform. 32 samples at C-4 (8363 Hz) = ~261 Hz = C4."""
    v = []
    for i in range(n):
        p = i / n
        if kind == "square":
            s = 1 if p < 0.5 else -1
        elif kind == "pulse25":
            s = 1 if p < 0.25 else -1
        elif kind == "pulse12":
            s = 1 if p < 0.125 else -1
        elif kind == "tri":
            s = 1 - 4 * abs(p - 0.5)
        elif kind == "saw":
            s = 2 * p - 1
        else:
            raise ValueError(kind)
        v.append(s)
    mean = sum(v) / n
    return normalise([s - mean for s in v], peak)


def make_kick():
    """Speaker-friendly kick: a short downward sweep 520 -> 170 Hz in ~100 ms plus a click.
    (The V2 speaker can't reproduce real kick-drum low end, so we don't pretend.)"""
    n, phase, out = int(DRUM_RATE * 0.12), 0.0, []
    for i in range(n):
        t = i / DRUM_RATE
        phase += 2 * math.pi * (170 + 350 * math.exp(-t * 40)) / DRUM_RATE
        click = rng.uniform(-1, 1) * math.exp(-t * 500) * 0.4
        out.append(math.tanh(1.8 * (math.sin(phase) * math.exp(-t * 22) + click)))
    return normalise(fade_tail(out, 150), 125)


def make_snare():
    """Speaker-friendly snare: mostly noise burst (~140 ms) with a short 400 Hz tone on the front."""
    n, out, prev = int(DRUM_RATE * 0.14), [], 0.0
    for i in range(n):
        t = i / DRUM_RATE
        tone = math.sin(2 * math.pi * 400 * t) * math.exp(-t * 45)
        x = rng.uniform(-1, 1)
        noise = (x - prev * 0.5) * math.exp(-t * 22)
        prev = x
        out.append(math.tanh(1.6 * (tone * 0.4 + noise)))
    return normalise(fade_tail(out, 200), 118)


def make_clap():
    """909-style clap: a few quick noise bursts then a tail, band-passed."""
    n = int(DRUM_RATE * 0.30)
    bursts = (0.0, 0.011, 0.022, 0.034)
    a1 = 1 - math.exp(-2 * math.pi * 3200 / DRUM_RATE)
    a2 = 1 - math.exp(-2 * math.pi * 700 / DRUM_RATE)
    l1 = l2 = 0.0
    out = []
    for i in range(n):
        t = i / DRUM_RATE
        env = 0.0
        for bt in bursts[:-1]:
            if t >= bt:
                env = max(env, math.exp(-(t - bt) * 220))
        if t >= bursts[-1]:
            env = max(env, math.exp(-(t - bursts[-1]) * 17))
        x = rng.uniform(-1, 1) * env
        l1 += a1 * (x - l1)
        l2 += a2 * (x - l2)
        out.append(math.tanh(2.2 * (l1 - l2)))
    return normalise(fade_tail(out, 300), 118)


HAT_FREQS = (263, 400, 421, 474, 587, 845)      # six detuned squares = metallic hat


def metallic(t):
    return sum(1.0 if math.sin(2 * math.pi * f * t) >= 0 else -1.0 for f in HAT_FREQS) / 6


def make_hat(length_s, decay):
    n, l, out = int(DRUM_RATE * length_s), 0.0, []
    a = 1 - math.exp(-2 * math.pi * 3500 / DRUM_RATE)
    for i in range(n):
        t = i / DRUM_RATE
        x = metallic(t) * 0.8 + rng.uniform(-1, 1) * 0.5
        l += a * (x - l)
        out.append((x - l) * math.exp(-t * decay))        # high-passed
    return normalise(fade_tail(out, 60), 95)


def make_crash():
    n, l, out = int(DRUM_RATE * 1.5), 0.0, []
    a = 1 - math.exp(-2 * math.pi * 2500 / DRUM_RATE)
    for i in range(n):
        t = i / DRUM_RATE
        x = metallic(t) * 0.6 + rng.uniform(-1, 1) * 0.7
        l += a * (x - l)
        out.append((x - l) * math.exp(-t * 2.4) * (0.6 + 0.4 * math.exp(-t * 20)))
    return normalise(fade_tail(out, 500), 105)


def make_tom():
    """Low tom (played at C-4): sweep 420 -> 240 Hz. The high tom is the same sample at G-4 (1.5x = 630 -> 360 Hz)."""
    n, phase, out = int(DRUM_RATE * 0.20), 0.0, []
    for i in range(n):
        t = i / DRUM_RATE
        phase += 2 * math.pi * (240 + 180 * math.exp(-t * 18)) / DRUM_RATE
        v = math.sin(phase) * math.exp(-t * 14) + rng.uniform(-1, 1) * math.exp(-t * 500) * 0.25
        out.append(math.tanh(1.6 * v))
    return normalise(fade_tail(out, 200), 115)


def make_acid(accent=False):
    """TB-303-ish: saw -> two resonant low-pass stages with a fast cutoff envelope.
    Rendered with 128 samples per cycle at 110 Hz (A2): play it with relative note +24.
    Note start = the squelchy filter sweep; after that it holds a steady, darker tone (the loop),
    which is also what you hear on slid notes (a 303 doesn't re-trigger its envelope on slides)."""
    fs, f0, spc, OS = 14080.0, 110.0, 128, 4
    peak, base = (4200.0, 420.0) if accent else (2700.0, 260.0)
    tau = 0.045 if accent else 0.08
    damp1 = 0.09 if accent else 0.13              # lower = more resonance
    damp2, drive = 0.8, (2.4 if accent else 1.5)
    intro_n, settle_n = int(fs * 0.45), spc * 6
    phase = 0.0
    l1 = b1 = l2 = b2 = 0.0
    raw = []
    for n in range(intro_n + settle_n + spc):
        fc = base + (peak - base) * math.exp(-(n / fs) / tau) if n < intro_n else base
        f = 2 * math.sin(math.pi * fc / (fs * OS))
        phase = (phase + f0 / fs) % 1.0
        x = 2 * phase - 1
        acc = 0.0
        for _ in range(OS):
            l1 += f * b1
            b1 += f * (x - l1 - damp1 * b1)
            l2 += f * b2
            b2 += f * (l1 - l2 - damp2 * b2)
            acc += l2
        raw.append(acc / OS)
    m = max(abs(v) for v in raw) or 1
    shaped = [math.tanh(drive * v / m) for v in raw]
    return normalise(shaped, 110), intro_n + settle_n


def make_hoover():
    """Alpha-Juno-style 'What the' hoover: 3 detuned saws + a sub saw, with a pitch dive at the
    start of every note. Returns (data, loop_start). The loop is seamless: every saw has a whole
    number of cycles in the 2048-sample loop (64 cycles = base pitch, 62/66 = about +/-27 cents)."""
    rate, L = 8363.0, 2048
    comps = [(62, 1.0), (64, 1.0), (66, 1.0), (32, 0.9)]      # (cycles per loop, weight)
    T = int(rate * 0.14)                                      # length of the dive
    ph = [0.0] * len(comps)
    out = []
    for n in range(T):
        x = n / T
        k = 2 ** ((9 * (1 - x) ** 2) / 12)                    # starts 9 semitones up, glides to pitch
        v = 0.0
        for j, (m, w) in enumerate(comps):
            ph[j] = (ph[j] + (m / L) * k) % 1.0
            v += w * (2 * ph[j] - 1)
        out.append(v * min(1.0, n / 60))                      # short attack
    for n in range(L):
        v = 0.0
        for j, (m, w) in enumerate(comps):
            v += w * (2 * ((ph[j] + m * (n + 1) / L) % 1.0) - 1)
        out.append(v)
    return normalise(out, 100), T


def make_zap():
    """Laser 'pew' (played at C-4): square sweep 1500 -> 350 Hz in ~160 ms. At C-5 it is the high, faster pew
    (3000 -> 700 Hz)."""
    n, phase, out = int(DRUM_RATE * 0.16), 0.0, []
    for i in range(n):
        t = i / DRUM_RATE
        phase += 2 * math.pi * (350 + 1150 * math.exp(-t * 25)) / DRUM_RATE
        out.append((1.0 if math.sin(phase) >= 0 else -1.0) * math.exp(-t * 14))
    return normalise(fade_tail(out, 150), 100)


_hoover, _hoover_loop_start = make_hoover()

# (name, data, loops?, relative note, panning[, loop start])
SAMPLES = [
    ("Tone (square)", cycle("square"),     True,  0,  128),
    ("Kick",          make_kick(),         False, 12, 128),
    ("Snare",         make_snare(),        False, 12, 128),
    ("Clap",          make_clap(),         False, 12, 128),
    ("Hat",           make_hat(0.07, 60),  False, 12, 128),
    ("Open hat",      make_hat(0.32, 9),   False, 12, 128),
    ("Crash",         make_crash(),        False, 12, 128),
    ("Tom",           make_tom(),          False, 12, 128),
    ("Pew zap",       make_zap(),          False, 12, 128),
    ("Hoover",        _hoover,             True,  0,  128, _hoover_loop_start),
]


def delta(data):
    prev, out = 0, bytearray()
    for v in data:
        out.append((v - prev) & 0xFF)
        prev = v
    return bytes(out)


def instrument_bytes(name, data, loop, relnote, pan, loop_start=0):
    nm = name.encode("ascii")[:22].ljust(22, b"\0")
    h = struct.pack("<I22sBH", 263, nm, 0, 1)      # header size, name, type, num samples
    h += struct.pack("<I", 40)                      # sample header size
    h += bytes(96)                                  # note -> sample map (all sample 0)
    h += bytes(48) + bytes(48)                      # volume / panning envelope points
    h += bytes(8)                                   # env point counts, sustain/loop points
    h += bytes(2)                                   # envelope types (none)
    h += bytes(4)                                   # auto-vibrato
    h += struct.pack("<H", 0)                       # volume fadeout
    h += bytes(22)                                  # reserved
    assert len(h) == 263
    length = len(data)
    ls, ll, typ = (loop_start, length - loop_start, 1) if loop else (0, 0, 0)
    sh = struct.pack("<IIIBbBBbB22s", length, ls, ll, 64, 0, typ, pan, relnote, 0, nm)
    assert len(sh) == 40
    return h + sh + delta(data)


# ------------------------------------------------------------------ composing
# ONE ROW = ONE EIGHTH NOTE. 8 rows per bar, 2 per beat, 32 per pattern (4 bars).
grid = [[None] * ROWS_PER_PATTERN for _ in range(CHANNELS)]
PATTERNS = {}


def new_pattern():
    global grid
    grid = [[None] * ROWS_PER_PATTERN for _ in range(CHANNELS)]


def R(bar, row=0):
    return bar * ROWS_PER_BAR + row


def put(ch, row, note, inst, vol=0):
    if 0 <= row < ROWS_PER_PATTERN:
        grid[ch][row] = (note, inst, 0)      # no volume column: every note plays at full sample volume


def off(ch, row, force=True):
    if 0 <= row < ROWS_PER_PATTERN and (force or grid[ch][row] is None):
        grid[ch][row] = (NOTE_OFF, 0, 0)


def finish_pattern(name):
    """Store the pattern. Self-contained: a tone channel with nothing on row 0 is cut there, so no
    note leaks in from whatever pattern played before."""
    for ch in (LEAD, ACID, VOX):
        if grid[ch][0] is None:
            grid[ch][0] = (NOTE_OFF, 0, 0)
    PATTERNS[name] = grid


C4 = N("C4")

# ================================================================ BELLA CIAO
CHORDS = {"Am": ("A", [0, 3, 7]), "A7": ("A", [0, 4, 7]), "Dm": ("D", [0, 3, 7]), "E7": ("E", [0, 4, 7])}
ROOT = {"Am": N("A4"), "A7": N("A4"), "Dm": N("D4"), "E7": N("E4")}
HALF = ROWS_PER_BAR // 2
VOICE_FLOOR = N("E4")

# The verse: (start row, length in rows, note), 64 rows = 8 bars. From the MIDI, moved to A minor, lead octave.
VERSE = [(0, 1, "E5"), (1, 1, "A5"), (2, 1, "B5"), (3, 1, "C6"), (4, 4, "A5"),
         (8, 1, "E5"), (9, 1, "A5"), (10, 1, "B5"), (11, 1, "C6"), (12, 4, "A5"),
         (16, 1, "E5"), (17, 1, "A5"), (18, 1, "B5"), (19, 2, "C6"), (21, 1, "B5"), (22, 1, "A5"), (23, 2, "C6"),
         (25, 1, "B5"), (26, 1, "A5"), (27, 2, "E6"), (29, 2, "E6"), (31, 1, "E6"),
         (32, 1, "E6"), (33, 1, "D6"), (34, 1, "E6"), (35, 1, "F6"), (36, 4, "F6"),
         (40, 1, "F6"), (41, 1, "E6"), (42, 1, "D6"), (43, 1, "F6"), (44, 3, "E6"),
         (48, 1, "E6"), (49, 1, "D6"), (50, 1, "C6"), (51, 1, "B5"), (53, 1, "E6"), (55, 1, "B5"), (57, 1, "C6"),
         (59, 5, "A5")]
PROG = ["Am"] * 7 + ["A7", "A7", "Dm", "Dm", "Am", "Am", "E7", "E7", "Am"]       # 16 half bars
assert len(PROG) == 16
HOOK = [(r - 16, l, n) for r, l, n in VERSE if 16 <= r < 32]                 # bars 3-4, 16 rows
PROG_HOOK = PROG[4:8]


def part(events, r0, r1):
    """The events that start in rows [r0, r1), moved so r0 is row 0."""
    return [(r - r0, l, n) for r, l, n in events if r0 <= r < r1]


def melody(ch, events, shift=0):
    """Place notes; where a note ends before the next one starts, close it with a note-off."""
    ev = sorted(events)
    for i, (r, l, n) in enumerate(ev):
        put(ch, r, N(n) + shift, I_SQ)
        nxt = ev[i + 1][0] if i + 1 < len(ev) else None
        end = r + l
        if nxt is None or end < nxt:
            off(ch, end, force=False)


def chord_notes(name, octave):
    root, iv = CHORDS[name]
    base = N(root + str(octave))
    while base < VOICE_FLOOR:
        base += 12
    return [base + i for i in iv]


def hoover_note(chord):
    """2 pitches only: E-4 over E7, A-4 over everything else."""
    return N("E4") if chord == "E7" else N("A4")


SOUND = {"lo": (N("C4"), I_TOM), "hi": (N("G4"), I_TOM), "clap": (C4, I_CLAP), "hat": (C4, I_HAT),
         "ohat": (C4, I_OHAT), "crash": (C4, I_CRASH), "kick": (C4, I_KICK), "snare": (C4, I_SNARE)}


def hit(ch, row, what):
    note, inst = SOUND[what]
    put(ch, row, note, inst)


BASS_STYLES = {
    "hold":  [(0, 0), None, None, "off"],
    "beat":  [(0, 0), "off", (0, 0), "off"],
    "off":   ["off", (0, 0), "off", (0, 0)],
    "drive": [(0, 0), (0, 0), (0, 1), (0, 0)],
    "roll":  [(0, 0), (0, 1), (7, 0), (0, 1)],
    "pump":  [(0, 0), (0, 1), (0, 0), (0, 1)],
}


def bass(pos, chord, style, last=HALF):
    base = pos * HALF
    for k, step in enumerate(BASS_STYLES[style][:last]):
        if step is None:
            continue
        if step == "off":
            off(ACID, base + k)
        else:
            semis, octv = step
            put(ACID, base + k, ROOT[chord] + semis + 12 * octv, I_ACID)


def bass_line(prog, style, fill=False):
    for pos, c in enumerate(prog):
        if fill and pos == 7:
            bass(pos, c, style, last=2)
            off(ACID, pos * HALF + 2)
        else:
            bass(pos, c, style)


def pings(pos, chord):
    tones = chord_notes(chord, 5)
    for k, t in ((1, 0), (3, 2)):
        put(VOX, pos * HALF + k, tones[t], I_P12)
        off(VOX, pos * HALF + k + 1, force=False)


def arp(pos, chord, octave=4):
    tones = chord_notes(chord, octave)
    for k, t in enumerate((0, 1, 2, 1)):
        put(VOX, pos * HALF + k, tones[t], I_P12)


def kick_hats(bar, hat="hat", every_beat=True, clap=False, last=ROWS_PER_BAR):
    for r in range(min(ROWS_PER_BAR, last)):
        if r % 2 == 0:
            if clap and r in (2, 6):
                hit(DRUMS, R(bar, r), "clap")
            elif every_beat or r in (0, 4):
                hit(DRUMS, R(bar, r), "kick")
        elif hat:
            hit(DRUMS, R(bar, r), hat)


def perc_bar(bar, prog, crash=False, ghost=False, stabs=True, fill=False):
    """VOX lane: crash or hat on 1, clap on 2 and 4, hat on 3, Hoover stabs on the offbeats of 2 and 4."""
    hit(VOX, R(bar, 0), "crash" if crash else "hat")
    hit(VOX, R(bar, 2), "clap")
    if stabs:
        put(VOX, R(bar, 3), hoover_note(prog[2 * bar]), I_HOOVER)
    else:
        hit(VOX, R(bar, 3), "hat")
    if ghost and not fill:
        hit(VOX, R(bar, 1), "snare")
        hit(VOX, R(bar, 5), "snare")
    if fill:
        for q, p in enumerate(("C4", "C4", "C5", "C5")):
            put(VOX, R(bar, 4 + q), N(p), I_ZAP)
        return
    hit(VOX, R(bar, 4), "hat")
    hit(VOX, R(bar, 6), "clap")
    if stabs:
        put(VOX, R(bar, 7), hoover_note(prog[2 * bar + 1]), I_HOOVER)
    else:
        hit(VOX, R(bar, 7), "hat")


def fill_drums(bar):
    kick_hats(bar, "ohat", last=4)
    for r, what in ((4, "kick"), (5, "snare"), (6, "hi"), (7, "lo")):
        hit(DRUMS, R(bar, r), what)


def roll_bar(bar, level, last=ROWS_PER_BAR):
    for r in range(min(ROWS_PER_BAR, last)):
        if level == 1:
            what = "snare" if r in (3, 7) else ("kick" if r % 2 == 0 else None)
        elif level == 2:
            what = "kick" if r % 2 == 0 else "snare"
        else:
            what = "kick" if r in (0, 4) else "snare"
        if what:
            hit(DRUMS, R(bar, r), what)


def finish(name):
    finish_pattern(name)


# ================================================================ the 16 patterns
# ---- INT1: kick + hats, offbeat pings, bass on the beat (Am)
new_pattern()
for b in range(4):
    kick_hats(b, "hat", every_beat=False)
for pos in range(8):
    bass(pos, "Am", "beat")
    pings(pos, "Am")
finish("INT1")

# ---- INT2: + claps, offbeat bass, arpeggio with Hoover stabs; the last bar teases "ciao ciao ciao"
new_pattern()
for b in range(4):
    kick_hats(b, "hat", clap=True)
for pos in range(8):
    c = "Am" if pos < 6 else "A7"
    bass(pos, c, "off")
    if pos < 6:
        arp(pos, c)
for b in range(3):
    for k in (3, 7):
        put(VOX, R(b, k), N("A4"), I_HOOVER)
melody(LEAD, [(r + 27, l, n) for r, l, n in part(HOOK, 11, 16)])   # "ciao ciao ciao" at the very end
finish("INT2")


# ---- VA1 VA2: the verse over the two-lane kit (kick on 1 and 3)
def verse_pat(name, k):
    new_pattern()
    melody(LEAD, part(VERSE, 32 * k, 32 * (k + 1)))
    prog = PROG[8 * k: 8 * (k + 1)]
    for b in range(4):
        kick_hats(b, "ohat", every_beat=False)
        perc_bar(b, prog, crash=(k == 0 and b == 0), stabs=(k == 1))
    bass_line(prog, "beat")
    finish(name)


verse_pat("VA1", 0)
verse_pat("VA2", 1)


# ---- A1 A2 A1x A2x: the verse as a drop
def drop_pat(name, k, style, hat, ghost=False):
    new_pattern()
    melody(LEAD, part(VERSE, 32 * k, 32 * (k + 1)))
    prog = PROG[8 * k: 8 * (k + 1)]
    fill = (k == 1)
    for b in range(4):
        if fill and b == 3:
            fill_drums(b)
        else:
            kick_hats(b, hat)
        perc_bar(b, prog, crash=(b == 0), ghost=ghost, fill=(fill and b == 3))
    bass_line(prog, style, fill=fill)
    finish(name)


drop_pat("A1", 0, "drive", "ohat")
drop_pat("A2", 1, "drive", "ohat")
drop_pat("A1x", 0, "roll", "hat", ghost=True)
drop_pat("A2x", 1, "roll", "hat", ghost=True)


# ---- B1 B2: the hook drop - "bella ciao, bella ciao, bella ciao ciao ciao" chopped and looped
def hook_pat(name, second, style):
    new_pattern()
    ev = HOOK + ([(r + 16, l, n) for r, l, n in part(VERSE, 48, 64)] if second else [(r + 16, l, n) for r, l, n in HOOK])
    melody(LEAD, ev)
    prog = PROG_HOOK + (PROG[12:16] if second else PROG_HOOK)
    for b in range(4):
        if second and b == 3:
            fill_drums(b)
        else:
            kick_hats(b, "ohat")
        perc_bar(b, prog, crash=(b in (0, 2)), ghost=True, fill=(second and b == 3))
    bass_line(prog, style, fill=second)
    finish(name)


hook_pat("B1", False, "roll")
hook_pat("B2", True, "roll")


# ---- BR1 BR2: breakdown - no drums, the verse over held bass and a quiet arpeggio
def break_pat(name, k):
    new_pattern()
    melody(LEAD, part(VERSE, 32 * k, 32 * (k + 1)))
    prog = PROG[8 * k: 8 * (k + 1)]
    for pos, c in enumerate(prog):
        bass(pos, c, "hold")
        arp(pos, c, 5)
    finish(name)


break_pat("BR1", 0)
break_pat("BR2", 1)

# ---- BU1 BU2: the 8-bar build - "ciao" stutter climbing A5 C6 E6 A6, pew-pews, snare roll, octave pump,
#      then one beat of silence
BUILD_ROWS = 2 * ROWS_PER_PATTERN - 2
CLIMB = ["A5", "A5", "C6", "C6", "E6", "E6", "A6", "A6"]
STEP = (2, 2, 1, 1, 1, 1, 1, 1)
ZAP_RATE = ((4, 1), (4, 1), (2, 1), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0))
trig = [g for g in range(BUILD_ROWS)
        if (g % ROWS_PER_BAR) % ZAP_RATE[g // ROWS_PER_BAR][0] == ZAP_RATE[g // ROWS_PER_BAR][1]]
zap_at = {g: (N("C4"), N("C5"))[int(n / len(trig) * 2)] for n, g in enumerate(trig)}
BUILD_PROG = ["Am"] * 8 + ["Dm", "Dm", "Dm", "Dm", "E7", "E7", "E7", "E7"]
for k in range(2):
    new_pattern()
    for b in range(4):
        i = 4 * k + b
        last = 6 if i == 7 else ROWS_PER_BAR
        if i < 2:
            kick_hats(b, "hat", every_beat=False)
        else:
            roll_bar(b, (1, 1, 2, 2, 3, 3)[i - 2], last)
    prog = BUILD_PROG[8 * k: 8 * (k + 1)]
    for pos, c in enumerate(prog):
        if k == 1 and pos == 7:
            bass(pos, c, "pump", last=2)
        else:
            bass(pos, c, "beat" if k == 0 else "pump")
    for rr in range(ROWS_PER_PATTERN):
        g = k * ROWS_PER_PATTERN + rr
        if g >= BUILD_ROWS:
            break
        bi = g // ROWS_PER_BAR
        if (g - bi * ROWS_PER_BAR) % STEP[bi] == 0:
            put(LEAD, rr, N(CLIMB[bi]), I_SQ)
        if g in zap_at:
            put(VOX, rr, zap_at[g], I_ZAP)
    if k == 1:
        for ch in range(CHANNELS):
            off(ch, BUILD_ROWS - ROWS_PER_PATTERN)
    finish(f"BU{k + 1}")

# ---- RLD: reload - held Hoover + the first line of the verse, then a quick mini-build and a silent beat
new_pattern()
melody(LEAD, part(VERSE, 0, 16))
for b in (0, 1):
    put(VOX, R(b), N("A4"), I_HOOVER)
    off(VOX, R(b, ROWS_PER_BAR - 1))
for pos in range(4):
    bass(pos, "Am", "hold")
RLD_ROWS = ROWS_PER_PATTERN - 2
for b in (2, 3):
    roll_bar(b, (2, 3)[b - 2], 6 if b == 3 else ROWS_PER_BAR)
for pos in range(4, 8):
    bass(pos, "E7", "pump", last=2 if pos == 7 else HALF)
for rr in range(2 * ROWS_PER_BAR, RLD_ROWS):
    t = (rr - 2 * ROWS_PER_BAR) / (RLD_ROWS - 2 * ROWS_PER_BAR)
    put(LEAD, rr, N("E6") if rr < 3 * ROWS_PER_BAR else N("A6"), I_SQ)
    put(VOX, rr, (N("C4"), N("C5"))[int(t * 2)], I_ZAP)
for ch in range(CHANNELS):
    off(ch, RLD_ROWS)
finish("RLD")

# ---- OUT: the last "ciao ciao" and the final A, then the kick fades out
new_pattern()
melody(LEAD, part(VERSE, 53, 64))                   # "...ciao, ciao" and the final A
for pos in (0, 1, 2):
    bass(pos, "Am", "hold")
    pings(pos, "Am")
kick_hats(0, "hat")
kick_hats(1, None)
kick_hats(2, None, every_beat=False, last=4)
hit(DRUMS, R(3, 0), "kick")
finish("OUT")

# ================================================================ the song: 64 slots, same shape as Korobeiniki
PATTERN_NAMES = ["INT1", "INT2", "VA1", "VA2", "A1", "A2", "A1x", "A2x", "B1", "B2",
                 "BR1", "BR2", "BU1", "BU2", "RLD", "OUT"]
INTRO, VERSE_P, BREAK, BUILD = ["INT1", "INT2"], ["VA1", "VA2"], ["BR1", "BR2"], ["BU1", "BU2"]
DROP_A, DROP_AX, DROP_B, RELOAD = ["A1", "A2"], ["A1x", "A2x"], ["B1", "B2"], ["RLD"]
ORDER = (INTRO + VERSE_P + BREAK + BUILD + DROP_A + DROP_B                        #  0-11
         + VERSE_P + BREAK + BUILD + DROP_B + DROP_AX + DROP_A                    # 12-23
         + ["INT2", "INT1"] + BREAK + RELOAD + DROP_AX + DROP_B + DROP_A          # 24-34
         + VERSE_P + BREAK + BUILD + DROP_B + DROP_AX + RELOAD                    # 35-45
         + DROP_A + DROP_B + DROP_AX + BREAK + BUILD + DROP_B + DROP_A            # 46-59
         + ["INT2", "INT1", "INT1", "OUT"])                                       # 60-63
assert len(PATTERNS) == len(PATTERN_NAMES) == 16 and set(PATTERNS) == set(PATTERN_NAMES)
assert len(ORDER) == 64, len(ORDER)
assert set(ORDER) == set(PATTERN_NAMES)
ORDER_IDX = [PATTERN_NAMES.index(n) for n in ORDER]

# ------------------------------------------------------------------ write the file
def build_xm():
    n_pat = len(PATTERN_NAMES)
    out = bytearray()
    out += b"Extended Module: "
    out += b"Bella Ciao Techno".ljust(20, b"\0")
    out += b"\x1a"
    out += b"pyxm generator".ljust(20, b" ")
    out += struct.pack("<H", 0x0104)
    out += struct.pack("<I", 276)
    out += struct.pack("<HHHHHHHH", len(ORDER_IDX), 0, CHANNELS, n_pat, len(SAMPLES), 1, SPEED, BPM)
    out += bytes(ORDER_IDX + [0] * (256 - len(ORDER_IDX)))
    for p in range(n_pat):
        packed = bytearray()
        for r in range(ROWS_PER_PATTERN):
            for ch in range(CHANNELS):
                cell = PATTERNS[PATTERN_NAMES[p]][ch][r]
                if cell is None:
                    packed.append(0x80)
                    continue
                note, inst, vol = cell
                flags, body = 0x80, bytearray()
                if note:
                    flags |= 1
                    body.append(note)
                if inst:
                    flags |= 2
                    body.append(inst)
                if vol:
                    flags |= 4
                    body.append(vol)
                packed.append(flags)
                packed += body
        out += struct.pack("<IBHH", 9, 0, ROWS_PER_PATTERN, len(packed))
        out += packed
    for s in SAMPLES:
        out += instrument_bytes(*s)
    return bytes(out)

if __name__ == "__main__":
    data = build_xm()
    with open(OUT, "wb") as f:
        f.write(data)
    secs = len(ORDER_IDX) * ROWS_PER_PATTERN * 2.5 * SPEED / BPM
    print(f"wrote {OUT}: {len(data)} bytes, {len(PATTERN_NAMES)} patterns, song length {len(ORDER_IDX)}, ~{secs:.0f}s")
