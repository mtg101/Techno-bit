"""
ODE TO JOY - SYNTHWAVE v2, for 4 micro:bits. Same setup and the same 10 instruments as the other tunes.
Beethoven's Symphony No. 9 (1824), public domain. Melody from memory, re-rhythmed (same notes, same order).

What v2 adds to the syncopated synthwave version, to make it less "basic":
  1. RICHER CHORDS: two chords a bar instead of only A and E.
       phrase A: A F#m E A D A A E      phrase A': A F#m E A D A E A      phrase B: E E Bm F#m E A D E
  2. MINOR VERSES, MAJOR DROPS: intro, verses and breakdown in A MINOR (C# becomes C; chords Am Dm E F G),
     every drop in bright A MAJOR.
  3. KEY CHANGE: the last drops go up a whole step to B MAJOR (KA KA2 KB).
  4. COUNTER-MELODY: in the verses track 3 answers the lead at the end of each bar (instead of an arpeggio).
  5. EDITS: a stutter on the last note of the first drop phrase, a half-bar stop before phrase B, Hoover brass
     hits in the key-change drops, tom cascades.
Kept from v1: the syncopated melody, the 3+3+2 kick, the bass locked to the kick, track 3 as a second kit in the
drops, the half-time feel (one row = a 16th at 75 BPM).

Hoover (only A-4 and E-4): A-4 over A Am D Dm F G F#m Bm B; E-4 over E F# C#m; silent over G#m.

Setup (unchanged): 4 channels, 32 rows per pattern, speed 12 / tempo 150, 16 patterns, 64-slot order list,
no volume column, no effects, 10 instruments. Pitched parts C-4 to B-6; lead and voice no lower than E-4.
Patterns: INT1 INT2 P1 P2 P3 P4 D1 D2 D3 D4 KA KA2 KB BR BU OUT

Usage: python3 make_ode_to_joy_synthwave_v2_xm_microbit.py [output.xm]
"""
import math
import random
import struct
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "ode_to_joy_synthwave_v2_4ch_microbit.xm"

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

# ================================================================ ODE TO JOY SYNTHWAVE v2
HALF = ROWS_PER_BAR // 2
VOICE_FLOOR = N("E4")

# the syncopated phrases (note, rows), A major; the minor versions swap C# for C
SY_A = [("C#6", 3), ("C#6", 3), ("D6", 1), ("E6", 1), ("E6", 2), ("D6", 1), ("C#6", 3), ("B5", 2),
        ("A5", 3), ("A5", 3), ("B5", 1), ("C#6", 1), ("C#6", 3), ("B5", 1), ("B5", 4)]
SY_A2 = SY_A[:12] + [("B5", 3), ("A5", 1), ("A5", 4)]
SY_B = [("B5", 3), ("B5", 3), ("C#6", 1), ("A5", 1), ("B5", 2), ("C#6", 1), ("D6", 1), ("C#6", 3), ("A5", 1),
        ("B5", 2), ("C#6", 1), ("D6", 1), ("C#6", 3), ("B5", 1), ("A5", 2), ("B5", 1), ("E5", 5)]
PHRASES = [SY_A, SY_A2, SY_B, SY_A2]
for ph in PHRASES:
    assert sum(l for _, l in ph) == ROWS_PER_PATTERN

# chords per half bar (A major)
PROG_A = ["A", "F#m", "E", "A", "D", "A", "A", "E"]
PROG_A2 = ["A", "F#m", "E", "A", "D", "A", "E", "A"]
PROG_B = ["E", "E", "Bm", "F#m", "E", "A", "D", "E"]
PROGS = [PROG_A, PROG_A2, PROG_B, PROG_A2]
TO_MINOR = {"A": "Am", "D": "Dm", "E": "E", "F#m": "F", "Bm": "G"}
UP_A_STEP = {"A": "B", "D": "E", "E": "F#", "F#m": "G#m", "Bm": "C#m"}

CHORDS = {"A": ("A", [0, 4, 7]), "Am": ("A", [0, 3, 7]), "D": ("D", [0, 4, 7]), "Dm": ("D", [0, 3, 7]),
          "E": ("E", [0, 4, 7]), "F#m": ("F#", [0, 3, 7]), "F": ("F", [0, 4, 7]), "Bm": ("B", [0, 3, 7]),
          "B": ("B", [0, 4, 7]), "G": ("G", [0, 4, 7]), "F#": ("F#", [0, 4, 7]), "G#m": ("G#", [0, 3, 7]), "C#m": ("C#", [0, 3, 7])}


def root(c):
    return N(CHORDS[c][0] + "4")                 # every root sits between C-4 and B-4


def chord_tones(c):
    base = root(c)
    while base < VOICE_FLOOR:
        base += 12
    return [base + i for i in CHORDS[c][1]]


def hoover_note(c):
    if c in ("E", "F#", "C#m"):
        return N("E4")
    if c == "G#m":
        return None                              # neither A nor E fits G# minor
    return N("A4")


def mode(prog, m):
    """m = 'major', 'minor' or 'up' (the key change)."""
    if m == "minor":
        return [TO_MINOR[c] for c in prog]
    if m == "up":
        return [UP_A_STEP[c] for c in prog]
    return list(prog)


def phrase_notes(ph, m):
    out = []
    for n, l in ph:
        x = N(n.replace("C#", "C") if m == "minor" else n) + (2 if m == "up" else 0)
        out.append((x, l))
    return out


def melody(ch, notes, stutter_last=False):
    r = 0
    for i, (x, l) in enumerate(notes):
        last = i == len(notes) - 1
        if stutter_last and last:
            for k in range(l):                    # the edit: the last note repeated every row
                put(ch, r + k, x, I_SQ)
        else:
            put(ch, r, x, I_SQ)
            if l >= 4:
                off(ch, r + l - 1)
        r += l


SOUND = {"lo": (N("C4"), I_TOM), "hi": (N("G4"), I_TOM), "clap": (C4, I_CLAP), "hat": (C4, I_HAT),
         "ohat": (C4, I_OHAT), "crash": (C4, I_CRASH), "kick": (C4, I_KICK), "snare": (C4, I_SNARE)}


def hit(ch, row, what):
    if what:
        note, inst = SOUND[what]
        put(ch, row, note, inst)


# ---------------- drums (from v1): 3+3+2 kick, half-time snare; track 3 the second kit in the drops
SW_DRUMS = [["kick", "hat", "ohat", "kick", "snare", "hat", "kick", "hat"],
            ["kick", "hat", "hat", "kick", "snare", "kick", "hat", "ohat"]]
SW_VOX = [[None, None, "hi", None, "clap", "lo", None, "clap"],
          [None, "lo", None, "hi", "clap", None, "lo", "clap"]]
SW_VERSE = [["kick", None, "hat", "kick", "snare", None, "hat", None],
            ["kick", None, "hat", None, "snare", "kick", "hat", "ohat"]]


def drop_kit(b, brass=None, last=ROWS_PER_BAR):
    for r in range(min(ROWS_PER_BAR, last)):
        hit(DRUMS, R(b, r), SW_DRUMS[b % 2][r])
        hit(VOX, R(b, r), SW_VOX[b % 2][r])
    if brass is not None:                         # key-change drops: a Hoover hit on the downbeat of every bar
        put(VOX, R(b, 0), brass, I_HOOVER)


def verse_kit(b):
    for r in range(ROWS_PER_BAR):
        hit(DRUMS, R(b, r), SW_VERSE[b % 2][r])


def tom_cascade(b):
    for k, (d, v) in enumerate((("snare", "hi"), ("hi", "hi"), ("lo", "lo"), ("kick", "crash"))):
        hit(DRUMS, R(b, 4 + k), d)
        hit(VOX, R(b, 4 + k), v)


def sync_bass(prog, drop, last_bar_rows=ROWS_PER_BAR):
    for b in range(4):
        c1, c2 = prog[2 * b], prog[2 * b + 1]
        steps = [(0, root(c1)), (2, "off"), (3, root(c1)), (5, "off"), (6, root(c2) + 12),
                 (7, root(c2) if drop else "off")]
        for r, v in steps:
            if b == 3 and r >= last_bar_rows:
                continue
            if v == "off":
                off(ACID, R(b, r))
            else:
                put(ACID, R(b, r), v, I_ACID)


GATE = (0, 1, 3, 4, 6)
ARP_SHAPE = [0, 1, 2, 3, 4, 5, 4, 3]


def arp(prog, rows):
    for r in rows:
        t = chord_tones(prog[r // HALF])
        ladder = t + [x + 12 for x in t]
        x = ladder[ARP_SHAPE[r % 8]]
        ld = lead_at(r)
        if ld is not None and (x - ld) % 12 in (1, 11):
            continue                              # a semitone from the lead would rub
        put(VOX, r, x, I_P12)


def lead_at(row):
    """The lead note sounding on this row (None if silent)."""
    for r in range(row, -1, -1):
        cell = grid[LEAD][r]
        if cell is not None:
            return None if cell[0] == NOTE_OFF else cell[0]
    return None


def counter(prog):
    """Track 3 answers the lead: 3 notes falling at the end of even bars, 2 rising at the end of odd bars,
    from the chord of the second half of the bar. A note a semitone from the lead is left out (it would rub)."""
    for b in range(4):
        t = chord_tones(prog[2 * b + 1])
        if b % 2 == 0:
            steps = zip((5, 6, 7), (t[2], t[1], t[0]))
        else:
            steps = zip((6, 7), (t[1], t[2]))
        for r, x in steps:
            ld = lead_at(R(b, r))
            if ld is not None and (x - ld) % 12 in (1, 11):
                continue
            put(VOX, R(b, r), x, I_P12)
        if b < 3:
            off(VOX, R(b + 1, 0), force=False)


def roll(b, level, last=ROWS_PER_BAR):
    for r in range(min(ROWS_PER_BAR, last)):
        if level == 2:
            what = "kick" if r % 4 == 0 else ("snare" if r % 2 == 0 else None)
        elif level == 3:
            what = "kick" if r % 2 == 0 else "snare"
        else:
            what = "kick" if r == 0 else "snare"
        hit(DRUMS, R(b, r), what)


finish = finish_pattern

# ================================================================ the 16 patterns
INTRO = mode(["A", "A", "D", "D", "A", "A", "E", "E"], "minor")      # Am Am Dm Dm Am Am E E

# ---- INT1: the gated arpeggio, then the bass from bar 3 (A minor)
new_pattern()
arp(INTRO, [r for r in range(ROWS_PER_PATTERN) if r % 8 in GATE])
sync_bass(INTRO, drop=False)
for r in range(16):
    grid[ACID][r] = None
finish("INT1")

# ---- INT2: + the verse kit, fill at the end
new_pattern()
arp(INTRO, [r for r in range(ROWS_PER_PATTERN) if r % 8 in GATE])
sync_bass(INTRO, drop=False)
for b in range(4):
    verse_kit(b)
for k, what in enumerate(("snare", "snare", "hi", "lo")):
    hit(DRUMS, R(3, 4 + k), what)
finish("INT2")

# ---- P1-P4: the verses, A MINOR: lead + counter-melody on track 3
for k in range(4):
    new_pattern()
    prog = mode(PROGS[k], "minor")
    melody(LEAD, phrase_notes(PHRASES[k], "minor"))
    counter(prog)
    for b in range(4):
        verse_kit(b)
    sync_bass(prog, drop=False)
    if k == 3:
        for j, what in enumerate(("snare", "snare", "hi", "lo")):
            hit(DRUMS, R(3, 4 + j), what)
    finish("P%d" % (k + 1))


# ---- D1-D4: the drops, A MAJOR. KA KA2 KB: the same, up a step (B major) with Hoover brass
def drop_pat(name, k, m, stutter=False, stop=False, cascade=False):
    new_pattern()
    prog = mode(PROGS[k], m)
    melody(LEAD, phrase_notes(PHRASES[k], m), stutter_last=stutter)
    for b in range(4):
        brass = hoover_note(prog[2 * b]) if m == "up" else None
        if (cascade or stop) and b == 3:
            drop_kit(b, brass, last=4)
        else:
            drop_kit(b, brass)
    hit(VOX, 0, "crash")
    sync_bass(prog, drop=True, last_bar_rows=(4 if (cascade or stop) else ROWS_PER_BAR))
    if cascade:
        tom_cascade(3)
    if stop:                                      # the edit: everything but the lead stops for half a bar
        for ch in (ACID, VOX, DRUMS):
            off(ch, R(3, 4))
    finish(name)


drop_pat("D1", 0, "major", stutter=True)
drop_pat("D2", 1, "major", stop=True)
drop_pat("D3", 2, "major")
drop_pat("D4", 3, "major", cascade=True)
drop_pat("KA", 0, "up", stutter=True)
drop_pat("KA2", 1, "up", cascade=True)
drop_pat("KB", 2, "up")

# ---- BR: breakdown, A MINOR - no drums, phrase A over held bass, the gated arpeggio, a Hoover pad
new_pattern()
prog = mode(PROG_A, "minor")
melody(LEAD, phrase_notes(SY_A, "minor"))
arp(prog, [r for r in range(ROWS_PER_PATTERN) if r % 8 in GATE and r % 16 >= 2])
for b in (0, 2):
    put(VOX, R(b, 0), hoover_note(prog[2 * b]), I_HOOVER)
for pos, c in enumerate(prog):
    put(ACID, pos * HALF, root(c), I_ACID)
    off(ACID, pos * HALF + 3)
hit(DRUMS, R(3, 0), "kick"); hit(DRUMS, R(3, 4), "kick")
finish("BR")

# ---- BU: the build (4 bars) - the roll speeds up, the lead stutters up E-E-B-E, the bass pumps on E,
#      the arpeggio climbs, then a beat of silence
new_pattern()
CLIMB, STEP = ["E5", "B5", "E6", "E6"], (2, 2, 1, 1)
for b in range(4):
    roll(b, (2, 3, 4, 4)[b], last=(6 if b == 3 else ROWS_PER_BAR))
    for r in range(ROWS_PER_BAR):
        if r % STEP[b] == 0:
            put(LEAD, R(b, r), N(CLIMB[b]), I_SQ)
        put(ACID, R(b, r), root("E") + (12 if r % 2 else 0), I_ACID)
arp(["E"] * 8, range(ROWS_PER_PATTERN))
for ch in range(CHANNELS):
    off(ch, 30)
    grid[ch][31] = None
finish("BU")

# ---- OUT: the end, in B major (after the key change): a held B, the arpeggio thins out, the beat falls away
new_pattern()
melody(LEAD, [(N("B5"), 16)])
arp(["B"] * 8, [r for r in range(24) if r % 8 in GATE])
put(ACID, 0, root("B"), I_ACID); off(ACID, 15)
hit(DRUMS, 0, "crash"); hit(DRUMS, 8, "kick"); hit(DRUMS, 16, "kick")
put(VOX, 0, hoover_note("B"), I_HOOVER)
finish("OUT")

# ================================================================ the song: 64 slots
PATTERN_NAMES = ["INT1", "INT2", "P1", "P2", "P3", "P4", "D1", "D2", "D3", "D4", "KA", "KA2", "KB", "BR", "BU", "OUT"]
VERSES, DROPS, KEYUP = ["P1", "P2", "P3", "P4"], ["D1", "D2", "D3", "D4"], ["KA", "KA2", "KB", "KA2"]
ORDER = (["INT1", "INT2"] + VERSES + ["BU"] + DROPS              #  0-10
         + ["BR"] + VERSES + ["BU"] + DROPS + DROPS              # 11-24
         + ["INT2"] + VERSES + ["BR", "BU"] + DROPS + DROPS      # 25-39
         + ["BR", "P3", "P4", "BU"] + DROPS                      # 40-47
         + ["BU"] + KEYUP + KEYUP + ["BR", "BU"] + KEYUP         # 48-62: the key change
         + ["OUT"])                                              # 63

assert len(PATTERNS) == len(PATTERN_NAMES) == 16 and set(PATTERNS) == set(PATTERN_NAMES)
assert len(ORDER) == 64, len(ORDER)
assert set(ORDER) == set(PATTERN_NAMES)
ORDER_IDX = [PATTERN_NAMES.index(n) for n in ORDER]

# ------------------------------------------------------------------ write the file
def build_xm():
    n_pat = len(PATTERN_NAMES)
    out = bytearray()
    out += b"Extended Module: "
    out += b"Ode to Joy Synth v2".ljust(20, b"\0")
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
