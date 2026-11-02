"""
KOROBEINIKI TECHNO - 8 TRACKS v3, for 4 or 8 micro:bits. v3: the extras are drums and bass, no melody or chords.

Channels 1-4 are EXACTLY the 4-track tune (korobeiniki_techno_4ch_microbit.xm), so 4 boards still play the
whole tune. Channels 5-8 are extras that only ADD - nothing the tune needs lives there:
  5 BASS2 Tone: a second bass line - only the chord's root, fifth and octave (C-4 up), locked to the beat:
          half notes in the intro, 3+3+2 in the verses, offbeats in the drops, a pump speeding up in the build
  6 KIT2  hats and snare: light hats on the beat early on, a soft pulse in the breakdown, claps speeding up
          with the build roll, a second kit in the drops, hats thinning out at the end
  7 PERC  toms and claps: pick-ups in the intro, a tom groove in the verses and drops, tom runs in the fills,
          a heartbeat in the breakdown, toms speeding up in the build
  8 HITS  crashes, extra syncopated kicks, open hats and pews
Every extra track plays in every pattern; the parts start small and grow, so the drops are still the biggest.
Rules kept: no extra note a semitone from the lead (it would rub), no drum doubling the same drum on another
track on the same row, the pre-drop silences stay silent, tones C-4 to B-6, harmony/arp no lower than E-4.
Same 10 instruments, same setup (32 rows, speed 12 / tempo 150, 16 patterns, 64-slot order list).

Usage: python3 make_korobeiniki_8ch_v3_xm_microbit.py [output.xm]
(The original 4-track generator's notes follow.)
"""
#!/usr/bin/env python3
"""
Techno "Korobeiniki" (traditional folk tune behind the Tetris theme) - 4-CHANNEL, 10-INSTRUMENT .xm

For a simple tracker: ONE pitched instrument (the square-wave Tone) plus 9 single-pitch instruments
(drums, and two 'ew' sounds that each use at most 2 pitches). Only note, instrument and note-off:
no volume column, no effect commands, no slides.

Instruments (every drum is one simple sound - no layered samples):
   1 Tone (square)      pitched - the only one that plays a melody
   2 Kick               C-4
   3 Snare              C-4
   4 Clap               C-4
   5 Hat                C-4
   6 Open hat           C-4
   7 Crash              C-4
   8 Tom                2 pitches: G-4 (high) and C-4 (low)
   9 Pew zap            2 pitches: C-4 (low pew) and C-5 (higher, faster pew)
  10 Hoover             2 pitches: A-4 and E-4

Channels (each strictly monophonic):
  1 LEAD   Tone: the tune, build stutter
  2 BASS   Tone: acid-style bass line
  3 VOICE  Tone arp / pings in intros and breaks. In VERSES and DROPS it becomes a SECOND PERCUSSION + FX
           LANE (clap, hats, ghost snares, crash, Hoover stabs, toms, pew-pew). Pew zaps in builds.
  4 DRUMS  kick + hats lane (the instrument number picks the sound)

RESOLUTION: one row = one EIGHTH note (8 rows per bar, 2 rows per beat). A 32-row pattern is 4 bars.
Tempo 150 BPM (XM header: speed 12 ticks/row, tempo 150 -> 0.2 s per row).

Song: 16 UNIQUE patterns, played in an order list 64 long (= 256 bars, about 6m50s).

  Patterns (name = what it is):
    INT1 INT2       intro: INT1 = kick + hats + pings + sparse acid; INT2 adds clap, arp + Hoover stabs
    VA1 VA2         VERSE on tune A: four-on-the-floor kick, open hats, clap lane, acid (VA2 adds Hoover stabs)
    A1 A2           DROP, tune A: kick every beat, open hats, 2nd lane = crash/clap/hats/Hoover stabs/ghost snares,
                    snare + tom fill at the end of bar 4 (A1), snare/tom + pew-pew fill at the end of A2
    A1x A2x         DROP, tune A, variant (closed hats, ghost snares every bar, different acid line)
    B1 B2           DROP, tune B (same fill at the end of B2)
    BR1 BR2         BREAKDOWN: no drums, tune B soft over a held bass note and a quiet arp
    BU1 BU2         the 8-bar BUILD (rising stutter, pew-pew, snare roll) - ends in 1 beat of silence
    RLD             4-bar RELOAD: held Hoover + a teaser of tune A, then a quick mini-build and a silent beat
    OUT             outro: kick fades out

  Order list (64): see ORDER near the end of this script - edit it to reshuffle or shorten the song.

MICRO:BIT V2 SPEAKER VERSION
  The V2's built-in speaker is tiny and has no real bass, so in this version:
    - nothing pitched goes below C-4 (262 Hz): the bass is in octave 4 (BASS_OCT = 4), and an arp triad is
      lifted an octave if it would start below E-4 (330 Hz)
    - Hoover = A-4 / E-4, Tom = C-4 (low) / G-4 (high)
    - the drum PREVIEW samples are re-rendered so nothing sits below ~170 Hz: kick = quick 520->170 Hz sweep,
      toms 420->240 / 630->360 Hz, pew 1500->350 / 3000->700 Hz, snare/clap/hats/crash = noise bursts.
  The pitch LIMITS are unchanged (one Tone; every other instrument at most 2 pitches).

Usage: python3 make_korobeiniki_xm_microbit.py [output.xm]
"""
import math
import random
import struct
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "korobeiniki_techno_8ch_v3_microbit.xm"

# ------------------------------------------------------------------ config
SPEED, BPM = 12, 150          # 12 ticks/row @ tempo 150 => 1 row = 1 eighth note (0.2 s)
BASS_OCT = 4                 # micro:bit V2 speaker has no real bass: lowest bass note = C4 (262 Hz)
CHANNELS = 8                 # 1-4 = the 4-track tune, unchanged; 5-8 = the extras
ROWS_PER_BAR = 8              # eighth-note resolution
ROWS_PER_PATTERN = 32        # = 4 bars at eighth-note resolution
TOTAL_ROWS = ROWS_PER_PATTERN      # scratch grid = one pattern at a time

LEAD, ACID, VOX, DRUMS, BASS2, KIT2, PERC, HITS = range(8)
HARM = BASS2                     # (helpers from v2 still name it HARM)
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

# Korobeiniki (traditional). Written on a 16th grid, then halved: every length is even, so it is
# exactly representable in eighth notes. (note, length in ROWS) - 2 rows = quarter note.
_MEL_A16 = [
    ("E5", 4), ("B4", 2), ("C5", 2), ("D5", 4), ("C5", 2), ("B4", 2),
    ("A4", 4), ("A4", 2), ("C5", 2), ("E5", 4), ("D5", 2), ("C5", 2),
    ("B4", 6), ("C5", 2), ("D5", 4), ("E5", 4),
    ("C5", 4), ("A4", 4), ("A4", 8),
    (None, 2), ("D5", 4), ("F5", 2), ("A5", 4), ("G5", 2), ("F5", 2),
    ("E5", 6), ("C5", 2), ("E5", 4), ("D5", 2), ("C5", 2),
    ("B4", 4), ("B4", 2), ("C5", 2), ("D5", 4), ("E5", 4),
    ("C5", 4), ("A4", 4), ("A4", 8),
]
_MEL_B16 = [
    ("E5", 8), ("C5", 8), ("D5", 8), ("B4", 8), ("C5", 8), ("A4", 8), ("G#4", 16),
    ("E5", 8), ("C5", 8), ("D5", 8), ("B4", 8), ("C5", 4), ("E5", 4), ("A5", 8), ("G#5", 16),
]
assert all(l % 2 == 0 for _, l in _MEL_A16 + _MEL_B16)
MEL_A = [(n, l // 2) for n, l in _MEL_A16]
MEL_B = [(n, l // 2) for n, l in _MEL_B16]
for m in (MEL_A, MEL_B):
    assert sum(l for _, l in m) == 8 * ROWS_PER_BAR


def melody(ch, inst, notes, r0=0, r1=ROWS_PER_PATTERN):
    """Place the part of a tune whose notes start in rows [r0, r1), shifted so r0 becomes row 0."""
    r = 0
    for name, ln in notes:
        if r0 <= r < r1:
            row = r - r0
            if name is None:
                off(ch, row, force=False)
            else:
                put(ch, row, N(name), inst)
                if ln >= 4:
                    off(ch, row + ln - 1)    # 1-row gap on half notes and longer
        r += ln


CHORDS = {"Am": ("A", [0, 3, 7]), "Dm": ("D", [0, 3, 7]), "E": ("E", [0, 4, 7]),
          "C": ("C", [0, 4, 7]), "G": ("G", [0, 4, 7])}
PROG_A = ["Am", "Am", "E", "Am", "Dm", "C", "E", "Am"]
PROG_B = ["Am", "G", "Am", "E", "Am", "G", "Am", "E"]
PROG_BUILD = ["Am"] * 4 + ["Dm", "Dm", "E", "E"]
PROG_RLD = ["Am", "Am", "Dm", "E"]


VOICE_FLOOR = N("E4")            # lead / voice Tone: nothing below E4 (330 Hz)


def chord_notes(name, octave):
    root, iv = CHORDS[name]
    base = N(root + str(octave))
    while base < VOICE_FLOOR:        # lift the whole triad an octave rather than let it dip too low
        base += 12
    return [base + i for i in iv]


def bass_root(name):
    return N(CHORDS[name][0] + str(BASS_OCT))


# ---------------- ACID (channel 2): 8 steps per bar (one per row). Step = (chord tone 0-3, octave 0/1) or None.
ACID_TONES = {"Am": [0, 3, 7, 10], "Dm": [0, 3, 7, 10], "E": [0, 4, 7, 10],
              "C": [0, 4, 7, 11], "G": [0, 4, 7, 10]}      # root, 3rd, 5th, 7th (semitones)
ACID_PATTERNS = {
    "A": [(0, 0), (0, 0), (0, 1), (0, 0), (0, 0), (0, 1), (2, 0), (3, 0)],      # driving
    "B": [(0, 0), None, (0, 1), (0, 0), None, (2, 0), (2, 0), (3, 0)],          # syncopated
    "C": [(0, 0), (0, 1), (0, 0), (0, 1), (0, 0), (0, 1), (2, 0), (0, 1)],      # rolling octaves
    "D": [None, (0, 0), None, (0, 0), None, (0, 0), None, (0, 1)],              # offbeat
    "E": [(0, 0), None, (0, 0), None, (0, 0), None, (0, 0), None],              # on the beat
    "F": [(0, 0), (0, 1)] * 4,                                                  # build: octave pump
}
for _p in ACID_PATTERNS.values():
    assert len(_p) == ROWS_PER_BAR


def acid_bar(bar, chord, pattern, last=ROWS_PER_BAR):
    root = N(CHORDS[chord][0] + str(BASS_OCT))
    offs = ACID_TONES[chord]
    pat, sounding = ACID_PATTERNS[pattern], False
    for st in range(min(ROWS_PER_BAR, last)):
        step, r = pat[st], R(bar, st)
        if step is None:
            if sounding or st == 0:
                off(ACID, r)                       # gate closes on rests
            sounding = False
            continue
        tone, octv = step
        put(ACID, r, root + offs[tone] + 12 * octv, I_ACID)
        sounding = True


# ---------------- VOX (channel 3): utility voice
def pings(bar, chord):
    tones = chord_notes(chord, 5)
    for k in range(4):
        r = 2 * k + 1                              # the offbeat of every beat
        put(VOX, R(bar, r), tones[[0, 1, 2, 1][k]], I_SAW)
        off(VOX, R(bar, r + 1), force=False)


def arp(bar, chord):
    tones, seq = chord_notes(chord, 4), [0, 1, 2, 1]
    for r in range(ROWS_PER_BAR):
        put(VOX, R(bar, r), tones[seq[r % 4]], I_P12)


def hoover_note(chord):
    """The Hoover only ever plays 2 pitches: E-4 over the E chord, A-4 over everything else."""
    return N("E4") if chord == "E" else N("A4")


def arp_stab(bar, chord):
    """Eighth-note arp with Hoover stabs answering on the offbeats of beats 2 and 4 (rows 3 and 7)."""
    tones, seq = chord_notes(chord, 4), [0, 1, 2, 1]
    for r in range(ROWS_PER_BAR):
        if r in (3, 7):
            put(VOX, R(bar, r), hoover_note(chord), I_HOOVER)
            off(VOX, R(bar, r + 1), force=False)
        else:
            put(VOX, R(bar, r), tones[seq[r % 4]], I_P12)


# ---------------- DRUMS (channel 4): one kit, one sound per row
def drums_groove(bar, hats="closed", clap=True, crash=False, last=ROWS_PER_BAR):
    """Kick on beats 1 and 3, clap on beats 2 and 4 (kick on every beat when clap=False), hats on the
    offbeat rows. crash=True: a lone crash on the downbeat (no kick), left to ring through the first half."""
    ev = {}
    for beat in range(4):
        r = beat * 2
        ev[r] = I_CLAP if (clap and beat in (1, 3)) else I_KICK
        if hats == "closed":
            ev[r + 1] = I_HAT
        elif hats == "open":
            ev[r + 1] = I_OHAT
        elif hats == "dense":
            ev[r + 1] = I_OHAT if beat % 2 == 0 else I_HAT
    if crash:
        ev = {r: i for r, i in ev.items() if r >= 4}
        ev[0] = I_CRASH
    for r, inst in ev.items():
        if r < last:
            put(DRUMS, R(bar, r), C4, inst)


def roll_bar(bar, level, last=ROWS_PER_BAR):
    """Build roll, eighth-note resolution: level 1 = kick on the beats + snare on the offbeats of 2 and 4,
    level 2 = snare on every offbeat, level 3 = kick on 1 and 3, snare on every other row."""
    for r in range(min(ROWS_PER_BAR, last)):
        if level == 1:
            inst = I_SNARE if r in (3, 7) else (I_KICK if r % 2 == 0 else None)
        elif level == 2:
            inst = I_KICK if r % 2 == 0 else I_SNARE
        else:
            inst = I_KICK if r in (0, 4) else I_SNARE
        if inst:
            put(DRUMS, R(bar, r), C4, inst)


def fill_drums(bar):
    """Last bar of a drop: one beat of groove, kick + snare, then a high / low tom."""
    drums_groove(bar, hats="closed", clap=True, last=4)
    put(DRUMS, R(bar, 4), C4, I_KICK)
    put(DRUMS, R(bar, 5), C4, I_SNARE)
    put(DRUMS, R(bar, 6), N("G4"), I_TOM)
    put(DRUMS, R(bar, 7), N("C4"), I_TOM)


# ================================================================ the 16 patterns (4 bars each)

# ---- INT1: kick + closed hats, offbeat pings, acid on the beat (Am Am E Am)
new_pattern()
for j in range(4):
    drums_groove(j, hats="closed", clap=False)
    acid_bar(j, PROG_A[j], "E")
    pings(j, PROG_A[j])
finish_pattern("INT1")

# ---- INT2: + clap, offbeat acid, arp with Hoover stabs (Dm C E Am)
new_pattern()
for j in range(4):
    drums_groove(j, hats="closed", clap=True)
    acid_bar(j, PROG_A[4 + j], "D")
    arp_stab(j, PROG_A[4 + j])
finish_pattern("INT2")


def perc_bar(bar, chord, hat_inst, crash=False, ghost=False, stabs=True, fill=None):
    """One bar of the TWO-LANE kit (eighth-note rows).
    DRUMS lane (ch4): kick on every beat, a hat on every offbeat.
    VOICE lane (ch3): crash/hat on 1, clap on 2 and 4, hat on 3, Hoover stabs on the offbeats of 2 and 4
                      (or hats if stabs=False), optional ghost snares on the offbeats of 1 and 3.
    fill='mid': snare roll on the DRUMS lane over the last half bar + tom run on the VOICE lane.
    fill='end': kick, snare, high tom, low tom on the DRUMS lane + 4 pew-pew zaps on the VOICE lane."""
    half = 4 if fill else ROWS_PER_BAR
    for beat in range(4):
        if 2 * beat < half:
            put(DRUMS, R(bar, 2 * beat), C4, I_KICK)
        if 2 * beat + 1 < half:
            put(DRUMS, R(bar, 2 * beat + 1), C4, hat_inst)
    put(VOX, R(bar, 0), C4, I_CRASH if crash else I_HAT)
    put(VOX, R(bar, 2), C4, I_CLAP)
    if stabs:
        put(VOX, R(bar, 3), hoover_note(chord), I_HOOVER)
    else:
        put(VOX, R(bar, 3), C4, I_HAT)
    if ghost and not fill:
        put(VOX, R(bar, 1), C4, I_SNARE)
        put(VOX, R(bar, 5), C4, I_SNARE)
    if fill is None:
        put(VOX, R(bar, 4), C4, I_HAT)
        put(VOX, R(bar, 6), C4, I_CLAP)
        if stabs:
            put(VOX, R(bar, 7), hoover_note(chord), I_HOOVER)
        else:
            put(VOX, R(bar, 7), C4, I_HAT)
    elif fill == "mid":
        put(DRUMS, R(bar, 4), C4, I_KICK)
        for r in (5, 6, 7):
            put(DRUMS, R(bar, r), C4, I_SNARE)
        put(VOX, R(bar, 4), C4, I_HAT)
        for r, pitch in ((5, "G4"), (6, "G4"), (7, "C4")):
            put(VOX, R(bar, r), N(pitch), I_TOM)
    elif fill == "end":
        put(DRUMS, R(bar, 4), C4, I_KICK)
        put(DRUMS, R(bar, 5), C4, I_SNARE)
        put(DRUMS, R(bar, 6), N("G4"), I_TOM)
        put(DRUMS, R(bar, 7), N("C4"), I_TOM)
        for q, pitch in enumerate(("C4", "C4", "C5", "C5")):
            put(VOX, R(bar, 4 + q), N(pitch), I_ZAP)


# ---- VA1 VA2: verse - tune A over the two-lane kit (tone only on the lead + bass)
def verse_pat(name, k):
    new_pattern()
    melody(LEAD, I_SQ, MEL_A, k * ROWS_PER_PATTERN, (k + 1) * ROWS_PER_PATTERN)
    for j in range(4):
        i = 4 * k + j
        perc_bar(j, PROG_A[i], I_OHAT, crash=(i == 0), stabs=(k == 1))
        acid_bar(j, PROG_A[i], "D" if k == 0 else "A")
    finish_pattern(name)


verse_pat("VA1", 0)
verse_pat("VA2", 1)


# ---- A1 A2 A1x A2x B1 B2: the drops. Tone only on the lead (tune) + bass (acid); everything else is kit/FX.
def drop_pat(name, k, mel, prog, acid_seq, hat_inst, ghost_all=False):
    new_pattern()
    melody(LEAD, I_SQ, mel, k * ROWS_PER_PATTERN, (k + 1) * ROWS_PER_PATTERN)
    for j in range(4):
        i = 4 * k + j                      # bar number within the 8-bar tune
        c = prog[i]
        fill = "end" if i == 7 else ("mid" if i == 3 else None)
        perc_bar(j, c, hat_inst, crash=(i in (0, 4)), ghost=(ghost_all or i % 2 == 1), fill=fill)
        if i == 7:
            acid_bar(j, c, acid_seq[i], 6)
            off(ACID, R(j, 6))
        else:
            acid_bar(j, c, acid_seq[i])
    finish_pattern(name)


ACID_A = ["A", "A", "B", "A", "A", "A", "B", "C"]
ACID_AX = ["C", "B", "C", "A", "C", "B", "C", "C"]
ACID_B = ["C", "B", "C", "C", "C", "B", "C", "C"]
drop_pat("A1", 0, MEL_A, PROG_A, ACID_A, I_OHAT)
drop_pat("A2", 1, MEL_A, PROG_A, ACID_A, I_OHAT)
drop_pat("A1x", 0, MEL_A, PROG_A, ACID_AX, I_HAT, ghost_all=True)
drop_pat("A2x", 1, MEL_A, PROG_A, ACID_AX, I_HAT, ghost_all=True)
drop_pat("B1", 0, MEL_B, PROG_B, ACID_B, I_OHAT)
drop_pat("B2", 1, MEL_B, PROG_B, ACID_B, I_OHAT, ghost_all=True)


# ---- BR1 BR2: breakdown - no drums, tune B soft over a held bass note + quiet arp
def break_pat(name, k):
    new_pattern()
    melody(LEAD, I_SQ, MEL_B, k * ROWS_PER_PATTERN, (k + 1) * ROWS_PER_PATTERN)
    for j in range(4):
        c = PROG_B[4 * k + j]
        put(ACID, R(j), bass_root(c), I_ACID)
        off(ACID, R(j, ROWS_PER_BAR - 1))
        arp(j, c)
    finish_pattern(name)


break_pat("BR1", 0)
break_pat("BR2", 1)

# ---- BU1 BU2: the 8-bar build, 4 bars per pattern. Everything climbs, then 1 beat of silence.
BUILD_ACID = ["D", "D", "D", "D", "C", "C", "F", "F"]
BUILD_ROWS = 8 * ROWS_PER_BAR - 2                         # the last beat (2 rows) is silent
LEAD_CLIMB = [N("E5"), N("E5"), N("A5"), N("A5"), N("C6"), N("C6"), N("E6"), N("E6")]
LEAD_STEP = (2, 2, 1, 1, 1, 1, 1, 1)                      # stutter: every beat, then every eighth
ZAP_RATE = ((4, 1), (4, 1), (2, 1), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0))   # (every n rows, offset)
PEW_NOTES = [N("C4"), N("C5")]                            # only 2 pitches: low pew first half, high pew second half
trig = [g for g in range(BUILD_ROWS)
        if (g % ROWS_PER_BAR) % ZAP_RATE[g // ROWS_PER_BAR][0] == ZAP_RATE[g // ROWS_PER_BAR][1]]
zap_at = {g: PEW_NOTES[int(n / len(trig) * len(PEW_NOTES))] for n, g in enumerate(trig)}

for k in range(2):
    new_pattern()
    for j in range(4):
        i = 4 * k + j
        c = PROG_BUILD[i]
        last = 6 if i == 7 else ROWS_PER_BAR
        if i < 2:
            drums_groove(j, hats="closed", clap=False)
        else:
            roll_bar(j, (1, 1, 2, 2, 3, 3)[i - 2], last)
        acid_bar(j, c, BUILD_ACID[i], last)
    for rr in range(ROWS_PER_PATTERN):
        g = k * ROWS_PER_PATTERN + rr
        if g >= BUILD_ROWS:
            break
        bi = g // ROWS_PER_BAR
        if (g - bi * ROWS_PER_BAR) % LEAD_STEP[bi] == 0:  # stuttering lead, climbing every 2 bars
            put(LEAD, rr, LEAD_CLIMB[bi], I_SQ)
        if g in zap_at:
            put(VOX, rr, zap_at[g], I_ZAP)
    if k == 1:
        for ch in range(CHANNELS):                        # the pre-drop silence
            off(ch, BUILD_ROWS - ROWS_PER_PATTERN)
    finish_pattern(f"BU{k + 1}")

# ---- RLD: reload - held Hoover + teaser of tune A (2 bars), then a quick mini-build and a silent beat
new_pattern()
melody(LEAD, I_SQ, MEL_A, 0, 2 * ROWS_PER_BAR)
for j in (0, 1):
    put(VOX, R(j), hoover_note(PROG_RLD[j]), I_HOOVER)
    off(VOX, R(j, ROWS_PER_BAR - 1))
    acid_bar(j, PROG_RLD[j], "E")
RLD_ROWS = ROWS_PER_PATTERN - 2
for j in (2, 3):
    last = 6 if j == 3 else ROWS_PER_BAR
    roll_bar(j, (2, 3)[j - 2], last)
    acid_bar(j, PROG_RLD[j], "C" if j == 2 else "F", last)
for rr in range(2 * ROWS_PER_BAR, RLD_ROWS):
    t = (rr - 2 * ROWS_PER_BAR) / (RLD_ROWS - 2 * ROWS_PER_BAR)
    put(LEAD, rr, N("E5") if rr < 3 * ROWS_PER_BAR else N("A5"), I_SQ)
    put(VOX, rr, (N("C4"), N("C5"))[int(t * 2)], I_ZAP)
for ch in range(CHANNELS):
    off(ch, RLD_ROWS)
finish_pattern("RLD")

# ---- OUT: groove thins out, then just the kick
new_pattern()
drums_groove(0, hats="closed", clap=False)
pings(0, "Am")
drums_groove(1, hats=None, clap=False)
drums_groove(2, hats=None, clap=False, last=4)
drums_groove(3, hats=None, clap=False, last=1)
finish_pattern("OUT")


# ================================================================ v8: the extra tracks 5-8 (only ADD)
PATTERN_PROG = {"INT1": PROG_A[:4], "INT2": PROG_A[4:], "VA1": PROG_A[:4], "VA2": PROG_A[4:],
                "A1": PROG_A[:4], "A2": PROG_A[4:], "A1x": PROG_A[:4], "A2x": PROG_A[4:],
                "B1": PROG_B[:4], "B2": PROG_B[4:], "BR1": PROG_B[:4], "BR2": PROG_B[4:],
                "BU1": PROG_BUILD[:4], "BU2": PROG_BUILD[4:], "RLD": PROG_RLD, "OUT": ["Am"] * 4}
DROPS = ("A1", "A2", "A1x", "A2x", "B1", "B2")
SCALE = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G"}      # A minor, letter by letter


def last_row(name):
    """Rows from here on stay silent (the pre-drop silences)."""
    return {"BU2": BUILD_ROWS - ROWS_PER_PATTERN, "RLD": RLD_ROWS}.get(name, ROWS_PER_PATTERN)


def lead_at(g, row):
    for r in range(row, -1, -1):
        c = g[LEAD][r]
        if c is not None:
            return None if c[0] == NOTE_OFF else c[0]
    return None


def rubs(g, row, note):
    ld = lead_at(g, row)
    return ld is not None and (note - ld) % 12 in (1, 11)


def harmony_below(note, chord):
    """If the lead is on a note of the chord: the next chord note down. Otherwise the note two letters down
    in A minor (a third), G# instead of G over the E chord."""
    root, iv = CHORDS[chord]
    pcs = [(N(root + "4") + i - 1) % 12 for i in iv]
    if (note - 1) % 12 in pcs:
        x = note - 1
        while (x - 1) % 12 not in pcs:
            x -= 1
        return x
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    letter = names[(note - 1) % 12][0]
    idx = [k for k, v in SCALE.items() if v == letter][0]
    want = SCALE[(idx - 2) % 7]
    if want == "G" and chord == "E":
        want = "G#"
    x = note - 1
    while names[x % 12] != want:
        x -= 1
    return x + 1


def free_drum(g, ch, row, choices):
    """Put the first drum in choices that no other track plays on this row."""
    taken = {g[c][row][:2] for c in range(CHANNELS) if c != ch and g[c][row] is not None}
    for note, inst in choices:
        if (note, inst) not in taken:
            g[ch][row] = (note, inst, 0)
            return


HAT, OHAT, SNARE, CLAP = (C4, I_HAT), (C4, I_OHAT), (C4, I_SNARE), (C4, I_CLAP)
TOM_HI, TOM_LO, CRASH = (N("G4"), I_TOM), (N("C4"), I_TOM), (C4, I_CRASH)
PEW_LO, PEW_HI = (N("C4"), I_ZAP), (N("C5"), I_ZAP)
KIT2_BAR = [HAT, HAT, SNARE, HAT, HAT, HAT, SNARE, OHAT]
INTROS, VERSES, BREAKS, BUILDS = ("INT1", "INT2"), ("VA1", "VA2"), ("BR1", "BR2"), ("BU1", "BU2")


def sounding(g, ch, row):
    for r in range(row, -1, -1):
        c = g[ch][r]
        if c is not None:
            return None if c[0] == NOTE_OFF else c[0]
    return None


def tone(g, ch, row, x):
    """A tone, unless it would rub a semitone against the lead or the harmony."""
    hm = sounding(g, HARM, row)
    if not rubs(g, row, x) and not (hm is not None and (x - hm) % 12 in (1, 11)):
        g[ch][row] = (x, I_SQ, 0)


def pad(g, ch, r0, r1, chord):
    """A held chord note from r0, chosen so it rubs the lead as little as possible; cut at the first rub."""
    best = None
    for x in chord_notes(chord, 4)[1:] + chord_notes(chord, 4)[:1]:        # third, fifth, then root
        clash = next((r for r in range(r0, r1) if rubs(g, r, x)), r1)
        if best is None or clash > best[1]:
            best = (x, clash)
    x, clash = best
    if clash == r0:
        return
    g[ch][r0] = (x, I_SQ, 0)
    if clash - r0 >= 2:
        g[ch][min(clash, r1) - 1] = (NOTE_OFF, 0, 0)


def drum(g, row, choices):
    free_drum(g, KIT2, row, choices)


TONE_CHANNELS = (LEAD, ACID, VOX)


def bass_ok(g, row, x):
    """No semitone rub against anything tonal sounding on tracks 1-3 at this row."""
    for ch in TONE_CHANNELS:
        y = sounding(g, ch, row)
        if y is not None and (x - y) % 12 in (1, 11):
            return False
    return True


def bass(g, row, x):
    if bass_ok(g, row, x):
        g[BASS2][row] = (x, I_SQ, 0)


for name in list(PATTERNS):
    g = PATTERNS[name]
    prog = PATTERN_PROG[name]
    stop = last_row(name)
    drop = name in DROPS
    for bar in range(4):
        chord = prog[bar]
        r0 = R(bar)
        if r0 >= stop:
            break
        root = bass_root(chord)                                   # C-4 .. B-4
        fifth, octave = root + 7, root + 12
        gi = (4 if name == "BU2" else 0) + bar if name in BUILDS else bar      # bar number within the build
        for st in range(ROWS_PER_BAR):
            row = r0 + st
            if row >= stop:
                break
            fill_half = bar == 3 and st >= 4
            # ---------- 5 BASS2: a second bass line - root, fifth and octave only, locked to the beat
            if name == "INT1" and st in (0, 4):
                bass(g, row, root)                                # half notes
            elif name in ("INT2",) + VERSES and st in (0, 3, 6):
                bass(g, row, (root, fifth, octave)[(0, 3, 6).index(st)])          # 3+3+2
            elif drop and st % 2 == 1 and not fill_half:
                bass(g, row, octave if st in (1, 5) else fifth)   # offbeat bass
            elif drop and fill_half and st == 4:
                bass(g, row, root)
            elif name in BREAKS and st in (0, 4):
                bass(g, row, root if st == 0 else fifth)          # calm half notes
            elif name in BUILDS and st % (1 if gi >= 4 else 2) == 0:
                bass(g, row, octave if st % 2 else root)          # the pump speeds up
            elif name == "RLD" and (st in (0, 4) if bar < 2 else True):
                bass(g, row, root if (bar < 2 or st % 2 == 0) else octave)
            elif name == "OUT" and bar < 3 and st in (0, 4) and not (bar == 2 and st == 4):
                bass(g, row, root)
            # ---------- 6 KIT2: hats and snare
            if drop:
                drum(g, row, [SNARE, CLAP, HAT] if fill_half else [KIT2_BAR[st], HAT, OHAT, CLAP])
            elif name in INTROS + VERSES or (name == "RLD" and bar < 2) or (name == "OUT" and bar < 2):
                if st % 2 == 0:
                    drum(g, row, [HAT, OHAT])                     # light hats on the beat
            elif name in BREAKS:
                if st in (0, 4):
                    drum(g, row, [HAT])                           # a soft pulse, the breakdown has no drums
            elif name in BUILDS or name == "RLD":
                every = 4 if gi < 4 else (2 if gi < 6 else 1)     # claps speed up with the roll
                if name == "RLD":
                    every = 2 if bar == 2 else 1
                if st % every == (2 % every):
                    drum(g, row, [CLAP, SNARE, HAT])
            # ---------- 7 PERC: toms and claps
            if name in INTROS and st in (3, 7):
                free_drum(g, PERC, row, [TOM_LO if st == 3 else TOM_HI, TOM_HI, TOM_LO])
            elif name in VERSES and st in (3, 5, 7):
                free_drum(g, PERC, row, [(TOM_LO, TOM_HI, TOM_LO)[(3, 5, 7).index(st)], TOM_HI, TOM_LO])
            elif drop and fill_half:
                free_drum(g, PERC, row, [(TOM_HI, TOM_HI, TOM_LO, TOM_LO)[st - 4], SNARE, CLAP])   # tom run
            elif drop and st % 2 == 1:
                free_drum(g, PERC, row, [TOM_HI if st in (1, 5) else TOM_LO, CLAP, TOM_LO, TOM_HI])
            elif name in BREAKS and st == 6:
                free_drum(g, PERC, row, [TOM_LO])                 # a heartbeat
            elif name in BUILDS and st % (4 if gi < 4 else (2 if gi < 6 else 1)) == 1 % (4 if gi < 4 else (2 if gi < 6 else 1)):
                free_drum(g, PERC, row, [TOM_LO if gi < 4 else TOM_HI, TOM_HI, TOM_LO, CLAP])
            elif name == "RLD" and bar >= 2:
                free_drum(g, PERC, row, [TOM_HI if st % 2 else TOM_LO, TOM_LO, TOM_HI])
            elif name == "OUT" and bar < 3 and st == 0:
                free_drum(g, PERC, row, [TOM_LO])
            # ---------- 8 HITS: crashes, extra kicks, open hats, pews
            if name in INTROS and st == 7:
                free_drum(g, HITS, row, [PEW_HI if bar % 2 else PEW_LO])
            elif name == "INT2" and row == 0:
                free_drum(g, HITS, row, [CRASH])
            elif name in VERSES and st == 7:
                free_drum(g, HITS, row, [OHAT, PEW_LO])
            elif name in VERSES and bar == 3 and st == 5:
                free_drum(g, HITS, row, [PEW_HI])
            elif drop and st == 0 and bar in (1, 2):
                free_drum(g, HITS, row, [CRASH, OHAT])
            elif drop and st == 5 and not fill_half:
                free_drum(g, HITS, row, [(C4, I_KICK)])           # a syncopated extra kick
            elif drop and st == 3:
                free_drum(g, HITS, row, [(C4, I_KICK), OHAT])
            elif name in BREAKS and st == 4 and bar % 2 == 1:
                free_drum(g, HITS, row, [PEW_LO])
            elif name in BUILDS and st % (4 if gi < 6 else 2) == 0:
                free_drum(g, HITS, row, [CRASH if gi == 7 and st == 0 else (C4, I_KICK), OHAT])
            elif name == "RLD" and (row == 0 or (bar >= 2 and st % 2 == 0)):
                free_drum(g, HITS, row, [CRASH if row == 0 else (C4, I_KICK), OHAT])
            elif name == "OUT" and st == 0 and bar < 3:
                free_drum(g, HITS, row, [CRASH if bar == 0 else (C4, I_KICK), OHAT])
    # the bass gate: short, punchy notes - an off on the next row unless another note starts there
    for row in range(stop):
        c = g[BASS2][row]
        if c is not None and c[0] != NOTE_OFF and row + 1 < stop and g[BASS2][row + 1] is None:
            g[BASS2][row + 1] = (NOTE_OFF, 0, 0)
    for ch in (BASS2, KIT2, PERC, HITS):          # self-contained, like the 4 tracks
        if g[ch][0] is None:
            g[ch][0] = (NOTE_OFF, 0, 0)

# ================================================================ the song: 64 slots from 16 patterns
PATTERN_NAMES = ["INT1", "INT2", "VA1", "VA2", "A1", "A2", "A1x", "A2x", "B1", "B2",
                 "BR1", "BR2", "BU1", "BU2", "RLD", "OUT"]
INTRO, VERSE, BREAK, BUILD = ["INT1", "INT2"], ["VA1", "VA2"], ["BR1", "BR2"], ["BU1", "BU2"]
DROP_A, DROP_AX, DROP_B, RELOAD = ["A1", "A2"], ["A1x", "A2x"], ["B1", "B2"], ["RLD"]
ORDER = (INTRO + VERSE + BREAK + BUILD + DROP_A + DROP_B                          #  0-11
         + VERSE + BREAK + BUILD + DROP_B + DROP_AX + DROP_A                      # 12-23
         + ["INT2", "INT1"] + BREAK + RELOAD + DROP_AX + DROP_B + DROP_A          # 24-34
         + VERSE + BREAK + BUILD + DROP_B + DROP_AX + RELOAD                      # 35-45
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
    out += b"Korobeiniki 8trk v3".ljust(20, b"\0")
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
