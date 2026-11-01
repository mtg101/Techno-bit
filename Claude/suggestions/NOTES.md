# Techno:bit notes

A running record of what we have decided and what is left to do. Claude keeps this file in `Claude/suggestions`;
anything worth keeping can be copied into the `Claude` record folder.

Last updated: 1 November 2026.

---

## Ground rules

- Claude **reads** the whole project. The `Claude` folder is the record of what has been agreed and is
  read-only for Claude, with two exceptions where Claude may write:
  - **`Claude/suggestions`**: suggested code, docs and notes. Code here is a suggestion for the teacher to
    read, understand and rebuild in Blocks, not a finished drop-in.
  - **`Claude/mods`**: music files (`.xm` tunes). The tunes are content, not code, so Claude can create them
    directly; generator scripts for them go in `suggestions`.
  Everywhere else is read-only for Claude. Git is the safety net.
- **Go slowly.** One small step at a time, explained well enough to repeat to the coding club. No big code
  drops without a go-ahead.
- All Python must be **block compatible**: paste into MakeCode, flip to Blocks, and it should render as real
  blocks, with no grey `<python code>` blocks hiding logic. Avoid Python string methods such as `.split()`,
  `.find()`, `.strip()`: MakeCode turns them into hidden helpers with no block. Use the text blocks instead:
  `substr`, `index_of`, `char_at`, `includes`.
- The **MakeCode project is the source of truth for the block layout**. `main.py` in GitHub is a copy for
  version control; when MakeCode exports Python it writes functions in its own (layout) order.

---

## Decisions

### The tracker format (see `Claude/microbit_tracker_format_students.md`)
- Cells: `tone D-6` (pitched note), `wave kick` (sound), `x` (silence), `-` (rest: carry on, do nothing).
- Note names are 3 characters: letter, `-` or `#`, octave (`C-4`, `C#4`). Sharps only. A name is looked up in
  `note_names` and the Hz value read from the same position in `note_hz`. 36 notes, C-4 to B-6; a name outside
  that range is not found and plays nothing.
- Because every tone cell has the same layout (`tone D-6`: positions 0-3 `tone`, 4 a space, 5-7 the note name),
  `play_note` reads it with **substring** blocks: `substr(0, 4)` is the kind, `substr(5, 3)` is the note name.
- 12 wave names: kick, snare, clap, hat, openhat, crash, tom_lo, tom_hi, pew_lo, pew_hi, hoover_e, hoover_a.
- One row = an eighth note = 200 ms (150 BPM). A pattern = 32 rows = 4 bars.
- One array entry per cell, one array per pattern, plus an order list. No volume, no effects.

### The tune and the boards
- Tune: `Claude/mods/korobeiniki_techno_4ch_microbit.xm` (4 channels, 16 patterns, 64-slot order list, 10 instruments).

### Song 2: Canon in D, bhangra techno
- Tune: `Claude/mods/canon_bhangra_4ch_microbit.xm`; generator `Claude/suggestions/make_canon_xm_microbit.py`.
- Why Pachelbel: the Knight Rider theme is under copyright (other people's versions don't change that), so the
  second tune had to be public domain. Pachelbel's *Canon and Gigue in D* (about 1700) suits 4-bar techno: an
  8-chord loop over an 8-note ground bass.
- Same setup and the **same 10 instruments, byte for byte**, so the code, LEDs and converter work for both songs.
- The 8 chords (D A Bm F#m G D G A) are stretched to 2 per bar: one pass of the ground bass = one pattern.
  Bass lifted to D5-D4 so it keeps its shape above the speaker's floor.
- Lead lines V1-V3 are Pachelbel's violin lines; V4 is new. In the canon patterns (V2-V4) track 3 plays the
  line track 1 played one pattern earlier: a real canon across two micro:bits.
- Bhangra: dhol groove on the toms (low tom = deep head, high tom = sharp head) with claps on beats 2 and 4,
  over a four-on-the-floor kick. Hoover stabs: A-4, except E-4 over the A chord.
- Patterns: INT1 INT2 V1 V2 V3 V4 D1 D2 D1x D2x BR1 BR2 BU1 BU2 RLD OUT (letters A-P in the same order).
- Tracks follow the XM channels: **1 lead** (melody), **2 acid** (bass), **3 vox** (voice lane: tone phrases plus
  claps, crashes, toms, pews, Hoover stabs), **4 drums** (kick and hats). **0 = conductor** (metronome + radio).
- Everything on the display is one character: tracks `0`-`4`, patterns `A`-`P` (Korobeiniki) and `a`-`p`
  (Canon), songs `*` (Korobeiniki) and `+` (Canon).
- Two songs, one per tune, each 64 patterns (about 6 min 50 s). The earlier test song was dropped: single
  patterns can be tested from the pattern screen.
- In the code each track has 32 patterns: Korobeiniki's 16 (`lead_int1` ...) then the Canon's 16
  (`canon_lead_int1` ...). The Canon's order list points at patterns 16-31. File: `Claude/suggestions/main_two_songs.py`.
- Sounds: one function per sound (`play_kick` ...), recipes from `Claude/code/microbit_instruments.py`.
- LEDs: one LED at a time. Waves on rows 1-2, related sounds share an LED; the low/open one is at
  `bright_dim` = 128 (half), the other at 255. Tones on rows 4, 3, 2 by note (not octave).

### Radio sync: "a message always interrupts" (in `main.py` since 1 Nov)
- The conductor broadcasts every pattern number; that is the point of the demo.
- History: the conductor waited 50 ms after each pattern so boards had finished before the next number arrived
  (a board ignored numbers while playing). That left a 50 ms hitch every pattern. 10 ms sometimes failed:
  in a 5-board simulation about 1 in 3 patterns were missed, matching what was heard on the real boards.
- Now: a pattern number is **always accepted** and **interrupts** whatever is playing (`new_pattern`). The
  conductor sends with **no wait**. During a radio song a board waits for the next number in a fast loop
  (`pause 1`), not in `forever` (which only runs every 20 ms). "end song" is sent **after** the last number.
- Simulated result: no missed patterns, no gap, boards 1-5 ms behind the conductor. Confirmed on the real
  boards: "keeps things running nicely without the wait".

---

## Known limits

- **First pattern** of a song can start up to ~20 ms late on some boards (they are idle in `forever` when it
  starts). Only the opening beat; fix later if it is audible.
- **Conductor switched off mid-song**: the other boards keep waiting for a number. Resetting them fixes it.
- **Block layout** can't be set from Python. Paste, then right-click > Collapse Blocks, then Format Code (F),
  then save/share from MakeCode so students open the arranged project.
- **Big file**: about 2,000 array entries; MakeCode may be slow converting it to Blocks.

---

## To do

- [ ] **Song 2 in MakeCode**: try `main_two_songs.py` (about 4,100 array entries, so Blocks may be slow; if it
      struggles, share identical patterns). Check the lowercase `a`-`p` are easy to read on the display.

- [ ] **XM converter** and a **template XM** (4 channels, 32 rows, 10 instruments, speed 12 / tempo 150, no
      volume or effects) so a new tune goes from OpenMPT to MakeCode without hand copying. Design first,
      in small steps.
- [ ] **README**: updated draft in `Claude/suggestions/README.md` (two tunes, 32 patterns, song names,
      Pachelbel spelling, AI use). Still to decide: the VS Code section and the converter sentence (see below).
- [ ] **Format doc**: updated student version in `Claude/suggestions/microbit_tracker_format_students.md`
      (both tunes, pattern tables A-P and a-p, substring version, radio timing). Copy it over
      `Claude/microbit_tracker_format_students.md`, which is still the first version.
- [ ] **README, VS Code section**: `main.py` is MakeCode Python (`basic.`, `music.create_sound_expression`,
      `radio.on_received_string`), not MicroPython, so adding `from microbit import *` and using "Put this
      file" won't run it. Loading `microbit-Technobit.hex` onto the MICROBIT drive would.
- [ ] **README, AI use**: "Claude Code has been used to create the .XM file conversion app" - the converter
      hasn't been written yet.
- [ ] **The .hex file** `microbit-Technobit.hex` was built before the Canon was added; download a fresh one
      from MakeCode before checking in.
- [ ] **Sounds and balance** on the real speakers: note any sound that is too quiet, too loud or wrong.
      The acid bass (around 440 Hz) is likely to be the quietest part.
- [ ] **First-beat lateness**: only if it can be heard.
- [ ] **Tidy `Claude/suggestions`**: `main_agreed_format.py`, `main_agreed_instruments.py`, `main_korobeiniki.py`
      and `main_interrupt.py` are stepping stones; `main_substring.py` = current `main.py`.

---

## Done

- Tracker format documented, with a student version and a short "what is a tracker" intro.
- Existing code converted to the format: XM note names, name/Hz lookup tables, 12 agreed sounds, shared LEDs.
- The tune hardcoded from the XM (64 pattern arrays checked cell by cell against the XM).
- Single-character display, XM track order.
- Radio sync without the wait (message always interrupts). Working on the real boards.
- `play_note` uses substring blocks instead of Python's `split` (adopted in `main.py`, 1 Nov).
- Song 2 XM (Canon in D, bhangra techno) generated, checked and listened to in OpenMPT.
- Song 2 added to the code as song `+` (`main_two_songs.py`): all 64 Canon arrays match the XM; both songs
  checked on the mock micro:bit.
- Demo video shrunk from 87 MB to 9 MB (720p MP4) and shown in the README on GitHub; the 87 MB original removed.

---

## Checked in the MakeCode source

From `microsoft/pxt-microbit` and `microsoft/pxt` on GitHub, in case the questions come up again:
- `basic.forever` sleeps 20 ms between runs.
- `plot x y brightness` exists (Advanced > LED), brightness 0-255.
- Sound expressions: frequency 0-5000, volume 0-255, duration 1-9999 ms.
- Python's `str.split()` becomes the hidden helper `_py.py_string_split` (no block); `"abc".substr(2, 2)`
  becomes the "substring of ... from ... of length ..." block (`pxt/libs/pxt-python`, `pxt/tests/decompile-test`).
- Pasted Python is laid out by "Format Code": on start first, then events, then functions in file order,
  flowed left to right in rows. The workspace menu has Format Code, Collapse Blocks, Expand Blocks.
