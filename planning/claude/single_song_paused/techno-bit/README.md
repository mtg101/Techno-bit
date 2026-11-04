# Techno:bit: playing and making the tunes

Several micro:bits play a tune together, like a tracker from the old Amiga days: each micro:bit plays one track, and a conductor micro:bit tells them all which pattern to play by radio.

## What's in this folder

| | What it is |
|---|---|
| `main.py` | The Techno:bit program, with the Korobeiniki (Tetris) tune. The base for every other tune |
| `mods/` | The tunes: each `.xm` file is a tune you can open in a tracker, with its program next to it |
| `hex/` | Ready-to-flash files, one per tune |
| `docs/` | [The tracker format](docs/tracker_format.md) and [making your own tunes](docs/making_tunes.md) |
| `tools/` | The converter that turns a tune into a program, and the template for new tunes |
| `media/` | The demo video |

## The tunes

Each tune is its own program: the code is the same, only the tune's arrays change. To play a different tune, flash every micro:bit with that tune.

| Tune | The tune (.xm) | Program | Ready to flash | Tracks |
|---|---|---|---|---|
| Korobeiniki (the Tetris tune), techno | [mods/korobeiniki.xm](mods/korobeiniki.xm) | [main.py](main.py) | [hex/korobeiniki.hex](hex/korobeiniki.hex) | 8: the first 4 are the whole tune, the other 4 add drums and bass |
| Pachelbel's Canon in D (about 1700), bhangra techno | [mods/canon.xm](mods/canon.xm) | [mods/canon_main.py](mods/canon_main.py) | [hex/canon.hex](hex/canon.hex) | 4 |
| Beethoven's Ode to Joy (1824), drum-heavy synthwave | [mods/ode_to_joy.xm](mods/ode_to_joy.xm) | [mods/ode_to_joy_main.py](mods/ode_to_joy_main.py) | [hex/ode_to_joy.hex](hex/ode_to_joy.hex) | 4 |

## Getting a tune onto the micro:bits

- **Quickest:** plug in a micro:bit and copy the tune's `.hex` file onto the MICROBIT drive. Do this for every micro:bit.
- **To see and change the code:** in [MakeCode](https://makecode.microbit.org/), start a new project, switch to Python, paste in the tune's program, then switch back to Blocks (it's big: give it a moment). Download it and flash every micro:bit.

Every micro:bit, the conductor included, needs the same tune.

## Making your own tune

Write it in a tracker such as [OpenMPT](https://openmpt.org/), starting from `tools/template.xm`, or change the arrays straight in MakeCode Blocks. The rules and the converter are in [docs/making_tunes.md](docs/making_tunes.md). How the music is stored (`tone D-6`, `wave kick`, `x` and `-`) and how the micro:bit plays it is in [docs/tracker_format.md](docs/tracker_format.md).

## Controls

### Playing a tune
On startup the Techno:bit shows the current 'track' it's going to play. 

Press the A button to cycle between the tracks:
- 1 = Lead (the melody)
- 2 = Acid bass
- 3 = Voice lane (a few tone phrases, plus claps, crashes, toms, pews and Hoover stabs)
- 4 = Drums (kick and hats, plus snare and toms in the fills)
- 5 to 8 = Extras, for up to 8 Techno:bits. In Korobeiniki they add a second bass line (5), hats and snare (6), toms and claps (7), and crashes, extra kicks and pews (8). In a 4-track tune they double tracks 1 to 4 (5 plays 1, 6 plays 2, 7 plays 3, 8 plays 4), so nobody sits out.

Tracks 1 to 4 play the whole tune on their own; tracks 5 to 8 only add to it.

Press the B button to play the tune on that track.

While playing press the B button to stop playing.

### Conducting via Radio
When in track selection, press the Micro:bit logo to enter Conductor mode. The track number will now show 0.

Now press B to play the tune: the microbit will broadcast each pattern number of the tune for the other microbits to play on their tracks, while this microbit plays a metronome beat.

So with 5 Techno:bits... one conductor makes the other 4 play the full 4 tracks of the song! And with 9, one conductor makes the other 8 play all 8 tracks.

The other Techno:bits only need to be on their track screen: as soon as one hears a pattern number it joins the song, and it goes back to its track screen when the song ends. If a Techno:bit misses a message it drops out for one pattern and then carries on. If one is ever left waiting (its top row glows dimly), press its B button to bring it back to the track screen.

Radio group 23 and frequency band 24 (2424 MHz) are used, so every Techno:bit needs to be on the same group and band. The band was picked to sit between the busy Wi-Fi channels: if your room has lots of 2.4 GHz wireless (Wi-Fi, Bluetooth, game controllers) and boards drop out, try moving them, or try another band on every board.

### What the lights show
The LEDs show what each Techno:bit is playing: one LED for each note (but not its octave) or sound, with related sounds sharing an LED. The top row shows the track while playing: tracks 0 to 4 light one LED each, and tracks 5 to 8 light their partner track's LED at half brightness. If the rest of the top row glows dimly, that Techno:bit is waiting for the conductor's next pattern number: it has missed one (it will carry on with the next), or the song has ended and it missed the message (press B). The tables are in [the format document](docs/tracker_format.md).
