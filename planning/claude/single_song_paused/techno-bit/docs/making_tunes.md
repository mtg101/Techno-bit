# Techno:bit tunes: the rules, and the XM converter

This explains how a tune made in a tracker becomes a Techno:bit program: the rules the tune has to follow, what
the converter does, and how it all gets onto the micro:bits. It is the plan *before* the code: when the code
and this document disagree, fix one of them.

---

## 1. The idea in one picture

```
 tools/template.xm ──► OpenMPT (write the tune) ──► mods/my_tune.xm
                                                        │
 main.py (the base program: Tetris) ───────────────────►├──► tools/xm_to_makecode.py ──► mods/my_tune_main.py
                                                                                   │
                     new MakeCode project ◄── paste the Python, switch to Blocks ◄─┘
                              │
                     download the .hex as hex/my_tune.hex, flash every micro:bit (conductor + players)
```

- **One song per MakeCode project.** Every song is the same program with different arrays. To change song,
  flash the boards with that song's project.
- **The base program** (`main.py` in the project root) is the tracker code with one example song: Tetris
  (Korobeiniki, 8 tracks). Everything that *plays* music lives here, and only here.
- **The converter** takes the base program, removes its song and puts in the song from an `.xm` file. It
  never changes the tracker code, so a fix to the base reaches every song the next time it is converted.
- **The `.xm` file is the master copy of a song.** Editing the arrays in MakeCode is fine for experimenting,
  but those changes don't flow back: the next conversion starts again from the `.xm`.

### Two ways to make a tune

Nobody should need Python to make a tune.

1. **In MakeCode, no tools at all.** Open the base project (Tetris) and change the arrays in Blocks: notes
   (`tone E-5` -> `tone G-5`), sounds (`wave clap` on another row), or the order of patterns in `song`. Good
   for small changes and for learning how the arrays work.
2. **In a tracker, then the converter.** Write the tune in OpenMPT, then convert it. Better for whole new
   tunes. Anyone can run the converter: it's all in the GitHub project. For anyone who doesn't want to run
   Python, a converter web page is planned (section 7), and until then someone who can run it converts the
   `.xm` for them.

### Where things live

```
main.py                     the base program: the tracker code + Korobeiniki (Tetris)
mods/                       the tunes: each .xm is the master copy, with its converted program next to it
  korobeiniki.xm              (its program is the root main.py)
  canon.xm, canon_main.py
  ode_to_joy.xm, ode_to_joy_main.py
hex/                        ready to flash, named after the tune: korobeiniki.hex, canon.hex ...
tools/
  xm_to_makecode.py         the converter
  template.xm               the starting point for a new tune: copy it into mods/
docs/                       this document and the tracker format
media/                      the demo video
```

The converter writes its program next to the `.xm`, so converting `mods/my_tune.xm` gives `mods/my_tune_main.py`.
These paths are inside the `techno-bit/` folder. `planning/claude/suggestions/` mirrors the project: a draft is
at the same path there (for example `planning/claude/suggestions/techno-bit/mods/x.xm`) until it's copied over.

---

## 2. Making a tune: the rules

Start from a copy of **`tools/template.xm`** (to be made: step 2), saved in `mods/` under the tune's name. It already has the right speed, tempo, rows and the 10
instruments, so most of these rules are kept just by not changing its settings.

### 2.1 Speed and time

| Setting | Value | Why |
|---|---|---|
| Speed | **12** ticks per row | the micro:bits play one row every 200 ms |
| Tempo | **150** | at speed 12, tempo 150 = 200 ms per row = 150 beats per minute with 2 rows a beat |
| Rows per pattern | **32** (exactly) | one pattern = 4 bars of 8 rows = 6.4 seconds |

The micro:bits always play at this speed. A different speed or tempo in the `.xm` only changes how it sounds
in OpenMPT, so the converter warns about it. (Other tempos are a possible later addition.)

### 2.2 Channels = tracks

A tune has **4 or 8 channels**. Each channel becomes one track, played by one micro:bit:

| Channel | Track | Name in the code | Usually |
|---|---|---|---|
| 1 | 1 | `lead` | the melody |
| 2 | 2 | `acid` | the bass line |
| 3 | 3 | `vox` | voice lane: a second tune, chords, claps, Hoover stabs |
| 4 | 4 | `drums` | kick and hats |
| 5 | 5 | `bass2` | extra |
| 6 | 6 | `kit2` | extra |
| 7 | 7 | `perc` | extra |
| 8 | 8 | `hits` | extra |

- **Channels 1-4 must make the whole tune on their own.** Channels 5-8 are extras that only add (the
  Tetris extras are drums and bass). The converter can't check this: listen with channels 5-8 muted.
- With **4 channels**, tracks 5-8 play the same as tracks 1-4 (5 plays 1, 6 plays 2 ...), so 8 boards never
  sit idle.
- The names describe the *usual* job. A tune can put anything on any channel.
- Track 0 is the conductor: it plays a metronome and is not in the `.xm`.

### 2.3 The 10 instruments

Use only instruments 1-10, as set up in the template. The sound comes from the micro:bit's own recipes, not
from the samples in the `.xm` (those only make it sound similar in OpenMPT).

| Instrument | Sound | Which notes |
|---|---|---|
| 1 | tone (square wave) | any note from **C-4 to B-6** |
| 2 | kick | any note (it plays the same; use C-4) |
| 3 | snare | any note (use C-4) |
| 4 | clap | any note (use C-4) |
| 5 | hat | any note (use C-4) |
| 6 | open hat | any note (use C-4) |
| 7 | crash | any note (use C-4) |
| 8 | tom | **C-4 = low tom, G-4 = high tom** (nothing else) |
| 9 | pew zap | **C-4 = low pew, C-5 = high pew** (nothing else) |
| 10 | Hoover stab | **E-4 = on E, A-4 = on A** (nothing else) |

Why no notes below C-4: the micro:bit's speaker gives out almost nothing below about 250 Hz.

### 2.4 Cells

Every cell becomes one array entry:

| In OpenMPT | Becomes | Means |
|---|---|---|
| a note with instrument 1 | `tone D-6` | play this note; it keeps sounding until the next sound or `x` |
| a note with instruments 2-10 | `wave kick` etc. | play this sound once, to its end |
| note off (`==`) | `x` | silence |
| empty | `-` | carry on: nothing new happens |

Rules for cells:
- **Every note needs its instrument number**, and every instrument number needs a note. (OpenMPT lets a
  note re-use the channel's last instrument; we don't, because a board may join a song half way through and
  must know what every cell means on its own.)
- **No volume column and no effects.** The micro:bit can't play them. Any volume or effect is an error.
- **One sound at a time per channel** (that's how trackers work anyway).

### 2.5 Patterns and the order list

- Every pattern has **exactly 32 rows**.
- **Each pattern starts fresh.** At the end of every pattern the micro:bit stops all sound, so a note or
  crash still ringing at the end of a pattern is cut, and a held note does *not* carry on into the next
  pattern as it would in OpenMPT. If a note should carry on, start it again on row 0 of the next pattern.
- The **order list** is the song: the patterns in the order they play. Each entry is 6.4 seconds, so 64
  entries is about 6 minutes 50 seconds. The conductor sends each entry's pattern number by radio.
- Patterns are numbered from 0, as in OpenMPT. In the code they become `lead_00`, `lead_01` and so on.
- **Every pattern in the file goes into the program**, even if the order list never plays it, so delete
  unused patterns: they waste memory.
- Ignored: the song title, the restart position, panning, and all instrument settings (envelopes, samples).

### 2.6 Size

Every cell costs about 15-18 bytes of the micro:bit's flash (measured from real `.hex` files). The tracker code plus Tetris (8 tracks x 16
patterns) leaves room to spare, but not unlimited room:

| Channels | Patterns that fit (about) |
|---|---|
| 8 | 35 |
| 4 | 70 |

The converter estimates the size and warns when a tune may not fit. The real test is downloading the
`.hex` from MakeCode.

---

## 3. Running the converter

Run it from the `techno-bit` folder (where `main.py` is):

```
python tools/xm_to_makecode.py mods/my_tune.xm
python tools/xm_to_makecode.py mods/my_tune.xm --base main.py --out mods/my_tune_main.py
```

- **Needs:** Python 3 on the PC. Nothing else to install.
- **`--base`**: the base program, normally the root `main.py` (default).
- **`--out`**: where to write (default: the tune's name plus `_main.py`).
- The converter **never changes** the `.xm` or the base program.

**If the tune breaks a rule**, nothing is written and the converter lists the problems with their place in
the tune, for example:

```
my_tune.xm: 2 problem(s) to fix first:
  - pattern 3, row 12, channel 2: tone C-3 is out of range (C-4 to B-6)
  - pattern 5, row 0, channel 4: volume or effect used (the micro:bits have neither)
```

**Warnings** (the program is still written): speed/tempo not 12/150, a tune that may be too big, and the
other warnings in section 6.

**If all is well:**

```
wrote my_tune_main.py: 4 tracks, 12 patterns, song of 48 patterns (5.1 minutes)
```

---

## 4. Getting it onto the micro:bits

1. In MakeCode, start a **new project** and switch to **Python**.
2. Select everything, paste the converted program, and switch to **Blocks**. (It is big: give it a moment.)
3. Download the `.hex` and save it as `hex/<tune>.hex` (MakeCode calls it `microbit-<project name>.hex`).
4. Flash **every** board with it: the conductor and all the players. Boards running different songs can't
   play together.
5. On each board: A picks the track (1-8), the logo makes it the conductor (0). Press B on the conductor to
   play the song.

---

## 5. What the converter writes

The output is the base program with its song swapped. Only these parts change; everything else is
copied exactly:

| Part | What it is |
|---|---|
| `create_lead_patterns()` ... `create_hits_patterns()` | one function per track with its own channel, each making that track's pattern arrays (`lead_00` ...). With 4 channels, only the first four |
| `create_patterns()` | puts the arrays into a list per track (`patterns_lead` ...), and those into `song_tracks`, so `song_tracks[track][pattern]` is one pattern's array. With 4 channels, tracks 5-8's lists are tracks 1-4's arrays |
| `create_song()` | `song`, the order list |
| the declarations of those variables | |

The converter finds these parts **by name**, not by position, because MakeCode reorders the program when it
exports Python. The output keeps Windows line endings, like MakeCode.

---

## 6. Changes this document asks of the draft converter

The draft `xm_to_makecode.py` already does most of this. To match the document it still needs:

1. **Unused patterns:** warn about patterns the order list never plays (they cost memory).
2. **Notes carrying across patterns:** warn when a tone channel's row 0 is empty (`-`) in a pattern that
   follows one whose note was still sounding, because the micro:bit cuts it at the pattern end (section 2.5).
3. **Size:** estimate in bytes and say how much is over, instead of a fixed cell count.

---

## 7. Open questions

1. ~~Where do song programs live?~~ Decided 4 Nov: in `mods/` in the project root
   (see "Where things live").
2. ~~Who runs the converter?~~ Decided 4 Nov: **anyone** - it's all in the GitHub project. But nobody should be
   blocked from making a tune by Python, hence the two ways in section 1 and the web page below.
3. **A converter web page** (planned, after the Python converter works): drop an `.xm` in, copy the Python
   out, nothing to install. Same rules and checks as the Python script, and it could live in the same GitHub
   project (GitHub Pages).
4. **Other tempos, more instruments:** later. They need changes to the base program as well as the rules.
