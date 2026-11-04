# Techno:bit

Messing about with Micro:bits https://microbit.org/ to make tracker music, like back in the good old Amiga days. But with each Micro:bit playing a single track, and a conductor broadcasting radio signals to play patterns.

## Demo

https://github.com/user-attachments/assets/debd2a19-0f8b-4f12-831e-922c98faf1f4

(The video file is [media/technobit-demo.mp4](media/technobit-demo.mp4).)

## What it is

- **Several BBC micro:bit V2s play one tune together.** Each micro:bit plays one track (the melody, the bass, a voice lane, the drums ...) through its built-in speaker, and lights up an LED for every note or drum it plays.
- **A conductor micro:bit keeps them together.** It broadcasts which pattern to play by radio, and plays a metronome.
- **Up to 9 micro:bits:** a conductor plus 4 tracks for the whole tune, plus 4 more tracks of extra drums and bass. Every tune works with 4 players or 8.
- **Three tunes so far:** Korobeiniki (the Tetris tune), Pachelbel's Canon in D and Beethoven's Ode to Joy, all with 8 tracks. All out of copyright. Each tune is its own program (`korobeiniki.py` and so on), with the same tracker code: flash all the micro:bits with the tune you want.
- **It's written in MakeCode Blocks**, so students can see and change everything, including the music: every pattern of every track is an array you can edit.

## The tunes

| Tune | Ready to flash | MakeCode project | The tune (.xm) |
|---|---|---|---|
| Korobeiniki (the Tetris tune), techno | [hex/korobeiniki.hex](hex/korobeiniki.hex) | https://makecode.microbit.org/S54592-76373-74001-91871 | [mods/korobeiniki.xm](mods/korobeiniki.xm) |
| Pachelbel's Canon in D (about 1700), bhangra techno | [hex/canon.hex](hex/canon.hex) | https://makecode.microbit.org/S16435-66036-39782-77562 | [mods/canon.xm](mods/canon.xm) |
| Beethoven's Ode to Joy (1824), drum-heavy synthwave with a key change | [hex/ode_to_joy.hex](hex/ode_to_joy.hex) | https://makecode.microbit.org/S92579-43021-82836-81182 | [mods/ode_to_joy.xm](mods/ode_to_joy.xm) |

All three have 8 tracks: the first 4 are the whole tune, the other 4 add drums and bass. The melodies are all out of copyright.

## Getting a tune onto the micro:bits

Pick a tune. Every micro:bit, the conductor included, needs the same tune: to play a different one, flash them all again.

- **Quickest:** plug in a micro:bit and copy the tune's `.hex` file (for example `hex/canon.hex`) onto the MICROBIT drive. Do this for every micro:bit.
- **To see and change the code:** open the tune's MakeCode project (in the table above), click **Edit Code** to make your own copy, then download it and flash every micro:bit.
- **Or start from the Python file:** in [MakeCode](https://makecode.microbit.org/), start a new project, switch to Python, paste in the tune's program (for example `canon.py`; MakeCode will still call it `main.py`), then switch back to Blocks. Download it and flash every micro:bit.

## How to play

| On a micro:bit | What it does |
|---|---|
| **A** | Picks the track this micro:bit plays (the display shows the number): **1** melody, **2** bass, **3** voice lane (tone phrases, claps, crashes, toms, pews, Hoover stabs), **4** drums, **5-8** extras: a second bass line (5), hats and snare (6), toms and claps (7), crashes, extra kicks and pews (8) |
| **Logo** (touch it) | Makes this micro:bit the **conductor**: the display shows **0** |
| **B** on the conductor | Plays the tune, and tells all the other micro:bits to join in by radio, while the conductor plays a metronome |
| **B** on any other track | Plays just that track on its own (good for practising one part) |
| **B** while playing | Stops |

**To play the whole tune together:** give each player micro:bit a different track with A (1 to 4 is the whole tune; 5 to 8 add more drums and bass), make one more the conductor with the logo, and press B on the conductor. The players only need to be showing their track number: they join in by themselves and go back to their track number at the end. So 5 micro:bits play the whole tune, and 9 play all 8 tracks.

**The lights:** each player lights an LED for every note (not its octave) or drum it plays, with related sounds sharing an LED. The top row shows the track: tracks 0 to 4 light one LED each, and tracks 5 to 8 light their partner track's LED at half brightness. If the rest of a player's top row glows dimly, it has missed a radio message: it carries on with the next pattern, or press its B button to bring it back. The full LED tables are in [the tracker format](docs/tracker_format.md).

**The radio:** every micro:bit uses radio group 23 and frequency band 24 (2424 MHz), picked to sit between the busy Wi-Fi channels. If boards drop out in a room full of Wi-Fi, Bluetooth and game controllers, try moving them closer together.

## What's in this project

| | What it is |
|---|---|
| `korobeiniki.py`, `canon.py`, `ode_to_joy.py` | The Techno:bit program, one per tune: the code is the same in all three, only the tune's arrays are different |
| [hex/](hex/) | The same programs, ready to flash |
| [mods/](mods/) | The tunes as `.xm` files: open them in a tracker such as [OpenMPT](https://openmpt.org/) and change them |
| [docs/](docs/) | [The tracker format](docs/tracker_format.md): how the music is stored (`tone D-6`, `wave kick`, `x`, `-`) and how the micro:bit plays it |
| [media/](media/) | The demo video |
| [planning/](planning/) | Behind the scenes: how I plan the project with Claude (an AI assistant). Not needed to play |

## How it works (the techie bit)

- **The music is a tracker tune.** The tunes are written in a tracker ([OpenMPT](https://openmpt.org/)) as `.xm` files, then copied into the program as arrays: one array per pattern per track, one entry per row. A row lasts 200 ms (150 BPM) and a pattern is 32 rows (4 bars). Each entry is `tone D-6` (a note), `wave kick` (one of 12 drum and effect sounds), `x` (silence) or `-` (carry on). An order list says which pattern plays next. All the details are in [the tracker format](docs/tracker_format.md).
- **Sounds:** notes come from a name-to-frequency lookup table (C-4 to B-6: the speaker can't do much lower). The drums and effects (kick, snare, clap, hats, crash, toms, pews, Hoover stabs) are MakeCode sound expressions.
- **Timing:** each row waits until 200 ms have passed on the clock since the row started, so the code's own speed doesn't make the beat drift.
- **Radio:** the conductor sends each pattern's number as it starts. A number always interrupts whatever a board is playing, so every board starts the pattern together, a few milliseconds behind the conductor, with no gap. There are only three messages: a pattern number, `end song` and `stop`. A board that misses a number drops out for one pattern, and its top row glows dimly while it waits. Radio group 23, frequency band 24 (2424 MHz, between the busy Wi-Fi channels).
- **LEDs:** one LED per note (not octave) or sound, with related sounds sharing an LED at different brightness; the top row shows the track.
- **Blocks-friendly Python:** the code is kept to things MakeCode can show as real blocks (no hidden Python helpers), so the Python in GitHub and the Blocks in MakeCode are the same program.
- **One program per tune:** all three tunes in one program filled a good part of the micro:bit V2's 512 KB flash, and made MakeCode crawl on student laptops (about 8,000 blocks). So each tune is its own program: the tracker code is identical, only the arrays (`track1_p00` ...) and the order list (`song`) change.

## About this project

Plus I think it makes a cool demo to show the students at our local coding club what you can do with a few cheap Micro:bits. (and so I've got a good tune to demo with I'm enlisting some help from an AI to create a track to test this with that I can use to demo - I'll be creative after I've inspired them :smile: )

The python saved here is taken from the Makecode projects (one per tune: see "The tunes" above) which I'm making in blocks so anyone can understand it. I'm just putting it here in GitHub for version control. OK it turns out that the Makecode site does that... kinda - I trust this more. Plus I can document and have multiple block projects collected here if I want. 

(The original MakeCode project, with all three tunes in one, was https://makecode.microbit.org/S26000-11508-29408-02742.)

## AI use

I started this to learn and to have a cool demo for the coding club, and I'm still using it to learn. But AI has become a big part of how it's built, so here's who does what.

**Me:** the idea and the design, the original program in MakeCode Blocks, deciding what goes in (and what doesn't), testing everything on the real micro:bits (all nine of them), and checking that I understand the code well enough to explain it to students. Nothing goes into the project until I've agreed to it.

**Gemini** helped me investigate the timings for the sounds, radio, LEDs and so on, with examples of MakeCode Blocks I could use.

**Claude** (an AI assistant from Anthropic, in the Claude app with access to this project) now writes a lot of the code and the music, and helps run the project:
- **Music:** arranged the three tunes (old, out-of-copyright melodies) as techno `.xm` files, including the 8-track Korobeiniki, and turned them into the program's arrays.
- **Code:** converted my program to the tracker format, wrote the 12 sound functions, and designed and tested the radio changes that keep the boards together (patterns that interrupt, no "start song", the B button fix, the dim waiting light).
- **Testing before the hardware:** checks its code on simulated micro:bits, including simulated radio with lost messages, before I try it on the real ones.
- **Documentation and organisation:** wrote most of the docs, keeps our planning notes in `planning/NOTES.md`, and helped set up this folder structure.
- **Other bits:** measured how much memory is left, shrank the demo video, and drafted a converter that turns an `.xm` tune into a program (paused for now).

Claude's suggestions go into `planning/` first, and we move them into the project together. The aim is still the same: get a cool tune playing quickly, then let students explore changing both the code and the music.
