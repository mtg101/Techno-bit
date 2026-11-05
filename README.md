# Techno:bit

A table full of [BBC micro:bits](https://microbit.org/) playing techno together. Each one plays a single track through its own little speaker, a conductor micro:bit keeps them in time by radio, and together they're a band. Tracker music, like back in the Amiga days, spread across nine tiny computers.

It's for our coding club. Nobody gets excited about arrays, timing and radio messages on their own, but a techno Tetris tune is a different story. And the whole thing, the code and the music, is in MakeCode Blocks, so once students have heard it they can take it apart, change it and make it their own.

## Demo

https://github.com/user-attachments/assets/debd2a19-0f8b-4f12-831e-922c98faf1f4

(The video file is [media/technobit-demo.mp4](media/technobit-demo.mp4).)

## What you need

- **BBC micro:bit V2s** (the V2 has the built-in speaker). 5 play a whole tune: a conductor and 4 players. 9 play everything: a conductor and 8 players. A single micro:bit can also play one track on its own.
- **A computer** to copy a tune onto each micro:bit over USB, or to open the tunes in [MakeCode](https://makecode.microbit.org/).

## The tunes

| Tune | Ready to flash | MakeCode project | The tune (.xm) |
|---|---|---|---|
| Korobeiniki (the Tetris tune), techno | [hex/microbit-TB-Korobeiniki-Tetris.hex](hex/microbit-TB-Korobeiniki-Tetris.hex) | https://makecode.microbit.org/S54592-76373-74001-91871 | [mods/korobeiniki.xm](mods/korobeiniki.xm) |
| Pachelbel's Canon in D (about 1700), bhangra techno | [hex/microbit-TB-canon.hex](hex/microbit-TB-canon.hex) | https://makecode.microbit.org/S16435-66036-39782-77562 | [mods/canon.xm](mods/canon.xm) |
| Beethoven's Ode to Joy (1824), drum-heavy synthwave with a key change | [hex/microbit-TB-ode_to_joy.hex](hex/microbit-TB-ode_to_joy.hex) | https://makecode.microbit.org/S92579-43021-82836-81182 | [mods/ode_to_joy.xm](mods/ode_to_joy.xm) |
| Midnight Diner: "Pretty Maid Milking Her Cow" (Irish, 18th century, the folk tune behind the TV show's theme), waltz techno in 3/4 | [hex/microbit-TB-midnight-diner.hex](hex/microbit-TB-midnight-diner.hex) | https://makecode.microbit.org/S89025-71001-08778-34052 | [mods/midnight_diner.xm](mods/midnight_diner.xm) |
| Manic Miner: Grieg's "In the Hall of the Mountain King" (1875), the tune in the ZX Spectrum game, with a tape-loading intro, half speed, a big build and a double-speed drop | [hex/microbit-TB-Manic-Miner.hex](hex/microbit-TB-Manic-Miner.hex) | https://makecode.microbit.org/S46227-98521-34187-17442 | [mods/manic_miner.xm](mods/manic_miner.xm) |
| The Modern Major-General: Sullivan's "I am the very model of a modern Major-General" (*The Pirates of Penzance*, 1879), patter drum'n'bass | [hex/microbit-TB-Major-General.hex](hex/microbit-TB-Major-General.hex) | https://makecode.microbit.org/S48230-90942-42245-11074 | [mods/major_general.xm](mods/major_general.xm) |

Every tune has 8 tracks: the first 4 are the whole tune, the other 4 add drums and bass. The melodies are all old enough to be out of copyright; the arrangements are new. The Modern Major-General's notes were read from the [Gilbert and Sullivan Archive](https://gsarchive.net/pirates/web_op/pirates13.html)'s MIDI of the song, licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/): thank you.

## Getting a tune onto the micro:bits

Every micro:bit, the conductor included, needs the same tune. To play a different tune, flash them all again.

- **Quickest:** plug in a micro:bit and copy the tune's `.hex` file (from the table above) onto the MICROBIT drive. Do this for every micro:bit.
- **To see and change the code:** open the tune's MakeCode project, click **Edit Code** to make your own copy, then download it and flash every micro:bit.
- **From the Python file:** in [MakeCode](https://makecode.microbit.org/), start a new project, switch to Python and paste in the tune's program (for example `canon.py`; MakeCode will still call it `main.py`), then switch back to Blocks. Download it and flash every micro:bit.

## How to play

| On a micro:bit | What it does |
|---|---|
| **A** | Picks the track this micro:bit plays (the display shows the number). In Korobeiniki: **1** melody, **2** bass, **3** voice lane (tone phrases, claps, crashes, toms, pews, Hoover stabs), **4** drums, **5-8** extras: a second bass line (5), hats and snare (6), toms and claps (7), crashes, extra kicks and pews (8). The other tunes use their tracks in their own way |
| **Logo** (touch it) | Makes this micro:bit the **conductor**: the display shows **0** |
| **B** on the conductor | Plays the tune, and tells all the other micro:bits to join in by radio, while the conductor plays a metronome |
| **B** on any other track | Plays just that track on its own (good for practising one part) |
| **B** while playing | Stops |

**Playing together:** give each player micro:bit a different track with A (1 to 4 is the whole tune; 5 to 8 add more drums and bass), make one more the conductor with the logo, and press B on the conductor. The players only need to be showing their track number: they join in by themselves and go back to their track number at the end.

**The lights:** each player lights an LED for every note (not its octave) or drum it plays, with related sounds sharing an LED. The top row shows the track: tracks 0 to 4 light one LED each, and tracks 5 to 8 light their partner track's LED at half brightness. If the rest of a player's top row glows dimly, it has missed a radio message: it carries on with the next pattern, or press its B button to bring it back. The full LED tables are in [the tracker format](docs/tracker_format.md).

**The radio:** every micro:bit uses radio group 23 and frequency band 24 (2424 MHz), picked to sit between the busy Wi-Fi channels. If boards drop out in a room full of Wi-Fi, Bluetooth and game controllers, try moving them closer together.

## How it works

- **The music is a tracker tune.** Each tune is written in a tracker ([OpenMPT](https://openmpt.org/)) as an `.xm` file, then copied into the program as arrays: one array per pattern per track, one entry per row. A row lasts 200 ms (150 BPM) and a pattern is 32 rows (4 bars of 4/4; Midnight Diner's waltz just lets its bars run on across patterns). Each entry is `tone D-6` (a note), `wave kick` (a drum or effect), `x` (silence) or `-` (carry on). An order list says which pattern plays next. All the details are in [the tracker format](docs/tracker_format.md).
- **Sounds:** notes come from a name-to-frequency lookup table, C-3 to B-6. The speaker can't really play the lowest octave, but a square wave is full of overtones, so you still hear the bass note: every tune's bass (track 2) uses it. The 12 drums and effects (kick, snare, clap, hats, crash, toms, pews, Hoover stabs) are MakeCode sound expressions. A tune can add its own sounds: Manic Miner adds three noise sounds for the screech of a Spectrum tape loading.
- **Timing:** each row waits until 200 ms have passed on the clock since the row started, so the code's own speed doesn't make the beat drift.
- **Radio:** the conductor sends each pattern's number as it starts. A number always interrupts whatever a board is playing, so every board starts the pattern together, a few milliseconds behind the conductor, with no gap. There are only three messages: a pattern number, `end song` and `stop`. A board that misses a number drops out for one pattern, and its top row glows dimly while it waits.
- **One program per tune:** all the tunes in one program filled a good part of the micro:bit V2's 512 KB flash and made MakeCode crawl on student laptops (about 8,000 blocks). So each tune is its own program with the same tracker code; only the arrays (`track1_p00` ...), the order list (`song`) and any extra sounds change.
- **Blocks-friendly Python:** the code sticks to things MakeCode can show as real blocks (no hidden Python helpers), so the Python here and the Blocks in MakeCode are the same program.

## What's in this project

| | What it is |
|---|---|
| `korobeiniki.py`, `canon.py`, `ode_to_joy.py`, `midnight_diner.py`, `manic_miner.py`, `major_general.py` | The Techno:bit program, one per tune |
| [hex/](hex/) | The same programs, ready to flash |
| [mods/](mods/) | The tunes as `.xm` files: open them in a tracker such as [OpenMPT](https://openmpt.org/) and change them |
| [docs/](docs/) | [The tracker format](docs/tracker_format.md): how the music is stored and how the micro:bit plays it |
| [media/](media/) | The demo video |
| [planning/](planning/) | Behind the scenes: how I plan the project with Claude (an AI assistant). Not needed to play |

## About this project

I made Techno:bit as a demo for the students at our local coding club: a way to show what you can do with a few cheap micro:bits. To have something good to demo with, I got help from AI to arrange the tunes. The plan is that once the students are hooked, they make their own.

The programs are written in MakeCode Blocks, one project per tune (see "The tunes" above), so anyone can follow them. The Python files here are copies of those projects, kept in GitHub for version control and so the code, the tunes and the docs live together in one place. (The original MakeCode project, with three tunes in one, was https://makecode.microbit.org/S26000-11508-29408-02742.)

## AI use

I started this to learn and to have a demo for the coding club, and I'm still using it to learn. But AI has become a big part of how it's built, so here's who does what.

**Me:** the idea and the design, the original program in MakeCode Blocks, deciding what goes in (and what doesn't), testing everything on the real micro:bits (all nine of them), and checking that I understand the code well enough to explain it to students. Nothing goes into the project until I've agreed to it.

**Gemini** helped me investigate the timings for the sounds, radio, LEDs and so on, with examples of MakeCode Blocks I could use.

**Claude** (an AI assistant from Anthropic, in the Claude app with access to this project) now writes a lot of the code and the music, and helps run the project:
- **Music:** arranged the six tunes (old, out-of-copyright melodies) as techno `.xm` files and turned them into the programs' arrays.
- **Code:** converted my program to the tracker format, wrote the sound functions, and designed and tested the radio changes that keep the boards together (patterns that interrupt, no "start song", the B button fix, the dim waiting light).
- **Testing before the hardware:** checks its code on simulated micro:bits, including simulated radio with lost messages, before I try it on the real ones.
- **Documentation and organisation:** wrote most of the docs, keeps our planning notes in `planning/NOTES.md`, and helped set up this folder structure.
- **Other bits:** measured how much memory is left, shrank the demo video, and drafted a converter that turns an `.xm` tune into a program (paused for now).

Claude's suggestions go into `planning/` first, and we move them into the project together. The aim is still the same: get a cool tune playing quickly, then let students explore changing both the code and the music.
