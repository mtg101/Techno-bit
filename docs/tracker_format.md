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

A tune has 4 channels that make the whole tune, and 4 extra ones (drums and bass) for up to 8 micro:bits (see section 8).

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
- A tune in **3/4** (a waltz) can still use 32-row patterns: its bars just run on across the pattern ends.
  Midnight Diner's slow waltz bars are 12 rows (3 beats of 4 rows) and its fast ones 6 rows (3 beats of 2 rows),
  so 3 patterns (96 rows) hold exactly 8 slow bars or 16 fast ones.

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

Each tune is its own program (`korobeiniki.py`, `canon.py`, `ode_to_joy.py`, `midnight_diner.py`): the tracker code is
the same in all four, only the arrays change.

- **A pattern array** holds the 32 cells of one pattern, named after its track and its pattern number:
  `track1_p00`, `track1_p01` ... `track1_p15` for track 1, `track2_p00` ... for track 2, and so on.
- **A track's list** puts that track's patterns in order: `track1_patterns` holds `track1_p00` to `track1_p15`.
  `track0_patterns` is the conductor's metronome.
- **`song_tracks`** holds all the lists, so `song_tracks[track][pattern]` is one pattern's array for one track.
- **The order list**, `song`, is an array of numbers saying which pattern plays next. Each number is 6.4
  seconds of music: our first three tunes are 64 numbers long (6 minutes 50 seconds), Midnight Diner 28 (3 minutes).
- A tune can have **any number of patterns** (Midnight Diner has 19, `track1_p00` to `track1_p18`), as long as it
  fits in the micro:bit's memory.

To play it: take the next number from the order list, find that pattern's array, then step through its 32 entries,
one every 200 ms.

### The tracks

Each micro:bit plays one track, chosen by its track number. Track 0 is the conductor, which keeps the beat and
tells the others which pattern to play. Tracks 1 to 4 play the whole tune on their own. Tracks 5 to 8 are
**extras** for up to 8 micro:bits: they only add drums and bass, so the tune still works with just 4.

| Track | In the code | What it plays (in Korobeiniki; other tunes use their tracks in their own way) |
|---|---|---|
| 0 | `track0` (conductor) | A metronome, and the radio messages that start the others |
| 1 | `track1` | The melody (tone notes) |
| 2 | `track2` | The acid bass line (tone notes) |
| 3 | `track3` | The voice lane: tone phrases, plus claps, crashes, toms, pews and Hoover stabs. In the Canon it also plays the dhol groove and the second canon voice; in Ode to Joy the counter-melody and a second drum kit |
| 4 | `track4` | The kick and hats, plus snare and toms in the fills |
| 5 | `track5` | Extra: a second bass line, only the chord's root, fifth and octave, in short notes |
| 6 | `track6` | Extra: hats and snare |
| 7 | `track7` | Extra: toms and claps |
| 8 | `track8` | Extra: crashes, extra kicks, open hats and pews |

All four of our tunes have their own tracks 5 to 8. A tune can also have just 4 tracks: then nobody sits out,
because track 5 plays track 1's part, 6 plays 2, 7 plays 3 and 8 plays 4 ("take away 4"). The code does this
with the lists, not with extra logic: in a 4-track tune, `track5_patterns` simply holds `track1_p00`,
`track1_p01` and so on.

### The patterns

The display shows only the track, so patterns are known by their number in the order list. A pattern's
number is in its array names (pattern 3 = `track1_p03`, `track2_p03` ...). The part names below come from how
each tune was written; they are not in the code.

**Korobeiniki (the Tetris tune), patterns 0 to 15.** The extras (tracks 5-8) start small in the intro and grow,
so the drops are the biggest moments.

| Number | Part | What it is |
|---|---|---|
| 0 | `int1` | Intro 1: kick, hats, pings, a sparse bass |
| 1 | `int2` | Intro 2: adds clap, arpeggio and Hoover stabs |
| 2 | `va1` | Verse on tune A |
| 3 | `va2` | Verse on tune A, with Hoover stabs |
| 4 | `a1` | Drop, tune A |
| 5 | `a2` | Drop, tune A, with a pew-pew fill at the end |
| 6 | `a1x` | Drop, tune A, variant |
| 7 | `a2x` | Drop, tune A, variant |
| 8 | `b1` | Drop, tune B |
| 9 | `b2` | Drop, tune B, with a fill at the end |
| 10 | `br1` | Breakdown: no drums, tune B quiet |
| 11 | `br2` | Breakdown, second half |
| 12 | `bu1` | Build: rising stutter, pew-pew, snare roll |
| 13 | `bu2` | Build, second half, ending in a beat of silence |
| 14 | `rld` | Reload: a held Hoover and a teaser of tune A |
| 15 | `out` | Outro: the kick fades out |

**Pachelbel's Canon in D (bhangra techno), patterns 0 to 15**

The Canon's chords and bass repeat every pattern: D, A, Bm, F#m, G, D, G, A. Lines 1 to 3 are Pachelbel's own
violin lines; line 4 is new. In a canon, a second voice plays the same line later: here track 3 plays the line
that track 1 played in the pattern before.

| Number | Part | What it is |
|---|---|---|
| 0 | `int1` | Intro 1: the bass alone, kick, hats and pings |
| 1 | `int2` | Intro 2: the bass on the beat, an arpeggio and Hoover stabs |
| 2 | `v1` | Line 1 over the dhol groove |
| 3 | `v2` | Line 2, with line 1 underneath on track 3: the canon starts |
| 4 | `v3` | Line 3, with line 2 underneath |
| 5 | `v4` | Line 4, with line 3 underneath |
| 6 | `d1` | Drop: line 3, dhol, crash and Hoover stabs |
| 7 | `d2` | Drop: line 4, with a fill at the end |
| 8 | `d1x` | Drop variant: rolling bass, closed hats |
| 9 | `d2x` | Drop variant, with a fill at the end |
| 10 | `br1` | Breakdown: no drums, line 1 over a held bass and an arpeggio |
| 11 | `br2` | Breakdown, line 2 |
| 12 | `bu1` | Build: rising stutter, pew-pew, snare roll |
| 13 | `bu2` | Build, second half, ending in a beat of silence |
| 14 | `rld` | Reload: a held Hoover and the start of line 1, then a mini-build |
| 15 | `out` | Outro: the kick fades out |

**Beethoven's Ode to Joy (drum-heavy synthwave), patterns 0 to 15**

Felt at half speed (one row is a sixteenth note at 75 BPM), with a syncopated melody and a 3+3+2 kick. The
verses are in A minor, the drops burst into A major, and the last drops go up a step to B major (a key change).

| Number | Part | What it is |
|---|---|---|
| 0 | `int1` | Intro 1: a gated arpeggio, then the bass (A minor) |
| 1 | `int2` | Intro 2: adds the verse drums and a fill |
| 2 | `p1` | Verse, phrase A in A minor, with a counter-melody on track 3 |
| 3 | `p2` | Verse, phrase A again (ending on the home note) |
| 4 | `p3` | Verse, phrase B |
| 5 | `p4` | Verse, phrase A, with a fill |
| 6 | `d1` | Drop in A major, phrase A; the last note stutters |
| 7 | `d2` | Drop, phrase A; everything but the melody stops for half a bar |
| 8 | `d3` | Drop, phrase B |
| 9 | `d4` | Drop, phrase A, ending in a tom cascade |
| 10 | `ka` | Key change: drop up a step (B major), Hoover brass, stutter |
| 11 | `ka2` | Key change drop, tom cascade |
| 12 | `kb` | Key change drop, phrase B |
| 13 | `br` | Breakdown: no drums, A minor, arpeggio and Hoover pad |
| 14 | `bu` | Build: the roll speeds up, then a beat of silence |
| 15 | `out` | Outro in B major: a held note, the beat falls away |

**Midnight Diner (waltz techno in 3/4), patterns 0 to 18**

The melody is the Irish air "Pretty Maid Milking Her Cow" (18th century), which the *Midnight Diner* theme is
based on, in E minor. Its A and B parts are 16 bars each. The first half plays at the tune's own speed (a bar
every 2.4 seconds); then it drops into double time (a bar every 1.2 seconds) for the techno. It is mostly melody
and beats: track 2 plays the **bass notes**, and track 5 a **bass rumble** on the same notes, because one
micro:bit speaker can't do much bass on its own.

| Number | Part | What it is |
|---|---|---|
| 0-2 | `so` | Part A, first 8 bars: the melody alone |
| 3-5 | `jn` | Part A, last 8 bars: the bass notes join |
| 6-11 | `bu` | Part B, building: a kick, then claps and the rumble, then hats and toms, then a snare roll that speeds up, ending in a moment of silence |
| 12-14 | `fb` | The drop, part B: double time, a kick on every beat, snare on 2, clap on 3, both basses, a Hoover stab every 4 bars |
| 15-17 | `fa` | The drop, part A, ending in a drum roll |
| 18 | `out` | The ending: the last two bars, slow, alone |

The order is 0-11, then the drops 15-17, 12-14, 15-17, 12-14, 15-17, then 18.

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

### The radio messages

The conductor only ever sends three kinds of message:

| Message | What a board does |
|---|---|
| a pattern number, such as `12` | Play that pattern now, and stay in the song: when it ends, wait for the next number |
| `end song` | Finish the pattern you're playing, then go back to the track screen |
| `stop` | Stop now and go back to the track screen |

A board joins a song as soon as it hears a number, so there is no "start" message to miss. Pressing B on a
board that is following the conductor also takes it back to its track screen.

### The radio: group and band

The conductor sends each pattern number by radio. Two radio settings decide which boards hear it:

- **The group** (`radio set group 23`) is like a name tag on every message. A board only listens to messages
  for its own group, so two Techno:bit bands in the same room can play different songs. It does **not**
  change the frequency: every group shares the same airwaves.
- **The band** (`radio set frequency band 24`) is the actual frequency: 2400 + 24 = **2424 MHz**. This is
  the same 2.4 GHz range used by Wi-Fi, Bluetooth, wireless game controllers and more, so a busy room can
  drown the messages out. If a board misses a pattern number, it drops out until the next one arrives.

We use group 23 and band 24. Band 24 sits in a gap: just above Wi-Fi channel 1 (about 2402-2422 MHz),
below Wi-Fi channel 6 (about 2427-2447 MHz), and just clear of a frequency every Bluetooth device uses to
announce itself (2426 MHz). The default band, 7, is right on top of Wi-Fi channel 1. **Every board,
conductor included, must use the same group and the same band**, or they can't hear each other.

## 10. The LEDs

The 5 x 5 LED display shows what is playing. Only one sound LED is lit at a time.

**The track** is shown on row 0 while playing: tracks 0 to 4 light x0 to x4. The top row only has 5 LEDs, so
tracks 5 to 8 light the same LED as their partner track (5 with 1, 6 with 2 and so on) at half brightness.

**Waiting:** if a pattern ends and the next pattern number hasn't arrived, the board lights the rest of the
top row very dimly (`bright_wait`). Normally the next number arrives within a few milliseconds, too fast to
see, so a dim top row means the board has missed a message. It carries on when the next number arrives, or
goes back to its track screen when you press B. Lighting LEDs with `plot` takes no time, unlike `show string`,
so this never makes the music late.

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
