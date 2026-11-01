"""
ODE TO JOY - three arrangements of the same tune, for 4 micro:bits. Same setup and the same 10 instruments
as the other tunes. Beethoven's Symphony No. 9 (1824) is in the public domain.

  python3 make_ode_to_joy_xm_microbit.py trance      -> euphoric trance: four on the floor, offbeat open hats,
                                                        rolling offbeat bass, running arpeggio, Hoover stabs
  python3 make_ode_to_joy_xm_microbit.py minor       -> dark techno: the tune in A MINOR, closed hats, acid bass,
                                                        claps / ghost snares / Hoover stabs on track 3
  python3 make_ode_to_joy_xm_microbit.py synthwave   -> half-time drums, 16th-note bass, arpeggio in the verses;
                                                        DRUM HEAVY, SYNCOPATED: the melody re-rhythmed (same
                                                        notes), a 3+3+2 kick, the bass locked to it, track 3 a
                                                        second kit in the drops (offbeat claps and toms)

The melody, chords, the 16 patterns and the 64-slot order are the same in all three: only the arrangement
changes. A good one to show students - same tune, three styles.

The tune is in A (major, or minor for "minor") so the Hoover's two pitches are the key note (A) and the fifth (E).
Four 4-bar phrases (A, A', B, A'), quarter note = 2 rows, so one phrase = one pattern. Written from memory
(not checked against a score). Lead E5-E6. Chords per half bar: phrase A: A A E E A A E E, A': A A E E A A E A,
B: E E A A E E A E.

Setup (unchanged): 4 channels, 32 rows per pattern, speed 12 / tempo 150, 16 patterns, a 64-slot order list,
no volume column, no effects, 10 instruments. Pitched parts C-4 to B-6; lead and voice no lower than E-4.

Patterns: INT1 INT2 P1 P2 P3 P4 D1 D2 D3 D4 D3x BR1 BR2 BU1 BU2 OUT
  P1-P4 = the four phrases, first time (lighter); D1-D4 = the four phrases as the drop; D3x = a variant of D3.
"""
import math
import random
import struct
import sys

STYLE = sys.argv[1] if len(sys.argv) > 1 else "trance"
assert STYLE in ("trance", "minor", "synthwave"), STYLE
OUT = sys.argv[2] if len(sys.argv) > 2 else "ode_to_joy_%s_4ch_microbit.xm" % STYLE
TITLE = {"trance": "Ode to Joy Trance", "minor": "Ode to Joy Dark", "synthwave": "Ode to Joy Synthwave"}[STYLE]

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

# ================================================================ ODE TO JOY
MINOR = STYLE == "minor"
HALF = ROWS_PER_BAR // 2
VOICE_FLOOR = N("E4")

# the four phrases (note, rows): quarter = 2 rows, 32 rows = 4 bars
PH_A = [("C#6", 2), ("C#6", 2), ("D6", 2), ("E6", 2), ("E6", 2), ("D6", 2), ("C#6", 2), ("B5", 2),
        ("A5", 2), ("A5", 2), ("B5", 2), ("C#6", 2), ("C#6", 3), ("B5", 1), ("B5", 4)]
PH_A2 = PH_A[:12] + [("B5", 3), ("A5", 1), ("A5", 4)]
PH_B = [("B5", 2), ("B5", 2), ("C#6", 2), ("A5", 2), ("B5", 2), ("C#6", 1), ("D6", 1), ("C#6", 2), ("A5", 2),
        ("B5", 2), ("C#6", 1), ("D6", 1), ("C#6", 2), ("B5", 2), ("A5", 2), ("B5", 2), ("E5", 4)]
PHRASES = [PH_A, PH_A2, PH_B, PH_A2]

# SYNTHWAVE re-rhythms the tune (same notes, same order) so it stops sounding like a recorder recital:
#   "long, long, short-short" (3+3+1+1) and "da, da-da, long, da" (2+1+3+2), with phrase B anticipating the beat
SY_A = [("C#6", 3), ("C#6", 3), ("D6", 1), ("E6", 1), ("E6", 2), ("D6", 1), ("C#6", 3), ("B5", 2),
        ("A5", 3), ("A5", 3), ("B5", 1), ("C#6", 1), ("C#6", 3), ("B5", 1), ("B5", 4)]
SY_A2 = SY_A[:12] + [("B5", 3), ("A5", 1), ("A5", 4)]
SY_B = [("B5", 3), ("B5", 3), ("C#6", 1), ("A5", 1), ("B5", 2), ("C#6", 1), ("D6", 1), ("C#6", 3), ("A5", 1),
        ("B5", 2), ("C#6", 1), ("D6", 1), ("C#6", 3), ("B5", 1), ("A5", 2), ("B5", 1), ("E5", 5)]
if STYLE == "synthwave":
    for orig, new in ((PH_A, SY_A), (PH_A2, SY_A2), (PH_B, SY_B)):
        assert [n for n, _ in orig] == [n for n, _ in new]          # the tune's notes are unchanged
    PHRASES = [SY_A, SY_A2, SY_B, SY_A2]
PROGS = [["A", "A", "E", "E", "A", "A", "E", "E"],
         ["A", "A", "E", "E", "A", "A", "E", "A"],
         ["E", "E", "A", "A", "E", "E", "A", "E"],
         ["A", "A", "E", "E", "A", "A", "E", "A"]]
for ph in PHRASES:
    assert sum(l for _, l in ph) == ROWS_PER_PATTERN


def key(name):
    """The minor version: C# becomes C (A major -> A minor). Nothing else in the tune changes."""
    return name.replace("C#", "C") if MINOR else name


def chord(name):
    return "Am" if (MINOR and name == "A") else name


CHORDS = {"A": ("A", [0, 4, 7]), "Am": ("A", [0, 3, 7]), "E": ("E", [0, 4, 7])}
ROOT = {"A": N("A4"), "Am": N("A4"), "E": N("E4")}


def chord_tones(name):
    root, iv = CHORDS[name]
    base = N(root + "4")
    while base < VOICE_FLOOR:
        base += 12
    return [base + i for i in iv]


def hoover_note(c):
    return N("E4") if c == "E" else N("A4")


def melody(ch, phrase, shift=0, inst=None):
    r = 0
    for name, ln in phrase:
        put(ch, r, N(key(name)) + shift, inst or I_SQ)
        if ln >= 4:
            off(ch, r + ln - 1)
        r += ln


SOUND = {"lo": (N("C4"), I_TOM), "hi": (N("G4"), I_TOM), "clap": (C4, I_CLAP), "hat": (C4, I_HAT),
         "ohat": (C4, I_OHAT), "crash": (C4, I_CRASH), "kick": (C4, I_KICK), "snare": (C4, I_SNARE)}


def hit(ch, row, what):
    if what:
        note, inst = SOUND[what]
        put(ch, row, note, inst)


# ---------------- ACID (bass): one chord per half bar (4 rows)
BASS = {
    "hold":    [(0, 0), None, None, "off"],
    "beat":    [(0, 0), "off", (0, 0), "off"],
    "offbeat": ["off", (0, 0), "off", (0, 0)],         # trance: bass on the "and"
    "rolling": ["off", (0, 0), (0, 0), (0, 0)],        # trance drop: rolls in after each kick
    "acid":    [(0, 0), (0, 1), (7, 0), (0, 1)],       # techno: root, octave, fifth, octave
    "pulse":   [(0, 0), (0, 0), (0, 0), (0, 0)],       # synthwave: steady 16ths
    "octave":  [(0, 0), (0, 0), (0, 1), (0, 0)],
    "pump":    [(0, 0), (0, 1), (0, 0), (0, 1)],
}


def bass_line(prog, style, last_pos_rows=None):
    for pos, c in enumerate(prog):
        c = chord(c)
        steps = BASS[style] if (last_pos_rows is None or pos < 7) else BASS[style][:last_pos_rows]
        for k, step in enumerate(steps):
            r = pos * HALF + k
            if step is None:
                continue
            if step == "off":
                off(ACID, r)
            else:
                semis, octv = step
                put(ACID, r, ROOT[c] + semis + 12 * octv, I_ACID)


# ---------------- VOX: arpeggio (one note per row, 2 octaves up and down) or the techno percussion lane
ARP_SHAPE = [0, 1, 2, 3, 4, 5, 4, 3]


def arp(prog, rows=range(ROWS_PER_PATTERN)):
    for r in rows:
        t = chord_tones(chord(prog[r // HALF]))
        ladder = t + [x + 12 for x in t]
        put(VOX, r, ladder[ARP_SHAPE[r % 8]], I_P12)


def perc_bar(bar, prog, crash=False, ghost=False):
    hit(VOX, R(bar, 0), "crash" if crash else "hat")
    hit(VOX, R(bar, 2), "clap")
    put(VOX, R(bar, 3), hoover_note(prog[2 * bar]), I_HOOVER)
    if ghost:
        hit(VOX, R(bar, 1), "snare")
        hit(VOX, R(bar, 5), "snare")
    hit(VOX, R(bar, 4), "hat")
    hit(VOX, R(bar, 6), "clap")
    put(VOX, R(bar, 7), hoover_note(prog[2 * bar + 1]), I_HOOVER)


# ---------------- DRUMS
def four_floor(bar, hat, last=ROWS_PER_BAR):
    for r in range(min(ROWS_PER_BAR, last)):
        hit(DRUMS, R(bar, r), "kick" if r % 2 == 0 else hat)


HALFTIME_LIGHT = ["kick", None, "hat", None, "snare", None, "hat", None]        # one 8-row bar, felt half speed
HALFTIME_BUSY = ["kick", "hat", "hat", "hat", "snare", "hat", "kick", "hat"]


def halftime(bar, kit):
    for r in range(ROWS_PER_BAR):
        hit(DRUMS, R(bar, r), kit[r])


# synthwave drop, two drum lanes. One 8-row bar (felt as half a bar at 75 BPM); bars alternate A, B.
# kick in a 3+3+2 pattern (rows 0, 3, 6), the big snare on the half-time backbeat (row 4), open hats on offbeats
SW_DRUMS = [["kick", "hat", "ohat", "kick", "snare", "hat", "kick", "hat"],
            ["kick", "hat", "hat", "kick", "snare", "kick", "hat", "ohat"]]
# track 3: a clap on the snare and another just before the next downbeat, toms off the beat
SW_VOX = [[None, None, "hi", None, "clap", "lo", None, "clap"],
          [None, "lo", None, "hi", "clap", None, "lo", "clap"]]
SW_VOX_BUSY = [["hat", "lo", "hi", "lo", "clap", "lo", "hi", "clap"],      # the variant drop: busier toms
               ["hat", "hi", "lo", "hi", "clap", "hi", "lo", "clap"]]
SW_VERSE = [["kick", None, "hat", "kick", "snare", None, "hat", None],      # verses: the same syncopation, lighter
            ["kick", None, "hat", None, "snare", "kick", "hat", "ohat"]]


def sync_bass(prog, drop):
    """Bass locked to the 3+3+2 kick: root on rows 0 and 3 (first chord of the bar), then the second chord's
    root an octave up on row 6 (and back down on 7 in the drop)."""
    for b in range(4):
        c1, c2 = chord(prog[2 * b]), chord(prog[2 * b + 1])
        put(ACID, R(b, 0), ROOT[c1], I_ACID); off(ACID, R(b, 2))
        put(ACID, R(b, 3), ROOT[c1], I_ACID); off(ACID, R(b, 5))
        put(ACID, R(b, 6), ROOT[c2] + 12, I_ACID)
        if drop:
            put(ACID, R(b, 7), ROOT[c2], I_ACID)
        else:
            off(ACID, R(b, 7))


GATE = (0, 1, 3, 4, 6)                     # the verse arpeggio only plays on these rows of each bar


def synth_heavy(bar, variant=False, last=ROWS_PER_BAR):
    vox = SW_VOX_BUSY if variant else SW_VOX
    for r in range(min(ROWS_PER_BAR, last)):
        hit(DRUMS, R(bar, r), SW_DRUMS[bar % 2][r])
        hit(VOX, R(bar, r), vox[bar % 2][r])


def tom_cascade(bar):
    """The end of the tune: both lanes tumble down the toms into the next section."""
    for k, (d, v) in enumerate((("snare", "hi"), ("hi", "hi"), ("lo", "lo"), ("kick", "crash"))):
        hit(DRUMS, R(bar, 4 + k), d)
        hit(VOX, R(bar, 4 + k), v)


def fill(bar):
    """The last half bar of a section: snare, snare, high tom, low tom."""
    for k, what in enumerate(("snare", "snare", "hi", "lo")):
        hit(DRUMS, R(bar, 4 + k), what)


def roll(bar, level, last=ROWS_PER_BAR):
    for r in range(min(ROWS_PER_BAR, last)):
        if level == 1:
            what = "snare" if r in (2, 6) else ("kick" if r in (0, 4) else None)
        elif level == 2:
            what = "kick" if r % 4 == 0 else ("snare" if r % 2 == 0 else None)
        elif level == 3:
            what = "kick" if r % 2 == 0 else "snare"
        else:
            what = "kick" if r == 0 else "snare"
        hit(DRUMS, R(bar, r), what)


def finish(name):
    finish_pattern(name)


# ================================================================ the 16 patterns
INTRO_PROG = ["A"] * 6 + ["E", "E"]

# ---- INT1
new_pattern()
if STYLE == "trance":
    arp(INTRO_PROG)
    bass_line(INTRO_PROG[:8], "offbeat")
    for r in range(16):                                   # the bass waits for bar 3
        grid[ACID][r] = None
elif STYLE == "minor":
    for b in range(4):
        four_floor(b, "hat")
    bass_line(INTRO_PROG, "beat")
else:
    arp(INTRO_PROG, rows=[r for r in range(ROWS_PER_PATTERN) if r % 8 in GATE])
    sync_bass(INTRO_PROG, drop=False)
    for r in range(16):
        grid[ACID][r] = None
finish("INT1")

# ---- INT2
new_pattern()
if STYLE == "trance":
    arp(INTRO_PROG)
    bass_line(INTRO_PROG, "offbeat")
    for b in range(4):
        hit(DRUMS, R(b, 0), "kick"); hit(DRUMS, R(b, 4), "kick")
    fill(3)
elif STYLE == "minor":
    for b in range(4):
        four_floor(b, "hat")
        perc_bar(b, INTRO_PROG, crash=(b == 0))
    bass_line(INTRO_PROG, "acid")
else:
    arp(INTRO_PROG, rows=[r for r in range(ROWS_PER_PATTERN) if r % 8 in GATE])
    sync_bass(INTRO_PROG, drop=False)
    for b in range(4):
        halftime(b, SW_VERSE[b % 2])
    fill(3)
finish("INT2")


# ---- P1-P4 (first time) and D1-D4 (the drop)
def phrase_pat(name, k, drop, variant=False):
    new_pattern()
    prog = PROGS[k]
    melody(LEAD, PHRASES[k])
    end = (k == 3)                                         # fill at the end of the 16 bars
    if STYLE == "trance":
        arp(prog)
        for b in range(4):
            if drop:
                four_floor(b, "ohat", last=(4 if end and b == 3 else ROWS_PER_BAR))
                put(VOX, R(b, 0), hoover_note(prog[2 * b]), I_HOOVER)        # supersaw-style stab on each bar
                if variant:
                    put(VOX, R(b, 4), hoover_note(prog[2 * b + 1]), I_HOOVER)
            else:
                hit(DRUMS, R(b, 0), "kick"); hit(DRUMS, R(b, 4), "kick")
                hit(DRUMS, R(b, 2), "hat"); hit(DRUMS, R(b, 6), "hat")
        if drop:
            hit(DRUMS, 0, "crash")
        bass_line(prog, "rolling" if drop else "offbeat")
    elif STYLE == "minor":
        for b in range(4):
            four_floor(b, "hat" if not drop or variant else "ohat", last=(4 if end and b == 3 else ROWS_PER_BAR))
            if drop:
                perc_bar(b, prog, crash=(b == 0), ghost=variant or b % 2 == 1)
            else:
                hit(VOX, R(b, 2), "clap"); hit(VOX, R(b, 6), "clap")
        bass_line(prog, "acid" if drop else "beat")
    else:
        if drop:                                           # drum heavy: track 3 is a second kit
            for b in range(4):
                synth_heavy(b, variant, last=(4 if end and b == 3 else ROWS_PER_BAR))
            hit(VOX, 0, "crash")
        else:
            arp(prog, rows=[r for r in range(ROWS_PER_PATTERN) if r % 8 in GATE])
            for b in range(4):
                halftime(b, SW_VERSE[b % 2])
        sync_bass(prog, drop)
    if end and STYLE == "synthwave" and drop:
        tom_cascade(3)
    elif end:
        fill(3)
    finish(name)


for k in range(4):
    phrase_pat("P%d" % (k + 1), k, drop=False)
    phrase_pat("D%d" % (k + 1), k, drop=True)
phrase_pat("D3x", 2, drop=True, variant=True)


# ---- BR1 BR2: breakdown - no drums, phrases A and A' over held bass
for j in (0, 1):
    new_pattern()
    prog = PROGS[j]
    melody(LEAD, PHRASES[j])
    if STYLE == "minor":
        for b in range(4):
            put(VOX, R(b, 0), hoover_note(prog[2 * b]), I_HOOVER)
            off(VOX, R(b, 7))
    else:
        arp(prog)
    bass_line(prog, "hold")
    if j == 1 and STYLE != "minor":
        for b in range(4):
            hit(DRUMS, R(b, 0), "kick")
    finish("BR%d" % (j + 1))

# ---- BU1 BU2: the build - the roll speeds up, the lead stutters up the A chord, the bass pumps on E,
#      then a beat of silence
CLIMB = ["E5", "E5", "A5", "A5", "C#6", "C#6", "E6", "E6"]
STEP = (2, 2, 2, 2, 1, 1, 1, 1)
for k in range(2):
    new_pattern()
    prog = (["A"] * 8) if k == 0 else (["E"] * 8)
    for b in range(4):
        i = 4 * k + b
        roll(b, (1, 1, 2, 2, 3, 3, 4, 4)[i], last=(6 if i == 7 else ROWS_PER_BAR))
    for rr in range(ROWS_PER_PATTERN):
        g = k * ROWS_PER_PATTERN + rr
        bi = g // ROWS_PER_BAR
        if (g % ROWS_PER_BAR) % STEP[bi] == 0:
            put(LEAD, rr, N(key(CLIMB[bi])), I_SQ)
    if STYLE == "minor":
        zap = [rr for rr in range(ROWS_PER_PATTERN) if rr % (4 if k == 0 else 2) == 1]
        for n_, rr in enumerate(zap):
            put(VOX, rr, N("C4") if k == 0 else N("C5"), I_ZAP)
    else:
        arp(prog)
    bass_line(prog, "beat" if k == 0 else "pump", last_pos_rows=(2 if k == 1 else None))
    if k == 1:
        for ch in range(CHANNELS):                         # the last beat (rows 30-31) is silent
            off(ch, 30)
            grid[ch][31] = None
    finish("BU%d" % (k + 1))

# ---- OUT: the last phrase's final notes and a held A, the beat falls away
new_pattern()
melody(LEAD, [("A5", 16)])
prog = ["A"] * 8
if STYLE == "minor":
    put(VOX, 0, hoover_note("A"), I_HOOVER); off(VOX, 15)
else:
    arp(prog, rows=range(0, 24))
bass_line(prog[:4], "hold")
hit(DRUMS, 0, "crash")
hit(DRUMS, 8, "kick")
hit(DRUMS, 16, "kick")
finish("OUT")

# ================================================================ the song: 64 slots (the same for all three styles)
PATTERN_NAMES = ["INT1", "INT2", "P1", "P2", "P3", "P4", "D1", "D2", "D3", "D4", "D3x",
                 "BR1", "BR2", "BU1", "BU2", "OUT"]
TUNE, DROP, DROPX, BREAK, BUILD = ["P1", "P2", "P3", "P4"], ["D1", "D2", "D3", "D4"], ["D1", "D2", "D3x", "D4"], ["BR1", "BR2"], ["BU1", "BU2"]
ORDER = (["INT1", "INT2"] + TUNE                       #  0-5
         + BUILD + DROP                                #  6-11
         + BREAK + BUILD + DROPX                       # 12-19
         + ["INT2"] + TUNE                             # 20-24
         + BUILD + DROP + DROPX                        # 25-34
         + BREAK + ["P3", "P4"] + BUILD                # 35-40
         + DROP                                        # 41-44
         + BREAK + BUILD + DROPX + DROP                # 45-56
         + TUNE + ["INT2", "INT1", "OUT"])             # 57-63
assert len(PATTERNS) == len(PATTERN_NAMES) == 16 and set(PATTERNS) == set(PATTERN_NAMES)
assert len(ORDER) == 64, len(ORDER)
assert set(ORDER) == set(PATTERN_NAMES)
ORDER_IDX = [PATTERN_NAMES.index(n) for n in ORDER]

# ------------------------------------------------------------------ write the file
def build_xm():
    n_pat = len(PATTERN_NAMES)
    out = bytearray()
    out += b"Extended Module: "
    out += TITLE.encode("ascii")[:20].ljust(20, b"\0")
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
    print(f"wrote {OUT} ({STYLE}): {len(data)} bytes, {len(PATTERN_NAMES)} patterns, song length {len(ORDER_IDX)}, ~{secs:.0f}s")
