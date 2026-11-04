# Techno:bit: playing and making the tunes

Several micro:bits play a tune together, like a tracker from the old Amiga days: each micro:bit plays one track, and a conductor micro:bit tells them all which pattern to play by radio.

## What's in this folder

| | What it is |
|---|---|
| `korobeiniki.py`, `canon.py`, `ode_to_joy.py` | The Techno:bit program, one per tune. The code is the same in all three: only the tune's arrays are different |
| `hex/` | The same programs, ready to flash: `korobeiniki.hex`, `canon.hex`, `ode_to_joy.hex` |
| `mods/` | The tunes as `.xm` files you can open in a tracker: `korobeiniki.xm`, `canon.xm`, `ode_to_joy.xm` |
| `docs/` | [The tracker format](docs/tracker_format.md): how the music is stored and played |
| `media/` | The demo video |

## Getting it onto the micro:bits

Pick a tune. Every micro:bit, the conductor included, needs the same tune: to play a different one, flash them all again.

- **Quickest:** plug in a micro:bit and copy the tune's `.hex` file (for example `hex/canon.hex`) onto the MICROBIT drive. Do this for every micro:bit.
- **To see and change the code:** in [MakeCode](https://makecode.microbit.org/), start a new project (call it after the tune), switch to Python, paste in the tune's program (for example `canon.py`; MakeCode will still call it `main.py`), then switch back to Blocks and it should all render properly. Download it and flash every micro:bit.

## The tunes and the tracker format

There are three tunes, all arranged for the same 4 channels and the same 10 instruments (Korobeiniki also has 4 extra drum and bass channels for up to 8 Techno:bits). Each has its own program and hex, named after the tune:
- a techno version of the traditional folk tune Korobeiniki (the one behind Tetris): [mods/korobeiniki.xm](mods/korobeiniki.xm) (8 tracks: the first 4 are the whole tune, the other 4 add drums and bass)
- a bhangra techno version of Pachelbel's Canon in D (from about 1700, so out of copyright): [mods/canon.xm](mods/canon.xm)
- a drum-heavy synthwave version of Beethoven's Ode to Joy (1824, also out of copyright), with minor verses, major drops and a key change: [mods/ode_to_joy.xm](mods/ode_to_joy.xm)

You can open the .xm files in a tracker such as [OpenMPT](https://openmpt.org/) and change them.

The music on the Micro:bits is stored in a very simple tracker format, with one row every 200ms (an eighth note at 150 BPM) and 32 rows to a pattern. It is described for students in [docs/tracker_format.md](docs/tracker_format.md): how notes (`tone D-6`), sounds (`wave kick`), silence (`x`) and rests (`-`) are written, and how the Micro:bit plays them.


## Techno:bit controls

### Playing a tune
On startup the Techno:bit shows the current 'track' it's going to play. 

Press the A button to cycle between the tracks. What each track plays depends on the tune, but usually:
- 1 = Lead (the melody)
- 2 = Acid bass
- 3 = Voice lane (a few tone phrases, plus claps, crashes, toms, pews and Hoover stabs)
- 4 = Drums (kick and hats, plus snare and toms in the fills)
- 5 to 8 = Extras, for up to 8 Techno:bits. In Korobeiniki they add a second bass line (5), hats and snare (6), toms and claps (7), and crashes, extra kicks and pews (8). In a 4-track tune (the Canon, Ode to Joy) they double tracks 1 to 4 (5 plays 1, 6 plays 2, 7 plays 3, 8 plays 4), so nobody sits out.

Tracks 1 to 4 play the whole tune on their own; tracks 5 to 8 only add to it.

Press the B button to play the tune on that track (on its own: handy for practising or checking one part).

While playing press the B button to stop playing.

### Conducting via Radio
When in track selection, press the Micro:bit logo to enter Conductor mode. The track number will now show 0.

Now press B: the microbit will broadcast each pattern number of the tune for the other microbits to play on their tracks, while this microbit plays a metronome beat.

So with 5 Techno:bits... one conductor makes the other 4 play the full 4 tracks of the song! And with 9, one conductor makes the other 8 play all 8 tracks.

The other Techno:bits only need to be on their track screen: as soon as one hears a pattern number it joins the song, and it goes back to its track screen when the song ends. If a Techno:bit misses a message it drops out for one pattern and then carries on. If one is ever left waiting (its top row glows dimly), press its B button to bring it back to the track screen.

Radio group 23 and frequency band 24 (2424 MHz) are used, so every Techno:bit needs to be on the same group and band. The band was picked to sit between the busy Wi-Fi channels: if your room has lots of 2.4 GHz wireless (Wi-Fi, Bluetooth, game controllers) and boards drop out, try moving them, or try another band on every board.

### What the lights show
The LEDs show what each Techno:bit is playing: one LED for each note (but not its octave) or sound, with related sounds sharing an LED. The top row shows the track while playing: tracks 0 to 4 light one LED each, and tracks 5 to 8 light their partner track's LED at half brightness. If the rest of the top row glows dimly, that Techno:bit is waiting for the conductor's next pattern number: it has missed one (it will carry on with the next), or the song has ended and it missed the message (press B). The tables are in [the format document](docs/tracker_format.md).
