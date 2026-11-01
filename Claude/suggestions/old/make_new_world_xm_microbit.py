"""
NEW WORLD SYMPHONY - techno, for 4 micro:bits. Same setup and the same 10 instruments as Korobeiniki and the Canon.

Dvorak's Symphony No. 9 "From the New World" (1893) is in the public domain. Used here from the original:
  - the opening of the 4th movement: the B-C semitone figure that starts slow and speeds up, the rising run,
    the alternating chord stabs (the INTRO and the BUILD)
  - the 4th movement's main theme, 8 bars, over Dvorak's chords: Em Am Em-G Em | Em Am Em-B Em (THEME, DROPS)
  - the Largo theme, both phrases, over Dvorak's chords (the BREAKDOWN)
The notes were checked against 8notes.com's MIDI files of the two themes (there in D minor and B-flat major).
Here the 4th movement is back in Dvorak's E minor, and the Largo is in G major (the relative major).
The theme's one triplet is rounded to eighths; the 4th movement's later 16th-note variations are not used.

Setup (unchanged): 4 channels, 32 rows per pattern = 4 bars of eighth notes, speed 12 / tempo 150,
16 patterns, a 64-slot order list, no volume column, no effects, 10 instruments:
  1 Tone  2 Kick  3 Snare  4 Clap  5 Hat  6 Open hat  7 Crash  8 Tom (C-4 low / G-4 high)
  9 Pew zap (C-4 / C-5)  10 Hoover (E-4 / A-4)
Pitched parts between C-4 and B-6; lead and voice Tone no lower than E-4 (micro:bit V2 speaker).

Channels: 1 LEAD (tune)  2 ACID (bass)  3 VOX (second percussion lane, Hoover stabs, arpeggios)  4 DRUMS

Usage: python3 make_new_world_xm_microbit.py [output.xm]
"""
import math
import random
import struct
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "new_world_techno_4ch_microbit.xm"

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

# ================================================================ NEW WORLD
CHORDS = {"Em": ("E", [0, 3, 7]), "Am": ("A", [0, 3, 7]), "G": ("G", [0, 4, 7]), "B": ("B", [0, 4, 7]),
          "D": ("D", [0, 4, 7]), "C": ("C", [0, 4, 7])}
ROOT = {"Em": N("E4"), "Am": N("A4"), "G": N("G4"), "B": N("B4"), "D": N("D4"), "C": N("C4")}
HALF = ROWS_PER_BAR // 2                          # chords change at most every half bar (4 rows)
VOICE_FLOOR = N("E4")

# ---- the 4th movement's main theme (E minor), (note, rows). 2 rows = a quarter note. 32 rows = 4 bars.
THEME_1 = [("E5", 4), ("F#5", 2), ("G5", 2), ("F#5", 3), ("E5", 1), ("E5", 4),
           ("E5", 4), ("D5", 2), ("B4", 1), ("D5", 1), ("E5", 6), ("E5", 2)]
THEME_2 = [("E5", 4), ("F#5", 2), ("G5", 2), ("F#5", 3), ("E5", 1), ("E5", 4),
           ("E5", 2), ("G5", 1), ("E5", 1), ("B5", 2), ("B4", 2), ("E5", 8)]
PROG_T1 = ["Em", "Em", "Am", "Am", "Em", "G", "Em", "Em"]     # per half bar
PROG_T2 = ["Em", "Em", "Am", "Am", "Em", "B", "Em", "Em"]

# ---- the Largo (G major). One beat = 2 rows, so each phrase takes 2 patterns.
LARGO_A1 = [("B4", 6), ("D5", 2), ("D5", 8), ("B4", 6), ("A4", 2), ("G4", 8)]
LARGO_A2 = [("A4", 6), ("B4", 2), ("D5", 6), ("B4", 2), ("A4", 16)]
LARGO_B1 = [("B4", 6), ("D5", 2), ("D5", 8), ("B4", 6), ("A4", 2), ("G4", 8)]
LARGO_B2 = [("A4", 4), ("B4", 4), ("A4", 6), ("G4", 2), ("G4", 16)]
PROG_LA1 = ["G"] * 8
PROG_LA2 = ["D"] * 8
PROG_LB1 = ["G", "G", "G", "G", "Em", "Em", "Em", "Em"]
PROG_LB2 = ["Am", "Am", "D", "D", "G", "G", "G", "G"]
for line in (THEME_1, THEME_2, LARGO_A1, LARGO_A2, LARGO_B1, LARGO_B2):
    assert sum(l for _, l in line) == ROWS_PER_PATTERN


def chord_notes(name, octave):
    root, iv = CHORDS[name]
    base = N(root + str(octave))
    while base < VOICE_FLOOR:
        base += 12
    return [base + i for i in iv]


def melody(ch, notes, gap=True):
    r = 0
    for name, ln in notes:
        if name:
            put(ch, r, N(name), I_SQ)
            if gap and ln >= 4:
                off(ch, r + ln - 1)
        r += ln


def hoover_note(chord):
    """2 pitches only: E-4 over E minor, C and G; A-4 over A minor, B and D."""
    return N("E4") if chord in ("Em", "C", "G") else N("A4")


SOUND = {"lo": (N("C4"), I_TOM), "hi": (N("G4"), I_TOM), "clap": (C4, I_CLAP), "hat": (C4, I_HAT),
         "ohat": (C4, I_OHAT), "crash": (C4, I_CRASH), "kick": (C4, I_KICK), "snare": (C4, I_SNARE)}


def hit(ch, row, what):
    note, inst = SOUND[what]
    put(ch, row, note, inst)


# ---------------- ACID: one chord = 4 rows
BASS_STYLES = {
    "hold":  [(0, 0), None, None, "off"],
    "beat":  [(0, 0), "off", (0, 0), "off"],
    "drive": [(0, 0), (0, 0), (0, 1), (0, 0)],
    "roll":  [(0, 0), (0, 1), (7, 0), (0, 1)],
    "pump":  [(0, 0), (0, 1), (0, 0), (0, 1)],
    "gallop": [(0, 0), (0, 0), (0, 1), "off"],
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


def bass_line(prog, style):
    for pos, c in enumerate(prog):
        bass(pos, c, style)


def arp(pos, chord, octave=4):
    tones = chord_notes(chord, octave)
    for k, t in enumerate((0, 1, 2, 1)):
        put(VOX, pos * HALF + k, tones[t], I_P12)


# ---------------- DRUMS and the VOX percussion lane
def kick_hats(bar, hat="hat", every_beat=True, last=ROWS_PER_BAR):
    for r in range(min(ROWS_PER_BAR, last)):
        if r % 2 == 0:
            if every_beat or r in (0, 4):
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
# ---- INT1: Dvorak's opening - the B-C semitone figure, slow, then faster, then alternating with a rising run
new_pattern()
for b in (0, 1):                                   # B (dotted quarter) C (eighth), rest: twice
    put(ACID, R(b, 0), N("B4"), I_ACID); put(ACID, R(b, 3), N("C5"), I_ACID); off(ACID, R(b, 4))
for k in (0, 4):                                   # faster: B (quarter) C (eighth), rest
    put(ACID, R(2, k), N("B4"), I_ACID); put(ACID, R(2, k + 2), N("C5"), I_ACID); off(ACID, R(2, k + 3))
RUN = ["C5", "C#5", "D#5", "E5", "F#5", "G5", "A5", "A#5"]
for k in range(4):                                 # B alternating with the rising run (first half)
    put(ACID, R(3, 2 * k), N("B4"), I_ACID); put(ACID, R(3, 2 * k + 1), N(RUN[k]), I_ACID)
for b in range(4):
    hit(DRUMS, R(b, 0), "kick")
hit(DRUMS, R(3, 4), "kick")
finish("INT1")

# ---- INT2: the run completes, then the alternating chord stabs (B vs C) over a B pedal, tremolo into the theme
new_pattern()
for k in range(4):
    put(ACID, R(0, 2 * k), N("B4"), I_ACID); put(ACID, R(0, 2 * k + 1), N(RUN[4 + k]), I_ACID)
for b in (1, 2):
    for beat in range(4):
        r = R(b, 2 * beat)
        put(LEAD, r, N("B5"), I_SQ); off(LEAD, r + 1)              # stab on the beat
        put(VOX, r + 1, N("C6") if beat % 2 == 0 else N("A5"), I_P12); off(VOX, r + 2, force=False)
        put(ACID, r, N("B4"), I_ACID); off(ACID, r + 1)
        hit(DRUMS, r, "kick"); hit(DRUMS, r + 1, "hat")
hit(DRUMS, R(1, 0), "crash")
for r in range(ROWS_PER_BAR):                                      # last bar: B-C tremolo + snare roll
    put(LEAD, R(3, r), N("B5") if r % 2 == 0 else N("C6"), I_SQ)
    put(ACID, R(3, r), N("B4"), I_ACID)
roll_bar(3, 2)
finish("INT2")


# ---- T1 T2: the main theme, first time - kick on 1 and 3, the VOX lane with claps and Hoover stabs
def theme_pat(name, line, prog):
    new_pattern()
    melody(LEAD, line)
    for b in range(4):
        kick_hats(b, "hat", every_beat=False)
        perc_bar(b, prog, crash=(b == 0 and name == "T1"), stabs=(name == "T2"))
    bass_line(prog, "beat")
    finish(name)


theme_pat("T1", THEME_1, PROG_T1)
theme_pat("T2", THEME_2, PROG_T2)


# ---- the drops: four on the floor, open or closed hats, Hoover stabs, fills
def drop_pat(name, line, prog, style, hat, fill, ghost=False):
    new_pattern()
    melody(LEAD, line)
    for b in range(4):
        if fill and b == 3:
            fill_drums(b)
        else:
            kick_hats(b, hat)
        perc_bar(b, prog, crash=(b == 0), ghost=ghost, fill=(fill and b == 3))
    for pos, c in enumerate(prog):
        if fill and pos == 7:
            bass(pos, c, style, last=2)
            off(ACID, pos * HALF + 2)
        else:
            bass(pos, c, style)
    finish(name)


drop_pat("D1", THEME_1, PROG_T1, "drive", "ohat", fill=False)
drop_pat("D2", THEME_2, PROG_T2, "drive", "ohat", fill=True)
drop_pat("D1x", THEME_1, PROG_T1, "roll", "hat", fill=False, ghost=True)
drop_pat("D2x", THEME_2, PROG_T2, "gallop", "hat", fill=True, ghost=True)


# ---- LG1-LG4: the Largo breakdown. First phrase: no drums. Second phrase: the kick comes back.
def largo_pat(name, line, prog, kick):
    new_pattern()
    melody(LEAD, line)
    for pos, c in enumerate(prog):
        bass(pos, c, "hold")
        arp(pos, c, 5)
    if kick:
        for b in range(4):
            kick_hats(b, None, every_beat=False)
    finish(name)


largo_pat("LG1", LARGO_A1, PROG_LA1, kick=False)
largo_pat("LG2", LARGO_A2, PROG_LA2, kick=False)
largo_pat("LG3", LARGO_B1, PROG_LB1, kick=True)
largo_pat("LG4", LARGO_B2, PROG_LB2, kick=True)

# ---- BU1 BU2: the build - the B-C figure speeding up and climbing over a B pedal, pew-pews, snare roll,
#      then one beat of silence
BUILD_ROWS = 2 * ROWS_PER_PATTERN - 2
FIG = [("B4", "C5"), ("B4", "C5"), ("B4", "C5"), ("B4", "C5"), ("B5", "C6"), ("B5", "C6"), ("B5", "C6"), ("B5", "C6")]
STEP = (4, 4, 2, 2, 2, 2, 1, 1)                    # rows per note: half the speed, then quarters, then eighths
ZAP_RATE = ((4, 1), (4, 1), (2, 1), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0))
trig = [g for g in range(BUILD_ROWS)
        if (g % ROWS_PER_BAR) % ZAP_RATE[g // ROWS_PER_BAR][0] == ZAP_RATE[g // ROWS_PER_BAR][1]]
zap_at = {g: (N("C4"), N("C5"))[int(n / len(trig) * 2)] for n, g in enumerate(trig)}
for k in range(2):
    new_pattern()
    for b in range(4):
        i = 4 * k + b
        last = 6 if i == 7 else ROWS_PER_BAR
        if i < 2:
            kick_hats(b, "hat")
        else:
            roll_bar(b, (1, 1, 2, 2, 3, 3)[i - 2], last)
    for pos in range(8):
        if k == 1 and pos == 7:
            bass(pos, "B", "pump", last=2)
        else:
            bass(pos, "B", "beat" if k == 0 else "pump")
    for rr in range(ROWS_PER_PATTERN):
        g = k * ROWS_PER_PATTERN + rr
        if g >= BUILD_ROWS:
            break
        bi = g // ROWS_PER_BAR
        n = (g - bi * ROWS_PER_BAR) // STEP[bi]
        if (g - bi * ROWS_PER_BAR) % STEP[bi] == 0:
            put(LEAD, rr, N(FIG[bi][n % 2]), I_SQ)
        if g in zap_at:
            put(VOX, rr, zap_at[g], I_ZAP)
    if k == 1:
        for ch in range(CHANNELS):
            off(ch, BUILD_ROWS - ROWS_PER_PATTERN)
    finish(f"BU{k + 1}")

# ---- RLD: reload - held Hoover over the B pedal + the first 2 bars of the theme, then a mini-build
new_pattern()
melody(LEAD, THEME_1[:6])                          # the first 2 bars (16 rows)
for b in (0, 1):
    put(VOX, R(b), N("A4"), I_HOOVER)
    off(VOX, R(b, ROWS_PER_BAR - 1))
for pos in range(4):
    bass(pos, "Em", "hold")
RLD_ROWS = ROWS_PER_PATTERN - 2
for b in (2, 3):
    roll_bar(b, (2, 3)[b - 2], 6 if b == 3 else ROWS_PER_BAR)
for pos in range(4, 8):
    bass(pos, "B", "pump", last=2 if pos == 7 else HALF)
for rr in range(2 * ROWS_PER_BAR, RLD_ROWS):
    t = (rr - 2 * ROWS_PER_BAR) / (RLD_ROWS - 2 * ROWS_PER_BAR)
    put(LEAD, rr, N("B5") if rr % 2 == 0 else N("C6"), I_SQ)
    put(VOX, rr, (N("C4"), N("C5"))[int(t * 2)], I_ZAP)
for ch in range(CHANNELS):
    off(ch, RLD_ROWS)
finish("RLD")

# ---- OUT: the end of the theme, then the kick fades out on E
new_pattern()
melody(LEAD, [("B5", 2), ("B4", 2), ("E5", 8)])
put(VOX, R(0), N("E4"), I_HOOVER); off(VOX, R(0, 7))
for pos in (0, 1, 2):
    bass(pos, "Em", "hold")
kick_hats(0, "hat")
kick_hats(1, None)
kick_hats(2, None, every_beat=False, last=4)
hit(DRUMS, R(3, 0), "kick")
finish("OUT")

# ================================================================ the song: 64 slots from 16 patterns
PATTERN_NAMES = ["INT1", "INT2", "T1", "T2", "D1", "D2", "D1x", "D2x",
                 "LG1", "LG2", "LG3", "LG4", "BU1", "BU2", "RLD", "OUT"]
INTRO, THEME, BUILD, RELOAD = ["INT1", "INT2"], ["T1", "T2"], ["BU1", "BU2"], ["RLD"]
DROP, DROPX, LARGO = ["D1", "D2"], ["D1x", "D2x"], ["LG1", "LG2", "LG3", "LG4"]
ORDER = (INTRO + THEME + BUILD + DROP + DROPX + DROP                       #  0-11
         + LARGO + BUILD + DROP + DROPX + DROP                            # 12-23
         + ["INT2"] + THEME + RELOAD + DROPX + DROP + DROPX               # 24-33
         + LARGO[:2] + BUILD + DROP + DROPX + RELOAD + DROP               # 34-44
         + DROPX + LARGO[2:] + BUILD + DROP + DROPX + DROP                # 45-56
         + THEME + DROPX + ["INT2", "INT1", "OUT"])                       # 57-63
assert len(PATTERNS) == len(PATTERN_NAMES) == 16 and set(PATTERNS) == set(PATTERN_NAMES)
assert len(ORDER) == 64, len(ORDER)
assert set(ORDER) == set(PATTERN_NAMES)
ORDER_IDX = [PATTERN_NAMES.index(n) for n in ORDER]

# ------------------------------------------------------------------ write the file
def build_xm():
    n_pat = len(PATTERN_NAMES)
    out = bytearray()
    out += b"Extended Module: "
    out += b"New World Techno".ljust(20, b"\0")
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
