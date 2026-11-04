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

## Where things are (4 Nov 14:20, after promoting)
- **Live** (project root): `main.py` = `old/main_no_start_song.py` (3 songs, 8 tracks, band 24 + power 7, no
  "start song", the B fix, the dim waiting row; tested on the boards 4 Nov: "more resilient"),
  `README.md` = `old/README_8_tracks.md`, `microbit-Technobit.hex` (fresh, 4 Nov 14:11).
  **Not yet promoted:** `old/microbit_tracker_format.md` (adds "The radio messages" and the waiting row) -
  copy it over the root `microbit_tracker_format.md`.
- `Claude/suggestions`: only this file. Everything else is in `old/`.
- `Claude/mods`: the three tunes - `korobeiniki_techno_8ch_v3_microbit.xm` (8 channels; 1-4 = the 4-track
  tune), `canon_bhangra_4ch_microbit.xm`, `ode_to_joy_synthwave_v3_4ch_microbit.xm`.
- `old/` in both: earlier steps, tries and promoted drafts, kept only to compare (and the generators that
  made the three `.xm` files). File names mentioned below are mostly in `old/` now.
- Flash (measured from the 14:11 hex): the V2 program area ends at 0x6B9A0, **about 45 KB free** below the
  bootloader (maybe a little less if MakeCode keeps some flash for storage).

## Decisions

### The tracker format (see `microbit_tracker_format.md` in the project root)
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

### Tried for song 3: Bella Ciao, chiptune techno
- Tune: `Claude/mods/bella_ciao_techno_4ch_microbit.xm`; generator `Claude/suggestions/make_bella_ciao_xm_microbit.py`.
- Traditional Italian folk song: only the traditional melody, no lyrics, no modern arrangement.
- Melody checked against 8notes.com's violin MIDI (fetched once through the built-in browser): the 8-bar verse
  matches note for note and every note is on the eighth-note grid, so nothing is rounded.
- Moved to A minor so the Hoover's two pitches (A, E) are the key note and its fifth. Lead E5-F6 (loud on the
  speaker). Chords per half bar: Am x7, A7 | A7, Dm, Dm, Am, Am, E7, E7, Am.
- Same setup and the same 10 instruments, byte for byte. Pattern names and the 64-slot song order follow
  Korobeiniki's; B1/B2 are the "bella ciao, bella ciao, bella ciao ciao ciao" hook chopped and looped.
- **Synthwave version** (`Claude/mods/bella_ciao_synthwave_4ch_microbit.xm`, generator
  `make_bella_ciao_synthwave_xm_microbit.py`): the techno version sounded too much like Korobeiniki, so this one
  changes the groove, not just the tune. Felt at half speed (75 BPM, one row = a 16th): half-time drums with a
  big snare on 2 and 4 and tom fills, a steady 16th-note bass, a two-octave arpeggio running on track 3 with
  Hoover hits in the choruses, the melody stretched to half speed (an octave lower in the verses). No acid
  octave pump, no pew-pews. Patterns: INT1 INT2 V1-V4 C1-C4 HK BR1 BR2 BU1 BU2 OUT.
- Bella Ciao's melody felt too weak in synthwave, so we moved on to Ode to Joy (below).
- Also tried: Dvorak's New World Symphony (XM in `mods`, not used: didn't work as techno). Ruled out as
  copyrighted: Knight Rider, West Side Story (until 2060), Midnight Diner's "Omoide".

### Song 3: Ode to Joy, drum-heavy synthwave (chosen 1 Nov)
- Beethoven's Symphony No. 9 (1824), public domain. Song `#`. The one to use:
  `Claude/mods/ode_to_joy_synthwave_v3_4ch_microbit.xm` (generator `make_ode_to_joy_synthwave_v3_xm_microbit.py`).
- How we got there:
  Three versions in `Claude/mods`: `ode_to_joy_trance_4ch_microbit.xm`,
  `ode_to_joy_minor_4ch_microbit.xm`, `ode_to_joy_synthwave_4ch_microbit.xm` (one generator,
  `make_ode_to_joy_xm_microbit.py trance|minor|synthwave`). Same tune, chords, patterns and order; only the
  arrangement differs. Melody written from memory, not checked against a score.
  Chosen style: **synthwave**, made drum heavy (1 Nov): in the drops track 3 is a second kit (claps on
  the snares, tom grooves, crashes, a tom cascade at the end).
  Then syncopated (it sounded too regular, "like a recorder recital"): the melody re-rhythmed with the
  same notes in the same order (3+3+1+1 and 2+1+3+2 bars, phrase B anticipating the beat), the kick in a
  3+3+2 pattern with the snare on the half-time backbeat, offbeat claps and toms on track 3, the bass
  locked to the kick, and a gated verse arpeggio. Off-beat notes: melody 14% -> 38%, kick 12% -> 40%.
  Then **v2, "everything at once"** (still sounded plain): `ode_to_joy_synthwave_v2_4ch_microbit.xm`,
  generator `make_ode_to_joy_synthwave_v2_xm_microbit.py`. The v1 file is kept to compare.
    1. Richer chords, two a bar: A F#m E A D A A E (phrase A), E E Bm F#m E A D E (phrase B).
    2. Minor verses, major drops: intro, verses and breakdown in A minor (C# -> C; Am F E Dm G), drops in A major.
    3. Key change: the last drops (KA KA2 KB) go up a step to B major, with Hoover brass hits on each bar.
    4. Counter-melody: in the verses track 3 answers the lead at the end of each bar.
    5. Edits: D1/KA stutter their last note, D2 cuts everything but the lead for the last half bar,
       D4/KA2 end in a tom cascade, the build ends with a beat of silence.
  Patterns: INT1 INT2 P1-P4 D1-D4 KA KA2 KB BR BU OUT (breakdown and build are one pattern each now).
  Checked: no melody note on a chord change is outside the chord, track 3 never plays a semitone from the
  lead, every cell converts to our format, same 10 instruments byte for byte.
  Then **v3, more drums** (v2 was "weirdly minor then anthemy" - good - but wanted more drums):
  `ode_to_joy_synthwave_v3_4ch_microbit.xm`, generator `make_ode_to_joy_synthwave_v3_xm_microbit.py`.
  Still 4 tracks (the conductor stays the metronome: we're recreating 4-track trackers). A micro:bit plays
  one sound at a time, so the extra drums go in the gaps; every tone is exactly as in v2:
    A. the bass track plays a clap/hat in its rests (rows 2 and 5 of each bar, and row 7 in the verses);
    B. in the drops track 3's second kit plays on nearly every row;
    C. in the verses track 3 has a light hat/tom/clap groove in the first half of each bar, under the
       counter-melody.
  No track doubles the same drum another track plays on that row (except the tom cascade, on purpose).
  About 44% more drum hits over the whole song.

### The boards and the code
- Tracks follow the XM channels: **1 lead** (melody), **2 acid** (bass), **3 vox** (voice lane: tone phrases plus
  claps, crashes, toms, pews, Hoover stabs), **4 drums** (kick and hats). **5-8 = extras** (see "8 tracks").
  **0 = conductor** (metronome + radio).
- Everything on the display is one character: tracks `0`-`8`, songs `*` (Korobeiniki), `+` (Canon),
  `#` (Ode to Joy).
- **Songs only** (1 Nov): the pattern screen is gone (a third set of 16 pattern letters would have been
  confusing). Controls: A = next track, logo = conductor (0), B = choose a song; then A = next song, B = play;
  B again = stop. Receivers still play whatever pattern number arrives by radio, so the radio sync is
  unchanged. Removed: `pattern_names`, `show_pattern_name`, `num_patterns`, the logo's songs/patterns switch;
  `choosing_pattern` became `choosing_song`. Patterns are now known by number (0-47) in the docs.
- Three songs, one per tune, each 64 patterns (about 6 min 50 s).
- In the code each track has 48 patterns: Korobeiniki's 16 (`lead_int1` ...) at 0-15, the Canon's 16
  (`canon_lead_int1` ...) at 16-31, Ode to Joy's 16 (`ode_lead_int1` ...) at 32-47. Each song's order list
  (`song_1` ...) points at its own patterns.
- Sounds: one function per sound (`play_kick` ...), recipes from `Claude/code/microbit_instruments.py`.
- LEDs: one LED at a time. Waves on rows 1-2, related sounds share an LED; the low/open one is at
  `bright_dim` = 128 (half), the other at 255. Tones on rows 4, 3, 2 by note (not octave). Track on row 0
  while playing (tracks 5-8: their partner's LED at half brightness).

### 8 tracks (1 Nov, agreed: v3, to test): `main_8_tracks_v3.py` + `korobeiniki_techno_8ch_v3_microbit.xm`
- Up to 8 boards plus the conductor. **The 4-track version must work on its own**: tracks 5-8 are extras that
  only ADD, and they are **drums and bass, not melody or chords**. The conductor stays the metronome (we're
  recreating 4-track trackers, and 8-track ones).
- Only Korobeiniki has its own tracks 5-8 (memory). In a 4-track song nobody is silent: **track 5 plays
  track 1, 6 plays 2, 7 plays 3, 8 plays 4** ("take away 4"). Done with the lists, not with logic:
  `patterns_bass2` etc. point at the Canon's and Ode to Joy's track 1-4 arrays (nothing copied).
- The 8-channel XM: channels 1-4 are byte for byte the 4-track tune (mute 5-8 in OpenMPT = the 4-track
  version). Every extra board plays in every pattern; the parts start small and grow, so the drops are
  still the biggest:
  - 5 `bass2`: a second bass line, only the chord's root / fifth / octave (C-4 up), short punchy notes: half
    notes in the intro, 3+3+2 in the verses, offbeats in the drops, a pump speeding up in the build.
  - 6 `kit2`: hats and snare: light hats on the beat early on, a soft pulse in the breakdown, claps speeding
    up with the build, a second kit in the drops, hats thinning out at the end.
  - 7 `perc`: toms and claps: pick-ups in the intro, a tom groove, tom runs in the fills, a heartbeat in the
    breakdown, toms speeding up in the build.
  - 8 `hits`: crashes, extra syncopated kicks, open hats, pews.
- Checked: no semitone clash between the extra bass and anything tonal; no drum doubled on two tracks on a row;
  tones C-4..B-6; the pre-drop silences stay silent; every extra pattern has something in it; on the mock
  micro:bit Korobeiniki's tracks 5-8 match the XM and the other songs' tracks 5-8 are tracks 1-4.
- 64 new arrays (256 in all). Estimated flash: about 165 KB of program (out of about 190 KB) - to be measured
  from a real hex.
- How we got here: v1 had harmony / arpeggio / Hoover extras, mostly in the drops ("works well musically"),
  but most extra boards had nothing to play early on - not great for students. v2 kept every board busy (with
  pads and arpeggios). v3 made the extras drums and bass ("a nice mix").

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

### Radio: no "start song", B fix, dim waiting row (4 Nov, tested and live in `main.py`): `main_no_start_song.py`
- Based on the current `main.py` (8 tracks, band 24, power 7). After "8-track Tetris works!" the radio was
  still the weak spot, so: simpler messages, and a way to SEE when a board is waiting.
- Messages now: **a number** = play this pattern and stay in the song; **`end song`** = after this pattern go
  back to the track screen; **`stop`** = stop now and go back. "start song" is gone: any number puts a board
  in the song (`receiving_song = True`), so a board can't miss the start of a song.
- **B fix**: B on a board that's following the conductor (`receiving_song`) now leaves the song and goes
  back to the track screen. Before, B mid-pattern did nothing visible (the board waited for the next number),
  and after a lost "end song" B opened the song screen while the board was still stuck in the song.
  Known and accepted: if the conductor is still playing, that board rejoins at the next pattern. To take boards
  out of a song that's still playing, stop the conductor.
- **Dim waiting row** (`show_waiting`): when a pattern ends and the next number hasn't arrived, the other
  LEDs on the top row light at `bright_wait` = 30 (around the track LED; only plots, no pause). The next
  pattern's `clear_screen` turns them off. Normally a board waits 1-5 ms (invisible), so the row only shows a
  lost number (for one pattern) or a lost "end song" (until B). Tune `bright_wait` on the boards: it has to
  look dimmer than tracks 5-8's half-bright track LED.
- Simulated (conductor + 2 boards, the same message lost in both versions):

  | Lost | Old code | New code |
  |---|---|---|
  | nothing | plays everything | plays everything |
  | "start song" | plays everything | (no such message) |
  | pattern 0's number | joins at the 2nd pattern | joins at the 2nd pattern, dim row while waiting |
  | a number mid-song | drops that pattern silently | drops that pattern, dim row while waiting |
  | "end song", then B | B opens the song screen, board still stuck in the song | dim row until B, then the track screen |
  | B mid-song | nothing visible | track screen, rejoins at the next pattern |

  So the new version never plays worse, shows when a board is waiting, and B always works. Correction: in the OLD code a lost "start song" did NOT spoil the song in the
  simulation (the next number arrives just before a board finishes, because boards run behind the
  conductor), so removing it is a simplification, not a big fix. The B fix and the waiting row are the gains.
- Later, if numbers are still often lost: send each one twice, with the song position so a repeat isn't
  replayed (patterns can legitimately repeat, e.g. INT1 INT1). Counting misses and logging (V2 data logger)
  also parked.

### Radio band (4 Nov, being tried): group 23, **band 24**
- Testing at home was unreliable: boards seemed dead, then played after being moved. The room is full of
  2.4 GHz wireless (Wi-Fi, Bluetooth, 2.4 GHz joypads ...) and "away from other wireless" isn't an option.
- `radio.set_group(23)` only filters messages; it doesn't change the frequency. `radio.set_frequency_band(n)`
  does: 2400 + n MHz, n = 0-83, default 7 (right on Wi-Fi channel 1).
- Picking a band: Wi-Fi channels 1 / 6 / 11 / 13 cover about 2402-2422 / 2427-2447 / 2452-2472 / 2462-2482 MHz.
  Gaps: bands 23-25 (between 1 and 6), 49-50 (between 6 and 11), 75-79 (above 11, only if nobody uses 13).
  Bluetooth hops over the whole band (brief collisions, can't be avoided) but advertises on fixed 2402, 2426,
  2480 MHz, so avoid bands 2, 26, 80. **24** is the middle of the first gap (23 is nearer Wi-Fi 1, 25 is
  nearer Bluetooth's 2426). Group 23 + band 23 was tempting (fnord), 24 is the safer bet.
- Band 24 and transmit power 7 are in `main.py` (4 Nov) and in `main_8_tracks_v3.py` (added 4 Nov, same place:
  straight after `radio.set_group(23)`). Fair test: conductor + one board, same spot, a whole song per band, listen for dropouts.
- Testing rig (4 Nov): the boards are now mounted on a board, close together and in fixed places (safe from
  cats jumping on the table), so radio tests are repeatable from one run to the next.
- `radio.set_transmit_power(7)` (the maximum) is the other idea, not tried yet.
- `radio.set_transmit_serial_number` (asked 4 Nov): adds the sender's serial number to every packet so a
  receiver can tell boards apart. Not needed - only the conductor sends.
- The README drafts and the format doc draft already say group 23 + band 24.

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

- [x] **3 songs on 4 boards** work with `main.py` (4 Nov).
- [x] **README promoted** (4 Nov 14:15): the root README is the 8-track version, links the root format doc.
- [x] Old `Claude/microbit_tracker_format_students.md` deleted (4 Nov); the root `microbit_tracker_format.md`
      is the format doc.
- [x] **8 tracks tested**: 8-track Tetris works on 8 boards + a conductor (4 Nov).
- [ ] **XM converter** and a **template XM** (4 channels, 32 rows, 10 instruments, speed 12 / tempo 150, no
      volume or effects) so a new tune goes from OpenMPT to MakeCode without hand copying. Design first,
      in small steps.
- [ ] **README, still to decide**: the VS Code section and the converter sentence (below).
- [ ] **README, VS Code section**: `main.py` is MakeCode Python (`basic.`, `music.create_sound_expression`,
      `radio.on_received_string`), not MicroPython, so adding `from microbit import *` and using "Put this
      file" won't run it. Loading `microbit-Technobit.hex` onto the MICROBIT drive would.
- [ ] **README, AI use**: "Claude Code has been used to create the .XM file conversion app" - the converter
      hasn't been written yet.
- [x] **Fresh hex** (4 Nov 14:11), measured: about 45 KB free.
- [ ] **Sounds and balance** on the real speakers: note any sound that is too quiet, too loud or wrong.
      The acid bass (around 440 Hz) is likely to be the quietest part.
- [ ] **First-beat lateness**: only if it can be heard.
- [x] **`main_no_start_song.py`** tested on the boards ("more resilient") and promoted to `main.py` with the
      README (4 Nov 14:15). Fresh hex downloaded.
- [ ] **Promote the format doc**: copy `Claude/suggestions/old/microbit_tracker_format.md` over the root
      `microbit_tracker_format.md` (it was missed: the root copy lacks "The radio messages" and the waiting row).
- [ ] **Radio band 24** (in `main.py` since 4 Nov, with transmit power 7: "not any worse"): keep testing it (see "Radio band" above). (Already in `main.py` and `main_8_tracks_v3.py`.) See also `main_no_start_song.py` (below).

---

## Done

- Tracker format documented, with a student version and a short "what is a tracker" intro.
- Existing code converted to the format: XM note names, name/Hz lookup tables, 12 agreed sounds, shared LEDs.
- The tune hardcoded from the XM (64 pattern arrays checked cell by cell against the XM).
- Single-character display, XM track order.
- Radio sync without the wait (message always interrupts). Working on the real boards.
- `play_note` uses substring blocks instead of Python's `split` (adopted in `main.py`, 1 Nov).
- Song 2 XM (Canon in D, bhangra techno) generated, checked and listened to in OpenMPT.
- Song 2 added to the code as song `+` (`main_two_songs.py`, adopted in `main.py`): all 64 Canon arrays match the XM; both songs
  checked on the mock micro:bit.
- Song 3 chosen: Ode to Joy, drum-heavy synthwave (v3), after trying New World, Bella Ciao (techno and
  synthwave) and three Ode to Joy styles; v1 -> syncopated -> v2 "everything at once" -> v3 more drums.
- Songs-only controls and Ode to Joy as song `#` (`main_three_songs.py`, copied to `main.py` 1 Nov, untested on
  the boards): the pattern screen removed; all 64
  Ode to Joy arrays match the XM; all three songs checked on the mock micro:bit (same sounds per track as
  their XMs) and the buttons simulated (track, conductor, song choice, play, radio messages).
- README draft updated for three tunes, the songs-only controls and tracks 1-8.
- Format doc draft updated: three tunes, tracks 5-8 and the "take away 4" rule, patterns by number (0-47)
  with an Ode to Joy table, the track LED.
- 8 tracks: Korobeiniki 8-channel XM v3 (tracks 1-4 unchanged, extras = drums and bass) and
  `main_8_tracks_v3.py`; checked on the mock micro:bit. Agreed 1 Nov ("a nice mix"); to test on the boards.
- Tidied (1 Nov): only the files in use are at the top of `Claude/suggestions` and `Claude/mods`; earlier
  steps and tries moved to `old/` in each (see "Where things are").
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
