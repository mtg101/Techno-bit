# The micro:bit tracker format

## What is a tracker?

Back in the Middle Ages (the late 1980s) people wrote music for computers like the Amiga using programs called
**trackers**. Instead of a piano roll or sheet music, a tracker is a grid: each column is a **channel**, each row is
a tiny slice of time, and each cell says which note or sound to play. Our tunes use the same idea, so you can read
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

## 7. Example: the first bar of Korobeiniki's intro

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

- **A pattern array** holds the 32 cells of one pattern. There are two tunes with 16 patterns each, so each
  channel has 32 arrays, named after the channel and the pattern: Korobeiniki's are `lead_int1`, `drums_bu2` and
  so on, and the Canon's start with `canon_`, such as `canon_lead_v3`.
- **An order list** is an array of numbers saying which pattern plays next. Each tune has one: `song_1`
  (Korobeiniki) uses patterns 0 to 15, and `song_2` (the Canon) uses patterns 16 to 31. Each is 64 numbers long,
  which is 6 minutes 50 seconds of music.

To play it: take the next number from the order list, find that pattern's array, then step through its 32 entries,
one every 200 ms.

### The channels

Both tunes have the same 4 channels. Each micro:bit plays one, chosen by its track number. Track 0 is the
conductor, which keeps the beat and tells the others which pattern to play.

| Track | Channel | What it plays |
|---|---|---|
| 0 | conductor | A metronome, and the radio messages that start the others |
| 1 | `lead` | The melody (tone notes) |
| 2 | `acid` | The acid bass line (tone notes) |
| 3 | `vox` | The voice lane: tone phrases, plus claps, crashes, toms, pews and Hoover stabs. In the Canon it also plays the dhol groove and the second canon voice |
| 4 | `drums` | The kick and hats, plus snare and toms in the fills |

### The patterns

The display shows one letter per pattern: capitals for Korobeiniki, small letters for the Canon. The number in
an order list is the pattern's position: A is 0, P is 15, a is 16 and p is 31.

**Korobeiniki (the Tetris tune), A to P**

| Letter | Name in the code | What it is |
|---|---|---|
| A | `int1` | Intro 1: kick, hats, pings, a sparse bass |
| B | `int2` | Intro 2: adds clap, arpeggio and Hoover stabs |
| C | `va1` | Verse on tune A |
| D | `va2` | Verse on tune A, with Hoover stabs |
| E | `a1` | Drop, tune A |
| F | `a2` | Drop, tune A, with a pew-pew fill at the end |
| G | `a1x` | Drop, tune A, variant |
| H | `a2x` | Drop, tune A, variant |
| I | `b1` | Drop, tune B |
| J | `b2` | Drop, tune B, with a fill at the end |
| K | `br1` | Breakdown: no drums, tune B quiet |
| L | `br2` | Breakdown, second half |
| M | `bu1` | Build: rising stutter, pew-pew, snare roll |
| N | `bu2` | Build, second half, ending in a beat of silence |
| O | `rld` | Reload: a held Hoover and a teaser of tune A |
| P | `out` | Outro: the kick fades out |

**Pachelbel's Canon in D (bhangra techno), a to p**

The Canon's chords and bass repeat every pattern: D, A, Bm, F#m, G, D, G, A. Lines 1 to 3 are Pachelbel's own
violin lines; line 4 is new. In a canon, a second voice plays the same line later: here track 3 plays the line
that track 1 played in the pattern before.

| Letter | Name in the code | What it is |
|---|---|---|
| a | `int1` | Intro 1: the bass alone, kick, hats and pings |
| b | `int2` | Intro 2: the bass on the beat, an arpeggio and Hoover stabs |
| c | `v1` | Line 1 over the dhol groove |
| d | `v2` | Line 2, with line 1 underneath on track 3: the canon starts |
| e | `v3` | Line 3, with line 2 underneath |
| f | `v4` | Line 4, with line 3 underneath |
| g | `d1` | Drop: line 3, dhol, crash and Hoover stabs |
| h | `d2` | Drop: line 4, with a fill at the end |
| i | `d1x` | Drop variant: rolling bass, closed hats |
| j | `d2x` | Drop variant, with a fill at the end |
| k | `br1` | Breakdown: no drums, line 1 over a held bass and an arpeggio |
| l | `br2` | Breakdown, line 2 |
| m | `bu1` | Build: rising stutter, pew-pew, snare roll |
| n | `bu2` | Build, second half, ending in a beat of silence |
| o | `rld` | Reload: a held Hoover and the start of line 1, then a mini-build |
| p | `out` | Outro: the kick fades out |

### Keeping the blocks manageable

In Blocks, right-click a pattern's array block and choose **Collapse Block**. Each pattern then shows as one
line with its name, and you expand only the one you are editing.

If 32 entries is still too tall, an array per bar (8 entries) is an option. It means more blocks, so only do it
if collapsing is not enough.

---

## 9. How the micro:bit plays a cell

1. **Timing.** `play_track` goes through a pattern's 32 cells. For each one it notes the time, plays the cell,
   then waits until 200 ms have passed since that note. Timing from the clock, not from the length of the
   code, keeps the rows evenly spaced. The wait also stops early if the conductor's next pattern number arrives,
   so every micro:bit starts the next pattern together, with no gap.
2. **Which kind of cell?** `play_note` looks at the cell and decides:
   - `x` stops all sound and switches the LED off.
   - `-` switches the LED off and does nothing else, so a tone that is playing keeps sounding.
   - `tone D-6` stops any old sound. Every tone cell has the same layout, so the code can pick it apart by
     position: letters 0 to 3 are `tone`, letter 4 is a space and letters 5 to 7 are the note name. The
     **substring** block takes the 3 letters from position 5 (`D-6`), `play_tone` finds that name in the
     `note_names` array with `index_of`, and takes the number at the same position in the `note_hz` array.
     That number is the frequency, and `music.ring_tone` plays it.
   - `wave kick` calls the function with that sound's recipe, such as `play_kick()`.
3. **Each sound function** does three things: stops the old sound, plays its own sound in the background with
   `music.create_sound_expression`, and lights its LED with `show_sound`.

---

## 10. The LEDs

The 5 x 5 LED display shows what is playing. Only one sound LED is lit at a time.

**Wave sounds** use rows 1 and 2. Related sounds share an LED: the low or open sound is at half brightness
and the other at full brightness.

| | x0 | x1 | x2 | x3 | x4 |
|---|---|---|---|---|---|
| **Row 1** | clap | tom (low dim, high bright) | hat (open hat dim) | snare | kick |
| **Row 2** | | | crash | hoover (E dim, A bright) | pew (low dim, high bright) |

**Tones** light one LED for the note, on rows 4, 3 and 2:

| | x0 | x1 | x2 | x3 | x4 |
|---|---|---|---|---|---|
| **Row 4** | C | C# | D | D# | E |
| **Row 3** | F | F# | G | G# | A |
| **Row 2** | A# | B | | | |

The LED shows the note but not the octave. The half brightness is set by the variable `bright_dim` (128 out of 255).

---

## 11. Not in the format

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
