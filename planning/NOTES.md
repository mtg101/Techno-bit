# Techno:bit notes

A running record of what we have decided and what is left to do. Claude keeps this file at
`planning/NOTES.md`.

Last updated: 5 November 2026, 00:20.

---

## Summary: where we are (5 Nov 00:20)

**Everything promoted** (agreed 5 Nov 00:17: "good let's promote everything"; before that 4 Nov 22:19).
`planning/` holds only these notes; nothing is pending.

**Promoted 5 Nov 00:18: song 4, Midnight Diner.** `midnight_diner.py`, `mods/midnight_diner.xm`, `README.md` (four
tunes, hex links with MakeCode's names) and `docs/tracker_format.md` (3/4 bars, any number of patterns, the Midnight
Diner table): each matched its draft byte for byte, all links work, drafts removed. The hex
`hex/microbit-TB-midnight-diner.hex` came from Russell's MakeCode project. **Still to do:** play it on the real boards.

**Promoted 5 Nov 00:24: a new README intro** ("the intro is weak - add that it's for teaching students about
coding, but not lame"): a table of micro:bits playing techno as a band, the Amiga tracker roots kept, and why: it's
for the coding club, the music is the hook for arrays, timing and radio, and it's all in Blocks to take apart.

**Live** (top level since 23:15): **one program per song, all 8 tracks**: `korobeiniki.py`, `canon.py`, `ode_to_joy.py`,
`midnight_diner.py`
(same tracker code, generic names `track1_p00` ..., no song screen: A = track, logo = conductor, B = play/stop).
The 8-channel `mods/*.xm`. `docs/guide.md` (for students), `docs/tracker_format.md`. Front page `README.md` with
"How to play". The old 3-song `main.py` and `hex/techno-bit.hex` were removed (in git history, the commit before).

**MakeCode projects** (made by Russell, 4 Nov 22:36; in the front page and the guide):
Korobeiniki https://makecode.microbit.org/S54592-76373-74001-91871 ,
Canon https://makecode.microbit.org/S16435-66036-39782-77562 ,
Ode to Joy https://makecode.microbit.org/S92579-43021-82836-81182 .
Midnight Diner https://makecode.microbit.org/S89025-71001-08778-34052 (made 5 Nov 00:07; in the README draft).
**Hex names (5 Nov 00:15):** the hexes keep MakeCode's own download names: `hex/microbit-TB-Korobeiniki-Tetris.hex`,
`microbit-TB-canon.hex`, `microbit-TB-ode_to_joy.hex`, `microbit-TB-midnight-diner.hex` (the first three are the same
files as before, same md5, only renamed). README links updated; the old 3-song `microbit-Technobit.hex` is gone (settled).
(The original all-in-one project https://makecode.microbit.org/S26000-11508-29408-02742 is mentioned as history.)

**Not yet tested on the real boards** (checked only on the mock micro:bit):
1. Listen to the 8-track Canon and Ode to Joy in OpenMPT.
2. MakeCode on a student laptop: the three projects exist now (links above) - is Blocks fast enough? (About 4,000 blocks each now: all three have 8 tracks.)
3. The boards: 4 boards, 8 + a conductor, B on a single track.
4. ~~Download the three hexes~~ Done 4 Nov 22:49: `techno-bit/hex/korobeiniki.hex`, `canon.hex`, `ode_to_joy.hex` (back to MakeCode's names 5 Nov 00:15)
   (downloaded from the three MakeCode projects; renamed from MakeCode's `microbit-TB-...` names). Measured:
   **about 111 KB free** in each (the 3-song hex had 46 KB). If something's wrong, the tested 3-song `main.py`
   and its hex are in git history.

**Song 4 (promoted 5 Nov 00:18; drafted 00:10):** Midnight Diner. Russell, 00:01: "that's pretty smooth". Drafts in `planning/`:
`mods/midnight_diner.xm` (the sixth try), `midnight_diner.py` (built from it: the tracker code is identical to `canon.py`, checked
by AST; on the mock micro:bit every track plays exactly what the XM says, 179.2 s, all tones found), `README.md`
(a fourth row in the tunes table, "four tunes"; the MakeCode link says "to come") and `docs/tracker_format.md`
(waltz bars across patterns, any number of patterns, a Midnight Diner pattern table). **Next:** Russell makes the
MakeCode project from `planning/midnight_diner.py` and downloads `hex/microbit-TB-midnight-diner.hex`; Claude puts the link in, then we promote.
Renamed 5 Nov 00:06 ("rename all the 'diner' to 'midnight diner'"): the tune is **Midnight Diner**, the files
`midnight_diner.py`, `mods/midnight_diner.xm`, `hex/microbit-TB-midnight-diner.hex` (the XM's title too; older notes updated).

**Song 5: Bella Ciao, Latin techno - dropped** (5 Nov 00:45, "that doesn't work as techno - reverse ferret and
abandon all that"). The draft `.xm` is deleted (never committed); what was tried is under "Song 5" below.

**Next after that:** making tunes from `.xm` files - the converter and its rules doc (draft in git at
`f50c8f5`, needs the new names; no template needed: any song's program and `.xm` serve as one). Later a web page.

**Parked:** sending radio numbers twice / counting misses / logging; compiling on the PC with MakeCode's own
command-line compiler; sound balance; more tempos and instruments.

**How we work:** see "How we work" below.

---

## How we work (agreed 4 Nov)

**The layout** (4 Nov 23:15: students' material at the top, planning in one folder off to the side):
```
README.md          the GitHub front page = the guide: what it is, demo, the tunes, getting them on, how to play
korobeiniki.py  canon.py  ode_to_joy.py  midnight_diner.py      one program per tune
hex/  mods/  docs/  media/                   ready-to-flash files, .xm tunes, tracker_format.md, the video
planning/          for us: NOTES.md (this file) + drafts of changes ("Not needed to play")
```

**`planning/` mirrors the project exactly** (except itself): a draft has the real file's path with `planning/` in
front - `planning/README.md` is a draft of `README.md`, `planning/canon.py` a draft of `canon.py`,
`planning/mods/x.xm` a draft of `mods/x.xm`. The one extra file is **`NOTES.md`**, which is never promoted.

**The steps, every time:**
1. **Draft:** Claude writes or changes files in `planning/`, at their real paths (only the files being changed).
2. **Check:** Claude checks the drafts before showing them: on the mock micro:bit for code, links for docs.
3. **Talk it through:** Claude explains what changed and why; Russell reads and asks.
4. **Agree:** promoting happens when we agree on it in the conversation - no separate permission questions.
5. **Promote:** Claude copies `planning/<path>` to `<path>`, checks each one matches byte for byte (and the
   links work), then **deletes the draft**.
6. **Remove what's replaced:** files the promotion makes obsolete (an old program, an old hex) are deleted,
   not kept.
7. **Test and commit:** Russell tests code on the real boards, then commits in VS Code (**Stage All** first, so
   moves are recorded as renames) and pushes. Claude never commits or pushes.

So **`planning/` holds only NOTES.md and what's pending**: when it's just NOTES.md, everything is in step.
**No `old` folders, no "_old" files:** git keeps the history, so anything replaced is deleted, and NOTES.md
says where to find it (the commit) if it might be wanted again.

**Who may change what:** Claude can change anything in `planning/` and can tidy the project (move, rename,
fix links); anything else in the project changes only by promoting (steps 4-5).

**Code rules:**
- **Go slowly.** One small step at a time, explained well enough to repeat to the coding club. No big code
  drops without a go-ahead.
- All Python must be **block compatible**: paste into MakeCode, flip to Blocks, and it should render as real
  blocks, with no grey `<python code>` blocks hiding logic. Avoid Python string methods such as `.split()`,
  `.find()`, `.strip()`: MakeCode turns them into hidden helpers with no block. Use the text blocks instead:
  `substr`, `index_of`, `char_at`, `includes`.
- **MakeCode is the source of truth for the block layout.** The `.py` files in GitHub are copies for version
  control; MakeCode writes functions in its own order when it exports Python, so when a program comes back from
  MakeCode, Claude compares it by what it does (functions, arrays), not by its text.

---

## Where things are (5 Nov 00:20)

```
README.md                         the front page and guide (merged 4 Nov 23:15; docs/guide.md folded into it)
korobeiniki.py canon.py ode_to_joy.py midnight_diner.py   one program per song, 8 tracks each
mods/   korobeiniki.xm canon.xm ode_to_joy.xm midnight_diner.xm   (all 8 channels)
hex/    microbit-TB-Korobeiniki-Tetris.hex microbit-TB-canon.hex microbit-TB-ode_to_joy.hex microbit-TB-midnight-diner.hex
docs/   tracker_format.md
media/  technobit-demo.mp4
planning/NOTES.md                 these notes (nothing else pending)
```
(Until 4 Nov 23:10 the students' files were in a `techno-bit/` folder; NOTES entries before then use those paths.)

**Promoted 4 Nov 17:10** (agreed: "just docs and we agreed it's good"): `README.md` (the front page),
`techno-bit/docs/guide.md` (for students), `techno-bit/docs/tracker_format.md` (the newest format doc). All links
checked (one fixed: the video is at `techno-bit/media/`). Nothing pending in `planning/` now.
**Promoted 4 Nov 17:20:** a fuller front page `README.md` (title, "What it is", "How it works (the techie bit)",
"Try it", and a rewritten "AI use" saying honestly who does what). (A VS Code README in `techno-bit/tools/local_build/`
was promoted too, then deleted with that folder the same day.) Every line of the old front page is now in one of the
READMEs. Nothing pending in `planning/`.

**Pending (in `planning/`, to TEST before promoting):** one program per song (agreed 4 Nov 17:34):
- `techno-bit/korobeiniki.py` (8 tracks, 92 KB), `techno-bit/canon.py` (56 KB), `techno-bit/ode_to_joy.py`
  (55 KB) - replace `techno-bit/main.py` (195 KB, all three).
- `techno-bit/docs/guide.md`, `techno-bit/docs/tracker_format.md`, `README.md` (front page) updated to match.
- Then: one MakeCode project per tune, hexes saved as `techno-bit/hex/<tune>.hex`; `main.py` and
  `hex/techno-bit.hex` go.

**The first one-song attempt + the XM converter** were deleted from `planning/single_song_paused/`
(4 Nov 17:42); they're in git at commit `f50c8f5` ("more refactors..."), path
`planning/single_song_paused/techno-bit/`. For the XM step, get back `tools/xm_to_makecode.py` and
`docs/making_tunes.md` from there (`git show f50c8f5:planning/single_song_paused/techno-bit/tools/xm_to_makecode.py`);
they use the older `lead_00` names and need updating to `track1_p00`.

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
- Tune: `mods/korobeiniki_techno_4ch_microbit.xm` (4 channels, 16 patterns, 64-slot order list, 10 instruments).

### Song 2: Canon in D, bhangra techno
- Tune: `mods/canon_bhangra_4ch_microbit.xm`; generator `planning/make_canon_xm_microbit.py`.
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
- Tune: `mods/bella_ciao_techno_4ch_microbit.xm`; generator `planning/make_bella_ciao_xm_microbit.py`.
- Traditional Italian folk song: only the traditional melody, no lyrics, no modern arrangement.
- Melody checked against 8notes.com's violin MIDI (fetched once through the built-in browser): the 8-bar verse
  matches note for note and every note is on the eighth-note grid, so nothing is rounded.
- Moved to A minor so the Hoover's two pitches (A, E) are the key note and its fifth. Lead E5-F6 (loud on the
  speaker). Chords per half bar: Am x7, A7 | A7, Dm, Dm, Am, Am, E7, E7, Am.
- Same setup and the same 10 instruments, byte for byte. Pattern names and the 64-slot song order follow
  Korobeiniki's; B1/B2 are the "bella ciao, bella ciao, bella ciao ciao ciao" hook chopped and looped.
- **Synthwave version** (`mods/bella_ciao_synthwave_4ch_microbit.xm`, generator
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
  `mods/ode_to_joy_synthwave_v3_4ch_microbit.xm` (generator `make_ode_to_joy_synthwave_v3_xm_microbit.py`).
- How we got there:
  Three versions (removed from `mods` 4 Nov; in git history): `ode_to_joy_trance_4ch_microbit.xm`,
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
- Sounds: one function per sound (`play_kick` ...), recipes from the old `Claude/code/microbit_instruments.py` (removed; in git history).
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

### Song 4: Midnight Diner (4 Nov 23:30, draft: `planning/mods/midnight_diner.xm`, to listen to)
- The Midnight Diner opening theme "Omoide" (Tsunekichi Suzuki) is his reworking of the Irish air "Pretty Girl /
  Pretty Maid Milking Her Cow" ("Cailín Deas Crúite na mBó", 18th century, public domain; JASRAC lists the song
  as based on an Irish folk song). We use **only the traditional melody**; Suzuki's lyrics and arrangement are
  his. (Earlier, on 1 Nov, Omoide was ruled out as copyrighted: the traditional air is the way round that.)
- Melody: Ed Wosik's ABC transcription ("Pretty Maid Milking Her Cow", folktunefinder.com tune 17902), a waltz
  in E minor, A and B parts of 16 bars, a D-E-F# pick-up; played an octave up (D5-F#6). Two bars in the ABC were
  a beat short (A7 "E4D", B9 "d2 Bcd"): filled as E4 D2 and d2 B c d2. **Russell to check by ear against the
  Omoide opening.**
- "Start traditional, add drums, speed up until it's techno": a waltz bar is squeezed into our bar as 3 + 3 + 2
  rows (beats on rows 0, 3, 6); the slow sections use 16-row bars (6 + 6 + 4).
  INT (arpeggio + bass, the pick-up), S1 (the tune, no drums), S2 (soft kick), S3 (+ hats), S4 (+ claps, tom
  pick-up) = the first 8 bars, slow; BU = full-speed build ending on the pick-up alone; A1-A4, B1-B4 = the whole
  A and B parts at full speed, four-on-the-floor; BR = breakdown, no drums; OUT = slow again, fading.
  Order: INT S1-S4 BU AA BB | BR S1 S2 BU A B A | BR S3 S4 BU AA BB | A S4 OUT (64 slots, 6.8 min).
- Chords (E minor) per bar: A = Em D D D G D Em Em Em D Em G C D Em Em; B = G G Em D C Bm Em Em G C D Em C D Em Em.
- 8 tracks: 1 melody, 2 bass (3+3+2 in the drops), 3 a guitar-like arpeggio (slow) / claps, pings and Hoover
  stabs (drops), 4 drums; 5-8 the usual drums-and-bass extras (add_8ch_extras.py, song "diner"), almost silent
  in the traditional opening (about 2 sounds a pattern), growing through S2-S4, full in the drops.
- Checked: the melody is the ABC note for note in every pattern; tones in range; no semitone rubs anywhere
  (tracks 2 and 3 pick another chord note if one would rub); no drum doubled; same 10 instruments; every extra
  pattern has sound; the pick-up into each drop plays alone.
- **First try rejected (4 Nov 23:31):** "not identifiable as the theme, too similar to the other tunes with the
  beepy backing; it needs to start slow, a single sound (shame it can't be a guitar), then gradually move to
  techno". Likely causes: the 3+3+2 squeeze bent the waltz rhythm; the usual backing from bar 1.
- **New plan:** keep it a **waltz all the way** - patterns don't have to line up with bars (12-row slow bars or
  6-row fast bars run on across patterns: 3 patterns = 8 slow or 16 fast bars). Open with the melody **alone**,
  plucked (notes cut about half way, like a picked string); then a bass note per bar; a soft kick on 1; the tune
  at double speed (same notes and rhythm); then **techno in 3** (a kick on every beat, hats between, claps), and
  the full 8 tracks. Boards 2-8 stay silent in the solo opening (on purpose here). The song may be shorter than
  64 patterns (about 4 minutes).
- **Step 1 now:** `planning/mods/midnight_diner.xm` is a **melody-only test** (replaced the first try): the A and B parts
  then A again, slow (one eighth = 2 rows), a straight waltz, plucked, nothing else; 12 patterns, 18 in the order,
  about 2 minutes; no pick-up at the start. If the melody isn't recognisably Omoide, the transcription is the
  wrong version and needs another source.
- **"It's 3/4... this isn't going to work, is it?"** Options: (1) techno in 3, (2) stretch each bar into 4/4
  (4+2+2), (3) a different tune. Russell: "3 is probably the right answer but let's try 3/4 techno (option 1)".
- **Second try, waltz techno in 3** (4 Nov 23:40, `planning/mods/midnight_diner.xm`, to listen to): a waltz throughout,
  bars running on across patterns (slow 12-row bars, fast 6-row bars; 3 patterns = 8 slow / 16 fast bars):
  SO1-3 solo (the first 8 bars, slow, melody alone, plucked); JN1-3 joining (the next 8 bars, slow: + a held bass
  note each bar, a soft kick on 1 from bar 4, a hat from bar 6); WT1-3 waltz techno (the A part fast: kick on 1,
  "oom-pah-pah" stabs on beats 2 and 3, hats; the extras begin small); FB1-3 full techno in 3 (the B part: a kick
  on every beat, the bass pumping every row, a clap on beat 3, Hoover hits, all 8 tracks); FA1-3 the same with
  the A part and a roll at the end; OUT the last two bars slow and alone.
  Order: SO JN WT FB FA FB FA | SO WT FB FA | OUT = 34 patterns, 3.6 minutes.
  Bar 11's half-eighth F#-E turn is one F# at full speed. Tones held over a pattern boundary are struck again
  at row 0 (the micro:bit stops all sound at a pattern's end); the plucked lead just stops.
  Checked: the melody is the ABC note for note in every section; in range; no semitone rubs between any of the
  8 tracks; no drum doubled; the same 10 instruments; the solo really is the melody alone.
  Boards 2-8 are silent in the solo (on purpose, agreed), and 3-8 mostly in the joining section.
- **Third try, melody and beats** (4 Nov 23:45, `planning/mods/midnight_diner.xm`): "3/4 techno is cool! But I don't like
  the extra notes/tones, counterpoint to chords - stick to single melody plus drums, maybe a little chords".
  Now the only tones are the melody (track 1) and **one bass note a bar** (track 2); a **Hoover hit every 4 bars**
  in the full techno is the "little chord". Everything else is drums: waltz techno = kick on 1, "oom-pah-pah" on
  claps (beats 2 and 3), hats; full techno = a kick on every beat, snare on 2, clap on 3, hats; tracks 5-8 = toms,
  hats and snare, more toms, crashes and extra kicks. Checked: no rubs, no doubled drums, cells ok.
- **Fourth try, two basses** (4 Nov 23:50, `planning/mods/midnight_diner.xm`, to listen to): "bass I like - bass melody
  plus drums", then "maybe double bass - two types - as my micro:bits will struggle with bass: melody, bass
  rumble, bass notes, plus drums". Track 2 = **bass notes**, a smooth line (the chord's root on beats 1-2, its
  fifth on beat 3, no gaps; the whole bar in waltz techno). Track 5 = **bass rumble**, the same note low down,
  rolling between two octaves on every row in full techno, short notes on "pah pah" in waltz techno (its toms
  moved to track 7). Melody, bass notes, kick and hats unchanged. Checked: no rubs, no doubled drums, cells ok.
- **Fifth try, theme speed then the drop** (4 Nov 23:55, `planning/mods/midnight_diner.xm`, to listen to): "trying to start
  slow and speed up doesn't work - start at the normal theme tune speed, then ramp up some drums and drop into
  double time". The first half stays at **theme speed** (a 3/4 bar every 12 rows = 2.4 s, about 75 beats a
  minute): A alone (SO), A with the bass (JN), then B with the **drums building** (BU, 6 patterns, 4 bars a
  stage: kick; + claps and rumble; + hats and toms; + a snare roll getting faster, then 2 rows of silence).
  Then the **drop into double time** (6-row bars): FA FB FA FB FA, then the slow ending. The fast waltz section
  (WT) is gone. Order: SO JN BU FA FB FA FB FA OUT = 28 patterns, 3.0 minutes; 19 patterns in the file.
  Checked: no rubs, no doubled drums, cells ok.
- **Sixth try, less twiddly** (4 Nov 23:59, `planning/mods/midnight_diner.xm`, to listen to): "too much twiddly backing
  melody - makes it sound too similar to our previous tunes". In double time the rumble no longer rolls between
  octaves: it plays the bass's own note, low, as a short pulse on each beat with the kick (two boards on one note
  = a louder bass). The bass notes' fifth on beat 3 now goes below the root when it fits, so both basses stay in
  the bottom octave (nothing above B-4). Melody, drums and the build-up unchanged. Checked: no rubs, no doubled
  drums, cells ok.

### Song 5: Bella Ciao, Latin techno (5 Nov 00:40) - dropped 5 Nov 00:45
- Russell: "Bella Ciao techno - but all Latin and not with the same techniques as the previous songs - still
  techno but needs to not just sound the same with a different melody". (Tried for song 3 as chiptune techno -
  too like Korobeiniki - and synthwave - the melody felt weak; see above.)
- Melody: the verse as checked for song 3 (8notes.com's violin MIDI, A minor, git `bb97906`); traditional, no lyrics.
- **Left out on purpose:** four-on-the-floor outside the drops, offbeat hats, the acid octave pump, the Hoover,
  pews, arpeggios, the snare-roll-and-silence build.
- **Latin instead:** the 3-2 son **clave** on claps (track 3; track 8 while track 3 plays horns); a **tumbao**
  bass (nothing on beat 1, the fifth on the "and" of 2, the next chord's root on beat 4 held over the bar line;
  track 2, track 5 doubles the hits); **congas** on toms (track 4) and **bongos** (track 7); the **cascara**
  (timbale-shell rhythm) on hats (track 6); **horns** - the hook a third below the tune (track 3); **coro**:
  call and response, the hook jumps from track 1 to track 3; a **descarga** percussion break with the horns'
  mambo stabs, ending in a timbale roll (abanico) into the drop; timbale "cha" and tom runs on track 8.
- Sections: INT1-2 percussion builds up (clave, congas, cascara, bass, bongos) | VA1-2 verse, no kick |
  VB1-2 verse, kick on 1 and 3, horns on the hook | D1-2 the drop: the verse, four on the floor | HK1 the hook,
  call and response | BR1-2 descarga | OUT1 the hook and a last hit.
  Order: INT VA VB D D HK HK VA BR D D HK HK OUT = 23 patterns, 2.5 minutes; 12 patterns in the file.
- Checked: no rubs, no doubled drums, tones in range, cells ok.
- **Second try, the tune from the start** (5 Nov 00:40): "when it gets going it's cool, but to start with I
  didn't recognise the theme - make the intro very clearly the Bella Ciao melody". INT1-2 now play the verse's
  first 4 bars ("una mattina... o bella ciao, bella ciao, bella ciao ciao ciao") twice: first over only the
  clave, then with congas, cascara, the tumbao bass and bongos coming in under it. Rest unchanged. Checked again.
- **Third try, half speed first** (5 Nov 00:45): "start at half speed for a few patterns, then double speed once we
  get going". The intro (now INT1-4) is the same music stretched to half speed (every row becomes two: tune,
  clave, congas, bass), ending in a full-speed snare roll into double time; it then goes straight to VB (the
  verse with a kick). Order: INT1-4 VB D D HK HK VA BR D D HK HK OUT = 23 patterns, 2.5 minutes; 14 patterns in
  the file. Checked again.
- **Dropped** (5 Nov 00:45): "that doesn't work as techno - reverse ferret and abandon all that"; Russell chose to
  drop Bella Ciao entirely, not just the half-speed intro. (Liked on the way: the Latin drops "when it gets going
  it's cool".) The draft was never committed; Claude's generator was in the session scratchpad only. Bella Ciao has
  now been tried three ways (chiptune techno, synthwave, Latin techno).

### No template (4 Nov 22:00)
- No separate template program or template `.xm`: the song programs share identical tracker code, so **any song
  program is the template** (swap in different patterns = a new tune), and **any song's `.xm` is the template
  `.xm`** (copy it: it already has the 10 instruments, speed 12 / tempo 150, 32-row patterns, 8 channels).
- So the XM converter can take any song program as its base.

### 8-track Canon and Ode to Joy (4 Nov 21:55, in `planning/`, to test)
- Same idea as the 8-track Korobeiniki: **tracks 1-4 byte for byte as before** (4 boards sound exactly the
  same), tracks 5-8 only add **drums and bass**: 5 a second bass line (root / fifth / octave, short notes),
  6 hats and snare, 7 toms and claps, 8 crashes, extra kicks, open hats, pews. Every extra board plays in every
  pattern, starting small and growing towards the drops.
- In each song's style: the Canon's drops get the straight drive (offbeat octave bass, snare on 2 and 4);
  Ode to Joy's drops follow its half-time 3+3+2 (bass an octave above the kick, snare on the backbeat, a kick
  pick-up into each bar). Fills on the Canon's D2/D2x and Ode's tom-cascade drops (D4, KA2).
- The extras stay silent where the tune goes quiet: the beat before the Canon's drops (BU2, RLD), Ode's
  half-bar stop in D2 (only the melody carries on) and the silent beat after its build.
- Made by `add_8ch_extras.py` (scratch, not in the project): reads the 4-channel .xm, copies channels 1-4 and the
  instruments, adds 5-8 from a short description of each song (sections, chords per half bar, quiet rows).
- Checked: tracks 1-4 and the instruments identical to the 4-channel files; no semitone clashes; no drum doubled
  on a row; tones C-4..B-6; no extras in the quiet rows; every extra pattern has sound; the programs' tracks
  0-4 = the 4-track programs, tracks 5-8 = the new .xm, the same sounds per track as the .xm.
- **To test:** listen in OpenMPT (and with 5-8 muted = as before), then on 8 boards + a conductor.

### One program per song (4 Nov 17:40, in `planning/`, to test)
- Why: MakeCode was too slow on student laptops with all three songs (256 arrays, about 8,000 blocks).
- **Three programs, named after the song:** `techno-bit/korobeiniki.py`, `canon.py`, `ode_to_joy.py`, with
  `mods/<song>.xm` and `hex/<song>.hex`. No `main.py` (MakeCode still calls its file main.py inside a project).
- **Generic names:** `track1_p00` ... `track8_p15` (one pattern of one track), `track1_patterns` ... (a track's
  list; `track0_patterns` = the metronome), `song_tracks[track][pattern]`, `song` (the order list), functions
  `create_track1_patterns()` ..., `create_patterns()`, `create_song()`. Each song's patterns are numbered 0-15.
- **No song screen:** A = next track (1-8), logo = conductor (0), B = play the song (conductor: broadcasts;
  other tracks: plays that track alone), B again = stop; boards following the conductor join by themselves.
- **Tracker code identical in all three**, made by a script from the tested `techno-bit/main.py` (its arrays
  taken from running it), so nothing can drift. The only code changes: `show_song_name` gone, and the song
  choice taken out of the A button, the logo, `on_forever` (B) and `on_forever2`.
- Checked on the mock micro:bit: each program's arrays and song order = the live program's exactly; the same
  sounds on every track 0-8; tracks 5-8 of the 4-track songs share tracks 1-4's arrays; no variable problems;
  the radio scenarios (lost numbers, lost "end song", B mid-song) behave as before.
- **To test:** each in MakeCode on a student laptop (Blocks speed: Korobeiniki is the biggest, about 4,000
  blocks), then on the boards: 4 boards and 8 boards + a conductor, B on a track plays that track alone.

### One song per project + XM converter (4 Nov: first attempt; the converter part is for later - files in git at `f50c8f5`)
- MakeCode got very slow with 3 songs (256 arrays, ~8,000 blocks). Arrays stay (students see them in Blocks),
  so: **one MakeCode project per song**, flashing the boards to change song. **Shared tracker code**: every
  song project is the same base program with different arrays.
- **Base** = `planning/main.py` (to become the root `main.py`): the live code with only Tetris
  (Korobeiniki, 8 tracks). The song screen is gone: A = next track, logo = conductor, **B = play the song**
  (B again = stop; on a board following the conductor, B = back to the track screen). Everything else
  (radio, no "start song", waiting row, band 24, LEDs, sounds) is unchanged. No song symbols (one song a hex).
  Arrays are numbered: `lead_00` ... `lead_15`, `acid_00` ..., tracks `lead acid vox drums bass2 kit2 perc
  hits`; `song` is the order list; `song_tracks[track][pattern]`. 98 KB instead of 195 KB.
- The song lives only in `create_<track>_patterns()`, `create_patterns()`, `create_song()` and their
  declarations; the converter replaces exactly those (found by name, so MakeCode's re-ordering doesn't matter).
- **Converter** = `planning/tools/xm_to_makecode.py` (Python script, decided 4 Nov: simple, and students can
  read it): `python xm_to_makecode.py tune.xm --base main.py --out tune_main.py`. Checks the tune follows the
  rules (4 or 8 channels, 32 rows, instruments 1-10, C-4..B-6, tom/pew/hoover pitches, no volume/effects,
  speed 12 / tempo 150, size) and reports problems by pattern / row / channel. 4 channels: tracks 5-8 play
  tracks 1-4.
- Checked: Tetris in the base = the live Korobeiniki arrays and order exactly; converting the Canon and Ode to
  Joy XMs reproduces the live arrays and orders exactly; Tetris -> Canon -> Tetris gives the identical file;
  all three play the same sounds per track as their XMs; no variable problems; radio scenarios (lost numbers,
  lost "end song", B mid-song) behave as in the live code.
- **Documentation first** (asked 4 Nov): `planning/xm_converter.md` - the rules for a tune, how the
  converter is run and used, what it writes, the changes it asks of the draft converter, open questions.
  The code above is a draft until that document is agreed. Decided: song programs live in **`mods/` in the
  project root** (mirrored in `planning/mods`): each `.xm` with its converted `<name>_main.py` next to it; the root
  `main.py` is the base (Tetris); the converter and `template.xm` in **`tools/`** (decided 4 Nov): `python tools/xm_to_makecode.py mods/my_tune.xm`.
  Anyone can run anything (it's all GitHub), but **nobody should be blocked by Python**: two ways to make a
  tune - edit the arrays in Blocks (no tools), or OpenMPT + converter; a **converter web page** (drop in an
  `.xm`, copy the Python out) is planned after the Python converter works.
- Next: agree `xm_converter.md`; then step 2 the template XM (4/8 channels, the 10 instruments, 32 rows, speed 12 / tempo 150); then docs
  (README controls without the song screen, format doc: one song per project, the converter).

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
- [ ] **Listen to the 8-track Canon and Ode to Joy** (`planning/techno-bit/mods/*.xm`) in OpenMPT.
- [ ] **Test the one-program-per-song split** (in `planning/`, all three now 8 tracks): MakeCode speed on a student laptop, then the
      boards (4, 8 + a conductor, B on one track). Then promote, make the three MakeCode projects and hexes.
- [ ] **XM converter and rules doc** (no template needed: any song is one) - after the split (draft in git at `f50c8f5`, needs the new
      names). Later: a web page converter.
- [ ] **Later: compile on the PC** (4 Nov). MakeCode is the focus of this project, so this waits. The old
      `microbit/` folder turned out to be "microbitstubs" (MicroPython auto-complete placeholders for VS Code,
      2019): they can't build MakeCode Python, so they were deleted (in git history, with Russell's original VS
      Code instructions). A real local build would use MakeCode's own command-line compiler (`pxt`, via Node.js).
- [x] **README decisions** (4 Nov): the VS Code section was moved, then deleted with the stubs; the wrong
      converter sentence went in the AI-use rewrite.
- [x] **Fresh hex** (4 Nov 14:11), measured: about 45 KB free.
- [ ] **Sounds and balance** on the real speakers: note any sound that is too quiet, too loud or wrong.
      The acid bass (around 440 Hz) is likely to be the quietest part.
- [ ] **First-beat lateness**: only if it can be heard.
- [x] **`main_no_start_song.py`** tested on the boards ("more resilient") and promoted to `main.py` with the
      README (4 Nov 14:15). Fresh hex downloaded.
- [x] **Format doc promoted** (4 Nov 17:10, the newest version with "The radio messages").
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
- Tidied (1 Nov): only the files in use are at the top of `planning/` and what was `Claude/mods`; earlier
  steps and tries moved to `old/` (the `old` folders were deleted on 4 Nov: they are in git history).
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
