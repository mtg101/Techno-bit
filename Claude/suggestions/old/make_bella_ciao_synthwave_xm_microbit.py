"""
BELLA CIAO - synthwave, for 4 micro:bits. Same setup and the same 10 instruments as the other tunes.

Traditional Italian folk melody only (checked against 8notes.com's violin MIDI, moved to A minor).

SYNTHWAVE ON A 150 BPM GRID: the rows still last 200 ms, but the music is felt at half speed (75 BPM), so one
row is a 16th note. A synthwave "bar" is 16 rows = 2 of our 8-row bars, and a pattern holds 2 of them.
  - DRUMS: half-time. Kick on beats 1 and 3, a big snare on 2 and 4, hats between. Tom fills, crashes.
  - ACID: the classic synthwave bass - a steady stream of 16th notes on the root, with octave jumps.
  - VOX: a two-octave arpeggio in 16ths running through everything; in the choruses Hoover hits cut in like brass.
  - LEAD: the melody stretched to half speed (every note twice as long), an octave lower in the verses (E4-F5)
    and up an octave in the choruses (E5-F6). No pew-pews, no acid octave pump.

Setup (unchanged): 4 channels, 32 rows per pattern, speed 12 / tempo 150, 16 patterns, 64-slot order list,
no volume column, no effects, the same 10 instruments. Pitched parts C-4 to B-6; lead and voice no lower than E-4.

Patterns: INT1 INT2 V1 V2 V3 V4 C1 C2 C3 C4 HK BR1 BR2 BU1 BU2 OUT
  V1-V4 and C1-C4 = the whole 8-bar tune, stretched to 4 patterns (V = verse, C = chorus).
  HK = the hook ("bella ciao, bella ciao, bella ciao ciao ciao") with the Hoover answering.

Usage: python3 make_bella_ciao_synthwave_xm_microbit.py [output.xm]
"""
import math
import random
import struct
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "bella_ciao_synthwave_4ch_microbit.xm"

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

# ================================================================ BELLA CIAO SYNTHWAVE
CHORDS = {"Am": ("A", [0, 3, 7]), "A7": ("A", [0, 4, 7]), "Dm": ("D", [0, 3, 7]), "E7": ("E", [0, 4, 7])}
ROOT = {"Am": N("A4"), "A7": N("A4"), "Dm": N("D4"), "E7": N("E4")}
UNIT = 8                                   # one chord lasts at least 8 rows (2 beats at 75 BPM)
SW_BAR = 16                                # a synthwave bar: 16 rows = 4 beats at 75 BPM
VOICE_FLOOR = N("E4")

# The verse from the MIDI (A minor, lead octave): (start row, length, note) on the 8th-note grid ...
VERSE = [(0, 1, "E5"), (1, 1, "A5"), (2, 1, "B5"), (3, 1, "C6"), (4, 4, "A5"),
         (8, 1, "E5"), (9, 1, "A5"), (10, 1, "B5"), (11, 1, "C6"), (12, 4, "A5"),
         (16, 1, "E5"), (17, 1, "A5"), (18, 1, "B5"), (19, 2, "C6"), (21, 1, "B5"), (22, 1, "A5"), (23, 2, "C6"),
         (25, 1, "B5"), (26, 1, "A5"), (27, 2, "E6"), (29, 2, "E6"), (31, 1, "E6"),
         (32, 1, "E6"), (33, 1, "D6"), (34, 1, "E6"), (35, 1, "F6"), (36, 4, "F6"),
         (40, 1, "F6"), (41, 1, "E6"), (42, 1, "D6"), (43, 1, "F6"), (44, 3, "E6"),
         (48, 1, "E6"), (49, 1, "D6"), (50, 1, "C6"), (51, 1, "B5"), (53, 1, "E6"), (55, 1, "B5"), (57, 1, "C6"),
         (59, 5, "A5")]
PROG8 = ["Am"] * 7 + ["A7", "A7", "Dm", "Dm", "Am", "Am", "E7", "E7", "Am"]      # per 4 rows of the original
# ... stretched to half speed: every start and length doubled. 128 rows = 4 patterns.
SLOW = [(2 * r, 2 * l, n) for r, l, n in VERSE]
PROG = PROG8                                                                    # now one chord per 8 rows


def part(events, r0, r1):
    return [(r - r0, l, n) for r, l, n in events if r0 <= r < r1]


def melody(ch, events, shift=0):
    ev = sorted(events)
    for i, (r, l, n) in enumerate(ev):
        put(ch, r, N(n) + shift, I_SQ)
        nxt = ev[i + 1][0] if i + 1 < len(ev) else None
        end = r + l - (1 if l >= 4 else 0)               # long notes get a 1-row gap so they re-articulate
        if nxt is None or end < nxt:
            off(ch, end, force=False)


def chord_tones(name):
    root, iv = CHORDS[name]
    base = N(root + "4")
    while base < VOICE_FLOOR:
        base += 12
    return [base + i for i in iv]


def hoover_note(chord):
    return N("E4") if chord == "E7" else N("A4")


SOUND = {"lo": (N("C4"), I_TOM), "hi": (N("G4"), I_TOM), "clap": (C4, I_CLAP), "hat": (C4, I_HAT),
         "ohat": (C4, I_OHAT), "crash": (C4, I_CRASH), "kick": (C4, I_KICK), "snare": (C4, I_SNARE)}


def hit(ch, row, what):
    if what:
        note, inst = SOUND[what]
        put(ch, row, note, inst)


# ---------------- ACID: 16th-note synthwave bass, one chord per 8 rows
BASS = {
    "pulse":  [(0, 0)] * 8,                                                    # steady 16ths on the root
    "octave": [(0, 0), (0, 0), (0, 1), (0, 0), (0, 0), (0, 0), (0, 1), (0, 0)],  # with octave jumps
    "gallop": [(0, 0), "off", (0, 0), (0, 0), (0, 0), "off", (0, 0), (0, 0)],
    "hold":   [(0, 0), None, None, None, None, None, None, "off"],
}


def bass(unit, chord, style, last=UNIT):
    for k, step in enumerate(BASS[style][:last]):
        r = unit * UNIT + k
        if step is None:
            continue
        if step == "off":
            off(ACID, r)
        else:
            semis, octv = step
            put(ACID, r, ROOT[chord] + semis + 12 * octv, I_ACID)


# ---------------- VOX: the arpeggiator. Two octaves up and back down, one note per row (a 16th at 75 BPM).
ARP_SHAPE = [0, 1, 2, 3, 4, 5, 4, 3]          # index into [t0, t1, t2, t0+12, t1+12, t2+12]


def arp(unit, chord, rows=range(UNIT)):
    t = chord_tones(chord)
    ladder = t + [x + 12 for x in t]
    for k in rows:
        put(VOX, unit * UNIT + k, ladder[ARP_SHAPE[k]], I_P12)


# ---------------- DRUMS: half-time, 16 rows = one synthwave bar
VERSE_KIT = ["kick", None, "hat", None, "snare", None, "hat", None,
             "kick", None, "hat", None, "snare", None, "hat", None]
CHORUS_KIT = ["kick", "hat", "hat", "hat", "snare", "hat", "hat", "kick",
              "kick", "hat", "hat", "hat", "snare", "hat", "ohat", "hat"]
TOM_FILL = ["snare", "snare", "hi", "hi", "hi", "lo", "lo", "lo"]       # the last 8 rows of a section


def drums_bar(swb, kit, crash=False, fill=False):
    for k in range(SW_BAR):
        hit(DRUMS, swb * SW_BAR + k, kit[k])
    if crash:
        hit(DRUMS, swb * SW_BAR, "crash")
    if fill:
        for k, what in enumerate(TOM_FILL):
            hit(DRUMS, swb * SW_BAR + 8 + k, what)


def finish(name):
    finish_pattern(name)


# ================================================================ the 16 patterns
# ---- INT1: the arpeggio alone for a bar, then the bass joins (Am)
new_pattern()
for u in range(4):
    arp(u, "Am")
for u in (2, 3):
    bass(u, "Am", "pulse")
finish("INT1")

# ---- INT2: drums come in (verse kit), Hoover swell at the start of each bar, tom fill at the end
new_pattern()
for u in range(4):
    arp(u, "Am" if u < 3 else "E7")
    bass(u, "Am" if u < 3 else "E7", "pulse")
drums_bar(0, VERSE_KIT)
drums_bar(1, VERSE_KIT, fill=True)
put(VOX, 0, N("A4"), I_HOOVER)
for k in range(1, 4):
    grid[VOX][k] = None                          # let the Hoover ring for the first 4 rows
finish("INT2")


def tune_pat(name, k, chorus):
    """Quarter k (0-3) of the stretched tune. Verse: lead an octave down, light kit, pulse bass.
    Chorus: lead up, busy kit, octave bass, Hoover hits on each synthwave bar."""
    new_pattern()
    melody(LEAD, part(SLOW, 32 * k, 32 * (k + 1)), shift=0 if chorus else -12)
    prog = PROG[4 * k: 4 * (k + 1)]
    for u, c in enumerate(prog):
        arp(u, c)
        bass(u, c, "octave" if chorus else "pulse")
    for swb in (0, 1):
        drums_bar(swb, CHORUS_KIT if chorus else VERSE_KIT, crash=(chorus and swb == 0 and k in (0, 2)),
                  fill=(swb == 1 and k == 3))
        if chorus:
            u = 2 * swb
            put(VOX, u * UNIT, hoover_note(prog[u]), I_HOOVER)
            for r in range(1, 4):
                grid[VOX][u * UNIT + r] = None
    finish(name)


for k in range(4):
    tune_pat("V%d" % (k + 1), k, chorus=False)
    tune_pat("C%d" % (k + 1), k, chorus=True)

# ---- HK: the hook (= C2's melody) with the Hoover answering each "ciao" instead of the arpeggio
new_pattern()
melody(LEAD, part(SLOW, 32, 64))
prog = PROG[4:8]
for u, c in enumerate(prog):
    bass(u, c, "gallop")
    arp(u, c, rows=range(0, 4))                          # half the arpeggio ...
    put(VOX, u * UNIT + 4, hoover_note(c), I_HOOVER)     # ... and a Hoover answer
    off(VOX, u * UNIT + 7)
drums_bar(0, CHORUS_KIT, crash=True)
drums_bar(1, CHORUS_KIT)
finish("HK")

# ---- BR1 BR2: breakdown - no drums. The arpeggio and the first half of the tune, lead low, bass held
for j in (0, 1):
    new_pattern()
    melody(LEAD, part(SLOW, 32 * j, 32 * (j + 1)), shift=-12)
    for u, c in enumerate(PROG[4 * j: 4 * (j + 1)]):
        arp(u, c)
        bass(u, c, "hold")
    if j == 1:                                           # the kick creeps back in
        for r in range(0, ROWS_PER_PATTERN, 8):
            hit(DRUMS, r, "kick")
    finish("BR%d" % (j + 1))

# ---- BU1 BU2: build - snare on every beat, then every 8th, then every 16th; toms at the very end;
#      the bass pulses on E, the arpeggio keeps running; a beat of silence before the chorus
for j in (0, 1):
    new_pattern()
    for u in range(4):
        c = "Am" if (j == 0 and u < 2) else ("Dm" if j == 0 else "E7")
        arp(u, c)
        bass(u, c, "pulse", last=(6 if (j == 1 and u == 3) else UNIT))
    for r in range(ROWS_PER_PATTERN):
        step = (4 if r < 16 else 2) if j == 0 else (1 if r < 24 else None)
        if step and r % step == 0:
            hit(DRUMS, r, "kick" if r % 8 == 0 else "snare")
    if j == 1:
        for k, what in enumerate(("hi", "hi", "lo", "lo", "crash", None)):
            hit(DRUMS, 24 + k, what)
        for ch in range(CHANNELS):                       # the last beat (rows 30-31) is silent
            off(ch, 30)
            grid[ch][31] = None
    finish("BU%d" % (j + 1))

# ---- OUT: the arpeggio thins out over a last held A, the kick on the first beat only
new_pattern()
melody(LEAD, [(0, 24, "A5")])
for u in range(4):
    arp(u, "Am", rows=range(0, 8 - 2 * u))
    bass(u, "Am", "hold")
hit(DRUMS, 0, "crash")
hit(DRUMS, 16, "kick")
finish("OUT")

# ================================================================ the song: 64 slots
PATTERN_NAMES = ["INT1", "INT2", "V1", "V2", "V3", "V4", "C1", "C2", "C3", "C4",
                 "HK", "BR1", "BR2", "BU1", "BU2", "OUT"]
VERSE_P, CHORUS, CHORUS_HK = ["V1", "V2", "V3", "V4"], ["C1", "C2", "C3", "C4"], ["C1", "HK", "C3", "C4"]
BREAK, BUILD = ["BR1", "BR2"], ["BU1", "BU2"]
ORDER = (["INT1", "INT2"] + VERSE_P + CHORUS                 #  0-9
         + BREAK + BUILD + CHORUS_HK + CHORUS_HK            # 10-21
         + ["INT2"] + VERSE_P + BUILD + CHORUS              # 22-32
         + BREAK + CHORUS_HK                                # 33-38
         + ["INT2"] + VERSE_P + BUILD + CHORUS + CHORUS_HK  # 39-53
         + BREAK + BUILD + CHORUS_HK                        # 54-61
         + ["INT1", "OUT"])                                 # 62-63
assert len(PATTERNS) == len(PATTERN_NAMES) == 16 and set(PATTERNS) == set(PATTERN_NAMES)
assert len(ORDER) == 64, len(ORDER)
assert set(ORDER) == set(PATTERN_NAMES)
ORDER_IDX = [PATTERN_NAMES.index(n) for n in ORDER]

# ------------------------------------------------------------------ write the file
def build_xm():
    n_pat = len(PATTERN_NAMES)
    out = bytearray()
    out += b"Extended Module: "
    out += b"Bella Ciao Synthwave".ljust(20, b"\0")
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
