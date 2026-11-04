# Techno:bit

Messing about with Micro:bits https://microbit.org/ to make tracker music, like back in the good old Amiga days. But with each Micro:bit playing a single track, and a conductor broadcasting radio signals to play patterns.

Plus I think it makes a cool demo to show the students at our local coding club what you can do with a few cheap Micro:bits. (and so I've got a good tune to demo with I'm enlisting some help from an AI to create a track to test this with that I can use to demo - I'll be creative after I've inspired them :smile: )

The python saved here is taken from the Makecode project https://makecode.microbit.org/S26000-11508-29408-02742 which I'm making in blocks so anyone can understand it. I'm just putting it here in GitHub for version control. OK it turns out that the Makecode site does that... kinda - I trust this more. Plus I can document and have multiple block projects collected here if I want. 

## What it is

- **Several BBC micro:bit V2s play one tune together.** Each micro:bit plays one track (the melody, the bass, a voice lane, the drums ...) through its built-in speaker, and lights up an LED for every note or drum it plays.
- **A conductor micro:bit keeps them together.** It broadcasts which pattern to play by radio, and plays a metronome.
- **Up to 9 micro:bits:** a conductor plus 4 tracks for the whole tune, plus 4 more tracks of extra drums and bass.
- **Three tunes so far:** Korobeiniki (the Tetris tune, 8 tracks), Pachelbel's Canon in D and Beethoven's Ode to Joy (4 tracks each). All out of copyright. Each tune is its own program (`korobeiniki.py` and so on), with the same tracker code: flash all the micro:bits with the tune you want.
- **It's written in MakeCode Blocks**, so students can see and change everything, including the music: every pattern of every track is an array you can edit.

## Demo


https://github.com/user-attachments/assets/debd2a19-0f8b-4f12-831e-922c98faf1f4

(The video file itself is in [techno-bit/media/technobit-demo.mp4](techno-bit/media/technobit-demo.mp4).)


## How it works (the techie bit)

- **The music is a tracker tune.** The tunes are written in a tracker ([OpenMPT](https://openmpt.org/)) as `.xm` files, then copied into the program as arrays: one array per pattern per track, one entry per row. A row lasts 200 ms (150 BPM) and a pattern is 32 rows (4 bars). Each entry is `tone D-6` (a note), `wave kick` (one of 12 drum and effect sounds), `x` (silence) or `-` (carry on). An order list says which pattern plays next. All the details are in [the tracker format](techno-bit/docs/tracker_format.md).
- **Sounds:** notes come from a name-to-frequency lookup table (C-4 to B-6: the speaker can't do much lower). The drums and effects (kick, snare, clap, hats, crash, toms, pews, Hoover stabs) are MakeCode sound expressions.
- **Timing:** each row waits until 200 ms have passed on the clock since the row started, so the code's own speed doesn't make the beat drift.
- **Radio:** the conductor sends each pattern's number as it starts. A number always interrupts whatever a board is playing, so every board starts the pattern together, a few milliseconds behind the conductor, with no gap. There are only three messages: a pattern number, `end song` and `stop`. A board that misses a number drops out for one pattern, and its top row glows dimly while it waits. Radio group 23, frequency band 24 (2424 MHz, between the busy Wi-Fi channels).
- **LEDs:** one LED per note (not octave) or sound, with related sounds sharing an LED at different brightness; the top row shows the track.
- **Blocks-friendly Python:** the code is kept to things MakeCode can show as real blocks (no hidden Python helpers), so the Python in GitHub and the Blocks in MakeCode are the same program.
- **One program per tune:** all three tunes in one program filled a good part of the micro:bit V2's 512 KB flash, and made MakeCode crawl on student laptops (about 8,000 blocks). So each tune is its own program: the tracker code is identical, only the arrays (`track1_p00` ...) and the order list (`song`) change.

## Try it

Everything you need is in **[techno-bit/](techno-bit/)**: [techno-bit/README.md](techno-bit/README.md) explains how to get it onto the micro:bits, the controls, and the tunes.

## How this project is organised

| Folder | What it is |
|---|---|
| **[techno-bit/](techno-bit/)** | **The Techno:bit itself: start here.** The program, the tunes, ready-to-flash files, and the documentation for using it and making your own tunes: see [techno-bit/README.md](techno-bit/README.md). |
| [planning/](planning/) | Where the project is planned. `planning/claude/` is where I work with Claude (an AI assistant): notes, and suggested changes that haven't made it into `techno-bit/` yet. |

The original MakeCode project (all three tunes in one) is https://makecode.microbit.org/S26000-11508-29408-02742.


## AI use

I started this to learn and to have a cool demo for the coding club, and I'm still using it to learn. But AI has become a big part of how it's built, so here's who does what.

**Me:** the idea and the design, the original program in MakeCode Blocks, deciding what goes in (and what doesn't), testing everything on the real micro:bits (all nine of them), and checking that I understand the code well enough to explain it to students. Nothing goes into `techno-bit/` until I've agreed to it.

**Gemini** helped me investigate the timings for the sounds, radio, LEDs and so on, with examples of MakeCode Blocks I could use.

**Claude** (an AI assistant from Anthropic, in the Claude app with access to this project) now writes a lot of the code and the music, and helps run the project:
- **Music:** arranged the three tunes (old, out-of-copyright melodies) as techno `.xm` files, including the 8-track Korobeiniki, and turned them into the program's arrays.
- **Code:** converted my program to the tracker format, wrote the 12 sound functions, and designed and tested the radio changes that keep the boards together (patterns that interrupt, no "start song", the B button fix, the dim waiting light).
- **Testing before the hardware:** checks its code on simulated micro:bits, including simulated radio with lost messages, before I try it on the real ones.
- **Documentation and organisation:** wrote most of the docs, keeps the planning notes in `planning/claude`, and helped set up this folder structure.
- **Other bits:** measured how much memory is left, shrank the demo video, and drafted a converter that turns an `.xm` tune into a program (paused for now).

Claude's suggestions go into `planning/claude/suggestions/` first, and we promote them to `techno-bit/` together. The aim is still the same: get a cool tune playing quickly, then let students explore changing both the code and the music.
