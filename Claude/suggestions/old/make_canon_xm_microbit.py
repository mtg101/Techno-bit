"""
CANON IN D - bhangra techno, for 4 micro:bits. Same setup and the same 10 instruments as the Korobeiniki tune.

Pachelbel's Canon and Gigue in D (about 1700) is in the public domain. Used here from the original:
  - the ground bass: 8 notes, D A B F# G D G A, under the chords D A Bm F#m G D G A
  - the first three violin lines (V1, V2, V3)
V4 is a new line written for this track (arpeggios over the same chords).

Setup (unchanged from Korobeiniki):
  4 channels, 32 rows per pattern = 4 bars of eighth notes, speed 12 / tempo 150 (1 row = 0.2 s),
  16 patterns, a 64-slot order list, no volume column, no effects, 10 instruments:
  1 Tone  2 Kick  3 Snare  4 Clap  5 Hat  6 Open hat  7 Crash  8 Tom (C-4 low / G-4 high)
  9 Pew zap (C-4 / C-5)  10 Hoover (E-4 / A-4)
  Pitched parts stay between C-4 and B-6; lead and voice Tone no lower than E-4 (micro:bit V2 speaker).

The 8 chords are STRETCHED to 2 per bar, so one pass of the ground bass = 4 bars = exactly one pattern.
Pachelbel's quarter notes become half notes here, his eighths become quarters, and so on.

THE CANON: Pachelbel's violins play the same lines, each one 2 of his bars behind the last. Stretched, that
delay is exactly one pattern. So in the canon patterns the VOX channel plays the line the LEAD played in the
previous pattern (V2 over V1, V3 over V2, V4 over V3) - two micro:bits playing a real canon.

BHANGRA: a dhol groove on the toms (low tom = the deep head, high tom = the sharp head) with claps on beats
2 and 4, over a four-on-the-floor kick.

Channels: 1 LEAD (tune)  2 ACID (ground bass)  3 VOX (dhol lane / canon voice / pings / Hoover)  4 DRUMS

Usage: python3 make_canon_xm_microbit.py [output.xm]
"""
import math
import random
import struct
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "canon_bhangra_4ch_microbit.xm"

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

# ================================================================ CANON IN D
CHORDS = {"D": ("D", [0, 4, 7]), "A": ("A", [0, 4, 7]), "Bm": ("B", [0, 3, 7]),
          "F#m": ("F#", [0, 3, 7]), "G": ("G", [0, 4, 7])}
PROG = ["D", "A", "Bm", "F#m", "G", "D", "G", "A"]           # 2 chords per bar: 8 chords = 4 bars = 1 pattern
# The ground bass, lifted so its shape is kept (down, up, down, up, down, up, up) and nothing is below C-4.
BASS = [N("D5"), N("A4"), N("B4"), N("F#4"), N("G4"), N("D4"), N("G4"), N("A4")]
HALF = ROWS_PER_BAR // 2                                     # 4 rows = one chord

# The violin lines. (note, rows). One line = 32 rows = one pattern.
V1 = [(n, 4) for n in ("F#5", "E5", "D5", "C#5", "B4", "A4", "B4", "C#5")]                  # Pachelbel
V2 = [(n, 4) for n in ("D5", "C#5", "B4", "A4", "G4", "F#4", "G4", "E4")]                   # Pachelbel
V3 = [(n, 2) for n in ("D5", "F#5", "A5", "G5", "F#5", "D5", "F#5", "E5",                   # Pachelbel
                       "D5", "B4", "D5", "A5", "G5", "B5", "A5", "G5")]
V4 = [(n, 1) for n in ("D5", "F#5", "A5", "D6",  "C#6", "A5", "E5", "A5",                   # new for this track
                       "B5", "F#5", "D5", "F#5", "A5", "F#5", "C#5", "F#5",
                       "G5", "B5", "D6", "B5",   "A5", "F#5", "D5", "F#5",
                       "G5", "D5", "B4", "D5",   "E5", "A5", "C#6", "E6")]
for line in (V1, V2, V3, V4):
    assert sum(l for _, l in line) == ROWS_PER_PATTERN

VOICE_FLOOR = N("E4")


def chord_notes(name, octave):
    root, iv = CHORDS[name]
    base = N(root + str(octave))
    while base < VOICE_FLOOR:
        base += 12
    return [base + i for i in iv]


def melody(ch, notes):
    """Place a whole line from row 0. A note of 4 rows or more gets a 1-row gap at its end."""
    r = 0
    for name, ln in notes:
        put(ch, r, N(name), I_SQ)
        if ln >= 4:
            off(ch, r + ln - 1)
        r += ln


def hoover_note(chord):
    """The Hoover has only 2 pitches: E-4 over the A chord, A-4 over everything else (A is in D, A and F#m)."""
    return N("E4") if chord == "A" else N("A4")


# ---------------- ACID: the ground bass, one chord = 4 rows
BASS_STYLES = {
    "hold":  [(0, 0), None, None, "off"],        # the plain ground bass (half notes)
    "beat":  [(0, 0), "off", (0, 0), "off"],     # on the beat
    "drive": [(0, 0), (0, 0), (0, 1), (0, 0)],   # driving
    "roll":  [(0, 0), (0, 1), (7, 0), (0, 1)],   # rolling: root, octave, fifth, octave
    "pump":  [(0, 0), (0, 1), (0, 0), (0, 1)],   # build: octave pump
}


def bass(pos, style, last=HALF):
    """Chord number pos (0-7) of the pattern, in one of the BASS_STYLES. (semitones above the root, octave)."""
    base = pos * HALF
    for k, step in enumerate(BASS_STYLES[style][:last]):
        if step is None:
            continue
        if step == "off":
            off(ACID, base + k)
        else:
            semis, octv = step
            put(ACID, base + k, BASS[pos] + semis + 12 * octv, I_ACID)


# ---------------- VOX: pings, arp, dhol
def pings(pos):
    """Offbeat chord pings, one chord = 4 rows."""
    tones = chord_notes(PROG[pos], 5)
    for k, t in ((1, 0), (3, 2)):
        put(VOX, pos * HALF + k, tones[t], I_P12)
        off(VOX, pos * HALF + k + 1, force=False)


def arp(pos, octave=4):
    tones = chord_notes(PROG[pos], octave)
    for k, t in enumerate((0, 1, 2, 1)):
        put(VOX, pos * HALF + k, tones[t], I_P12)


DHOL = ["lo", "hi", "clap", "lo", None, "lo", "clap", "hi"]  # one bar: deep, crack, clap ... (claps on beats 2 and 4)
SOUND = {"lo": (N("C4"), I_TOM), "hi": (N("G4"), I_TOM), "clap": (C4, I_CLAP), "hat": (C4, I_HAT),
         "ohat": (C4, I_OHAT), "crash": (C4, I_CRASH), "kick": (C4, I_KICK), "snare": (C4, I_SNARE)}


def hit(ch, row, what):
    note, inst = SOUND[what]
    put(ch, row, note, inst)


def dhol_bar(ch, bar, crash=False, stabs=False):
    """The dhol groove for one bar. crash = crash on the downbeat; stabs = Hoover stabs on the last row of
    each half bar (answering the chord)."""
    for r, what in enumerate(DHOL):
        if what:
            hit(ch, R(bar, r), what)
    if crash:
        hit(ch, R(bar, 0), "crash")
    if stabs:
        for k, pos in ((3, 2 * bar), (7, 2 * bar + 1)):
            put(ch, R(bar, k), hoover_note(PROG[pos]), I_HOOVER)


# ---------------- DRUMS
def kick_hats(bar, hat="hat", last=ROWS_PER_BAR):
    """Four on the floor + a hat on every offbeat."""
    for r in range(min(ROWS_PER_BAR, last)):
        hit(DRUMS, R(bar, r), "kick" if r % 2 == 0 else hat)


def kick_dhol(bar):
    """Four on the floor with the dhol answering on the offbeats (for when VOX is busy with the canon)."""
    for r, what in enumerate(["kick", "hi", "kick", "lo", "kick", "hi", "kick", "lo"]):
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


def fill_end(bar):
    """Last bar of a drop: half a bar of groove, then kick, snare, high tom, low tom + 4 pews on VOX."""
    kick_hats(bar, "ohat", last=4)
    for r, what in ((4, "kick"), (5, "snare"), (6, "hi"), (7, "lo")):
        hit(DRUMS, R(bar, r), what)
    for q, p in enumerate(("C4", "C4", "C5", "C5")):
        put(VOX, R(bar, 4 + q), N(p), I_ZAP)


def finish(name):
    finish_pattern(name)


# ================================================================ the 16 patterns
# ---- INT1: the ground bass alone (half notes), kick + hats, offbeat pings
new_pattern()
for b in range(4):
    kick_hats(b)
for pos in range(8):
    bass(pos, "hold")
    pings(pos)
finish("INT1")

# ---- INT2: the dhol comes in, bass on the beat, arp with Hoover stabs
new_pattern()
for b in range(4):
    kick_hats(b)
for pos in range(8):
    bass(pos, "beat")
    arp(pos)
for b in range(4):                     # Hoover stabs replace the last arp note of each chord
    for k, pos in ((3, 2 * b), (7, 2 * b + 1)):
        put(VOX, R(b, k), hoover_note(PROG[pos]), I_HOOVER)
finish("INT2")


# ---- V1-V4: the canon. LEAD plays line n; from V2 on, VOX plays line n-1 at the same time.
def canon_pat(name, lead_line, vox_line, style):
    new_pattern()
    melody(LEAD, lead_line)
    if vox_line is None:
        for b in range(4):
            dhol_bar(VOX, b, crash=(b == 0))
            kick_hats(b, "hat")
    else:
        melody(VOX, vox_line)
        for b in range(4):
            kick_dhol(b)
    for pos in range(8):
        bass(pos, style)
    finish(name)


canon_pat("V1", V1, None, "hold")
canon_pat("V2", V2, V1, "beat")
canon_pat("V3", V3, V2, "drive")
canon_pat("V4", V4, V3, "drive")


# ---- the drops: tune on LEAD, dhol + crash + Hoover on VOX, four on the floor + open hats on DRUMS
def drop_pat(name, line, style, hat, fill):
    new_pattern()
    melody(LEAD, line)
    for b in range(4):
        dhol_bar(VOX, b, crash=(b == 0), stabs=(b % 2 == 1))
        if fill and b == 3:
            fill_end(b)
        else:
            kick_hats(b, hat)
    for pos in range(8):
        if fill and pos == 7:
            bass(pos, style, last=2)   # the bass stops for the fill
            off(ACID, pos * HALF + 2)
        else:
            bass(pos, style)
    finish(name)


drop_pat("D1", V3, "drive", "ohat", fill=False)
drop_pat("D2", V4, "drive", "ohat", fill=True)
drop_pat("D1x", V3, "roll", "hat", fill=False)
drop_pat("D2x", V4, "roll", "hat", fill=True)


# ---- BR1 BR2: breakdown - no drums. The first two lines, slow, over held bass + a quiet arp
def break_pat(name, line):
    new_pattern()
    melody(LEAD, line)
    for pos in range(8):
        bass(pos, "hold")
        arp(pos, 5)
    finish(name)


break_pat("BR1", V1)
break_pat("BR2", V2)

# ---- BU1 BU2: the 8-bar build. Stuttering lead climbing, pew-pews speeding up, snare roll, octave pump,
#      then one beat of silence.
BUILD_ROWS = 2 * ROWS_PER_PATTERN - 2
LEAD_CLIMB = [N(n) for n in ("D5", "D5", "F#5", "F#5", "A5", "A5", "D6", "D6")]   # one per bar
LEAD_STEP = (2, 2, 1, 1, 1, 1, 1, 1)
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
            kick_hats(b)
        else:
            roll_bar(b, (1, 1, 2, 2, 3, 3)[i - 2], last)
    for pos in range(8):
        i = 4 * k + pos // 2
        if k == 1 and pos == 7:
            bass(pos, "pump", last=2)
        else:
            bass(pos, "beat" if i < 4 else "pump")
    for rr in range(ROWS_PER_PATTERN):
        g = k * ROWS_PER_PATTERN + rr
        if g >= BUILD_ROWS:
            break
        bi = g // ROWS_PER_BAR
        if (g - bi * ROWS_PER_BAR) % LEAD_STEP[bi] == 0:
            put(LEAD, rr, LEAD_CLIMB[bi], I_SQ)
        if g in zap_at:
            put(VOX, rr, zap_at[g], I_ZAP)
    if k == 1:
        for ch in range(CHANNELS):
            off(ch, BUILD_ROWS - ROWS_PER_PATTERN)
    finish(f"BU{k + 1}")

# ---- RLD: reload - held Hoover + the first half of V1, then a quick mini-build and a silent beat
new_pattern()
melody(LEAD, V1[:4])                   # the first half of V1 (2 bars)
for b in (0, 1):
    put(VOX, R(b), hoover_note(PROG[2 * b]), I_HOOVER)
    off(VOX, R(b, ROWS_PER_BAR - 1))
for pos in range(4):
    bass(pos, "hold")
RLD_ROWS = ROWS_PER_PATTERN - 2
for b in (2, 3):
    last = 6 if b == 3 else ROWS_PER_BAR
    roll_bar(b, (2, 3)[b - 2], last)
for pos in range(4, 8):
    bass(pos, "pump", last=2 if pos == 7 else HALF)
for rr in range(2 * ROWS_PER_BAR, RLD_ROWS):
    t = (rr - 2 * ROWS_PER_BAR) / (RLD_ROWS - 2 * ROWS_PER_BAR)
    put(LEAD, rr, N("D5") if rr < 3 * ROWS_PER_BAR else N("A5"), I_SQ)
    put(VOX, rr, (N("C4"), N("C5"))[int(t * 2)], I_ZAP)
for ch in range(CHANNELS):
    off(ch, RLD_ROWS)
finish("RLD")

# ---- OUT: the groove thins out over the ground bass, then just the kick
new_pattern()
kick_hats(0)
for pos in (0, 1):
    pings(pos)
    bass(pos, "hold")
kick_hats(1, hat="kick")
for r in range(0, 4, 2):
    hit(DRUMS, R(2, r), "kick")
hit(DRUMS, R(3, 0), "kick")
finish("OUT")

# ================================================================ the song: 64 slots from 16 patterns
PATTERN_NAMES = ["INT1", "INT2", "V1", "V2", "V3", "V4", "D1", "D2", "D1x", "D2x",
                 "BR1", "BR2", "BU1", "BU2", "RLD", "OUT"]
INTRO, CANON, BREAK, BUILD = ["INT1", "INT2"], ["V1", "V2", "V3", "V4"], ["BR1", "BR2"], ["BU1", "BU2"]
DROP, DROPX, RELOAD = ["D1", "D2"], ["D1x", "D2x"], ["RLD"]
ORDER = (INTRO + CANON                                       #  0-5   the ground bass, then the canon builds up
         + BUILD + DROP + DROPX                              #  6-11  first drop
         + BREAK + ["V3", "V4"] + BUILD                      # 12-17
         + DROP + DROPX + DROP                               # 18-23
         + ["INT2", "INT1"] + BREAK + RELOAD + DROPX + DROP  # 24-32
         + CANON + BREAK + BUILD                             # 33-40
         + DROP + DROPX + RELOAD + DROP + DROPX              # 41-49
         + BREAK + BUILD + DROP + DROPX + DROP               # 50-59
         + ["INT2", "INT1", "INT1", "OUT"])                  # 60-63
assert len(PATTERNS) == len(PATTERN_NAMES) == 16 and set(PATTERNS) == set(PATTERN_NAMES)
assert len(ORDER) == 64, len(ORDER)
assert set(ORDER) == set(PATTERN_NAMES)
ORDER_IDX = [PATTERN_NAMES.index(n) for n in ORDER]

# ------------------------------------------------------------------ write the file
def build_xm():
    n_pat = len(PATTERN_NAMES)
    out = bytearray()
    out += b"Extended Module: "
    out += b"Bhangra Canon in D".ljust(20, b"\0")
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
