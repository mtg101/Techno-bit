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

## Where things are (1 Nov, end of day)
- `Claude/suggestions`:
  - `main_8_tracks_v3.py` - **the code to test next**: 3 songs, songs-only controls, tracks 0-8.
  - Drafts: `README.md` (matches the current `main.py`: 3 songs, 4 tracks, songs only - to copy over the
    root README now), `README_8_tracks.md` (for when `main_8_tracks_v3.py` becomes `main.py`),
    `microbit_tracker_format_students.md` (8-track version; copy over `Claude/microbit_tracker_format_students.md`
    with the 8-track code).
  - This file.
- **`main.py` (in GitHub since 1 Nov 22:58) = `old/main_three_songs.py`**: 3 songs, 4 tracks, songs only.
  Copied over by Russell, not yet tested on the boards.
- `Claude/mods`: the three tunes - `korobeiniki_techno_8ch_v3_microbit.xm` (8 channels; 1-4 = the 4-track
  tune), `canon_bhangra_4ch_microbit.xm`, `ode_to_joy_synthwave_v3_4ch_microbit.xm`.
- `old/` in both: earlier steps and tries, kept only to compare. Python: `main_agreed_format.py`,
  `main_agreed_instruments.py`, `main_korobeiniki.py`, `main_interrupt.py`, `main_substring.py`,
  `main_two_songs.py` (2 songs with the pattern screen: the version before), `main_three_songs.py` (= `main.py`),
  `main_8_tracks.py` (v1) and `main_8_tracks_v2.py`. Tunes: `korobeiniki_techno_4ch_microbit.xm` (= channels
  1-4 of the 8-track), the 8-track v1 and v2, early Korobeiniki versions, New World, Bella Ciao (techno,
  synthwave), Ode to Joy trance/minor/synthwave v1/v2, with their generators. Also the generators of the three
  tunes in use (`make_korobeiniki_8ch_v3_xm_microbit.py`, `make_canon_xm_microbit.py`,
  `make_ode_to_joy_synthwave_v3_xm_microbit.py`): they made the `.xm` files, nothing runs them. File names
  mentioned below for any of these are now in `old/`.

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

- [ ] **Test the current `main.py`** (3 songs, 4 tracks, songs only) on the boards, and copy
      `Claude/suggestions/README.md` over the root README (it matches this `main.py`).
- [ ] **Test `main_8_tracks_v3.py`** (agreed 1 Nov): in MakeCode (paste, flip to Blocks: watch the conversion
      of the ~190 KB file) and on the boards - 4 boards should sound exactly like before, 8 boards + a
      conductor if there are enough. Memory: 256 pattern arrays. Then adopt it as `main.py`, copy the README
      and format doc drafts over, download a fresh `.hex` and measure it. If 8 tracks has to wait,
      the current `main.py` (3 songs, 4 tracks) is the fallback.

- [ ] **XM converter** and a **template XM** (4 channels, 32 rows, 10 instruments, speed 12 / tempo 150, no
      volume or effects) so a new tune goes from OpenMPT to MakeCode without hand copying. Design first,
      in small steps.
- [ ] **README and format doc drafts** are up to date (3 tunes, songs-only controls, tracks 1-8, the track
      LED; format doc: 8 tracks, patterns by number with an Ode to Joy table). Copy them over once
      `main_8_tracks_v3.py` is adopted. Still to decide in the README: the VS Code section and the converter
      sentence (below).
- [ ] **README, VS Code section**: `main.py` is MakeCode Python (`basic.`, `music.create_sound_expression`,
      `radio.on_received_string`), not MicroPython, so adding `from microbit import *` and using "Put this
      file" won't run it. Loading `microbit-Technobit.hex` onto the MICROBIT drive would.
- [ ] **README, AI use**: "Claude Code has been used to create the .XM file conversion app" - the converter
      hasn't been written yet.
- [ ] **The .hex file** `microbit-Technobit.hex` was built before the Canon and Ode to Joy were added; download a fresh one
      from MakeCode before checking in.
- [ ] **Sounds and balance** on the real speakers: note any sound that is too quiet, too loud or wrong.
      The acid bass (around 440 Hz) is likely to be the quietest part.
- [ ] **First-beat lateness**: only if it can be heard.

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
