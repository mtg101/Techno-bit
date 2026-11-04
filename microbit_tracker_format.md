# The micro:bit tracker format

## What is a tracker?

Back in the Middle Ages (the late 1980s) people wrote music for computers like the Amiga using programs called
**trackers**. Instead of a piano roll or sheet music, a tracker is a grid: each column is a **channel**, each row is
a tiny slice of time, and each cell says which note or sound to play. Our tune uses the same idea, so you can read
it like a spreadsheet of music.

Want to make your own tracks? Try **OpenMPT**, a free tracker for Windows (it also runs on other systems with a
little extra setup):

- [OpenMPT: download](https://openmpt.org/)
- [OpenMPT on Wikipedia](https://en.wikipedia.org/wiki/OpenMPT)
- [Trackers on Wikipedia](https://en.wikipedia.org/wiki/Tracker_(music_software))

The rest of this page describes the simple, cut-down version of a tracker that our micro:bits play.

A simple text format for one micro:bit's part of a tune. It is easy to read and easy to type into a MakeCode array.

---

## 1. The big picture

A tune is split into **channels**. Each micro:bit plays one channel, one sound at a time.

A channel is a list of **cells**. Each cell is one **row** of time and says what the micro:bit should do on that row.

| Word | Meaning |
|---|---|
| **Cell** | One entry in the list: `tone D-6`, `wave kick`, `x` or `-` |
| **Row** | One step of time. One row = one cell |
| **Channel** | One micro:bit's part (for example lead, bass, drums) |
| **Pattern** | A block of 32 rows (4 bars). A tune is built by playing patterns one after another |

---

## 2. The four kinds of cell

| Cell | What it means | What the micro:bit does |
|---|---|---|
| `tone D-6` | Play a pitched note | `music.ring_tone(tone_freq)` |
| `wave kick` | Play a drum or effect | `music.create_sound_expression(...)` |
| `x` | Silence | Stop making sound |
| `-` | Rest: nothing new happens this row | Do nothing |

- A cell is either one of the single symbols (`x`, `-`) or **two words**: the kind (`tone` or `wave`) then the value.
- There are **no effects** and (for now) **no volume levels**.

---

## 3. Time

- One row = one **eighth note**.
- The tempo is **150 BPM**, so one row lasts **200 ms**.
- A pattern is **32 rows** = **4 bars** (8 rows per bar, 2 rows per beat).

---

## 4. Notes: `tone` cells

### How note names are written

Every note name is exactly **three characters**: a letter, a middle character, and an octave number.

| Part | What it is | Examples |
|---|---|---|
| Letter | The note: C D E F G A B | `D` |
| Middle character | `-` for a plain (natural) note, `#` for a sharp | `-` or `#` |
| Octave | 4, 5 or 6 (higher number = higher pitch) | `5` |

So the plain notes are `C-4`, `D-4`, `E-4`, `F-4`, `G-4`, `A-4`, `B-4`, and the sharps (the black piano keys) are
`C#4`, `D#4`, `F#4`, `G#4`, `A#4`. The `-` is not a minus sign or a flat: it only fills the middle slot so every
name has three characters. The tracker uses sharps only, so you will see `D#4` and never `Eb4`.

In a cell the name follows the word `tone` and a space: `tone D-6`, `tone D#6`.

All 36 names, lowest to highest:

```
C-4 C#4 D-4 D#4 E-4 F-4 F#4 G-4 G#4 A-4 A#4 B-4
C-5 C#5 D-5 D#5 E-5 F-5 F#5 G-5 G#5 A-5 A#5 B-5
C-6 C#6 D-6 D#6 E-6 F-6 F#6 G-6 G#6 A-6 A#6 B-6
```

The tune uses three octaves, **C-4 to B-6** (36 notes). Frequencies in Hz, rounded to whole numbers:

| Note | Octave 4 | Octave 5 | Octave 6 |
|---|---|---|---|
| C | 262 | 523 | 1047 |
| C# | 277 | 554 | 1109 |
| D | 294 | 587 | 1175 |
| D# | 311 | 622 | 1245 |
| E | 330 | 659 | 1319 |
| F | 349 | 698 | 1397 |
| F# | 370 | 740 | 1480 |
| G | 392 | 784 | 1568 |
| G# | 415 | 831 | 1661 |
| A | 440 | 880 | 1760 |
| A# | 466 | 932 | 1865 |
| B | 494 | 988 | 1976 |

The formula behind the table: **Hz = 440 x 2^((n - 58) / 12)**, where *n* is the tracker's note number
(C-4 = 49, A-4 = 58). Every 12 notes up doubles the frequency.

**Why nothing is lower than C-4:** the micro:bit V2's built-in speaker is tiny and gives out almost nothing
below about 250 Hz.

---

## 5. Sounds: `wave` cells

These are all the wave names.

**Single-sound waves**

| Cell | Sound |
|---|---|
| `wave kick` | Kick drum |
| `wave snare` | Snare drum |
| `wave clap` | Clap |
| `wave hat` | Closed hi-hat (short) |
| `wave openhat` | Open hi-hat (longer) |
| `wave crash` | Crash cymbal |

**Waves that come in two pitches.** The tracker file has three sounds that can play at two
pitches. Giving each pitch its own name keeps every cell to two words:

| Cell | Sound | Tracker note it comes from |
|---|---|---|
| `wave tom_lo` / `wave tom_hi` | Low tom / high tom | C-4 / G-4 |
| `wave pew_lo` / `wave pew_hi` | Low zap / high zap | C-4 / C-5 |
| `wave hoover_e` / `wave hoover_a` | Hoover stab on E / on A | E-4 / A-4 |

That makes **12 wave names** in all.

---

## 6. What a cell does over time

`-` means "carry on": rest, do nothing, leave whatever is playing alone.

- `tone D-6` starts the note, and it **keeps sounding** through any `-` cells that follow, until the next `tone`, `wave` or `x`.
- `wave kick` plays its sound and lets it finish. A `-` after it does not cut it short.
- `x` stops whatever is playing.
- A new `tone` or `wave` replaces whatever was playing, like one channel on a tracker.
- `-` means "no change": it never makes a sound and never stops one.

---

## 7. Example: the first bar of the intro

Eight rows (one bar) for four micro:bits:

```
lead   x,-,-,-,-,-,-,-
bass   tone A-4,x,tone A-4,x,tone A-4,x,tone A-4,x
voice  x,tone A-5,x,tone C-6,x,tone E-6,x,tone C-6
drums  wave kick,wave hat,wave kick,wave hat,wave kick,wave hat,wave kick,wave hat
```

Reading the drums line: on row 0 play the kick, on row 1 the hat, on row 2 the kick, and so on. Each row is 200 ms.

The lead starts with `x` so it is silent at the start of the pattern.

---

## 8. Storing it in arrays

### One array entry per cell

Each cell is one entry in an array, so row 7 is the 7th entry. This reads like a tracker, a single cell can be
edited on its own, and you learn arrays and indexes without needing string splitting.

```
["x", "-", "-", "-", "-", "-", "-", "-"]
```

The only splitting left is turning one cell into its two words, for example `"tone D-6"` into `tone` and `D-6`.

### One array per pattern, plus an order list

- **A pattern array** holds the 32 cells of one pattern. A channel has up to 16 of them (for example `INT1`,
  `A1`, `B1`).
- **An order list** is an array of numbers saying which pattern plays next, for example `[0, 0, 1, 1, 10, 10, ...]`
  (up to 64 slots).

To play it: take the next number from the order list, find that pattern's array, then step through its 32 entries,
one every 200 ms.

### Keeping the blocks manageable

In Blocks, right-click a pattern's array block and choose **Collapse Block**. Each pattern then shows as one
line with its name, and you expand only the one you are editing.

If 32 entries is still too tall, an array per bar (8 entries) is an option. It means more blocks, so only do it
if collapsing is not enough.

---

## 9. Not in the format

- **Volume:** there are no volume levels. Every note plays at its sound's own volume.
- **Effects:** there are no effects (no slides, vibrato and so on).

---

## Appendix: where each wave comes from in the tracker file

The `.xm` tune file numbers its instruments 1 to 10:

| XM instrument | Cell |
|---|---|
| 1 | `tone` plus a note name, such as `tone D-6` or `tone D#6` (see section 4) |
| 2 | `wave kick` |
| 3 | `wave snare` |
| 4 | `wave clap` |
| 5 | `wave hat` |
| 6 | `wave openhat` |
| 7 | `wave crash` |
| 8 | `wave tom_lo` (C-4) or `wave tom_hi` (G-4) |
| 9 | `wave pew_lo` (C-4) or `wave pew_hi` (C-5) |
| 10 | `wave hoover_e` (E-4) or `wave hoover_a` (A-4) |

A note-off in the tracker becomes `x`, and an empty cell becomes `-`.
