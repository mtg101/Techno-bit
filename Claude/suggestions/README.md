Messing about with Micro:bits https://microbit.org/ to make tracker music, like back in the good old Amiga days. But with each Micro:bit playing a single track, and a conductor broadcasting radio signals to play patterns.

Plus I think it makes a cool demo to show the students at our local coding club what you can do with a few cheap Micro:bits. (and so I've got a good tune to demo with I'm enlisting some help from an AI to create a track to test this with that I can use to demo - I'll be creative after I've inspired them :smile: )

The python saved here is taken from the Makecode project https://makecode.microbit.org/S26000-11508-29408-02742 which I'm making in blocks so anyone can understand it. I'm just putting it here in GitHub for version control. OK it turns out that the Makecode site does that... kinda - I trust this more. Plus I can document and have multiple block projects collected here if I want. 

To use in MakeCode:
- copy/pasta the Python into the MakeCode project
- flip back to blocks and it should all render properly

To build manually in VSCode:
- check "from microbit import *" is at the  start of main.py (I copy & paste over from MakeCode a lot and I won't be adding this all the time...)
- use normal commands from the palette like "Put-this-file" to send to Micro:bit

### Demo
https://github.com/user-attachments/assets/debd2a19-0f8b-4f12-831e-922c98faf1f4

## The tunes and the tracker format

There are three tunes, all arranged for the same 4 channels and the same 10 instruments:
- a techno version of the traditional folk tune Korobeiniki (the one behind Tetris): `Claude/mods/korobeiniki_techno_8ch_v3_microbit.xm` (its first 4 channels are the tune; the other 4 are extras for a future 8-track version)
- a bhangra techno version of Pachelbel's Canon in D (from about 1700, so out of copyright): `Claude/mods/canon_bhangra_4ch_microbit.xm`
- a drum-heavy synthwave version of Beethoven's Ode to Joy (1824, also out of copyright), with minor verses, major drops and a key change: `Claude/mods/ode_to_joy_synthwave_v3_4ch_microbit.xm`

You can open the .xm files in a tracker such as [OpenMPT](https://openmpt.org/) and change them.

The music on the Micro:bits is stored in a very simple tracker format, with one row every 200ms (an eighth note at 150 BPM) and 32 rows to a pattern. It is described for students in [Claude/microbit_tracker_format_students.md](Claude/microbit_tracker_format_students.md): how notes (`tone D-6`), sounds (`wave kick`), silence (`x`) and rests (`-`) are written, and how the Micro:bit plays them.


## Techno:bit controls

### Playing Songs
On startup the Techno:bit shows the current 'track' it's going to play. 

Press the A button to cycle between the tracks:
- 1 = Lead (the melody)
- 2 = Acid bass
- 3 = Voice lane (a few tone phrases, plus claps, crashes, toms, pews and Hoover stabs)
- 4 = Drums (kick and hats, plus snare and toms in the fills)

Press the B button to select the track. Then the Techno:bit will show which song it's going to play.

Now press the A button to cycle between the songs:
- \* = Korobeiniki (Tetris theme)
- \+ = Pachelbel's Canon in D
- \# = Beethoven's Ode to Joy

Now press the B button to play that song using that track.

While playing press the B button to stop playing.

### Conducting via Radio
When in track selection, press the Micro:bit logo to enter Conductor mode. The track number will now show 0.

Now when you select a song (press B, then A to choose, then B to play) the microbit will broadcast each pattern number of the song for the other microbits to play on their tracks, while this microbit plays a metronome beat.

So with 5 Techno:bits... one conductor makes the other 4 play the full 4 tracks of the song!

Radio group 23 is used, so every Techno:bit needs to be on the same group.

### What the lights show
The LEDs show what each Techno:bit is playing: one LED for each note (but not its octave) or sound, with related sounds sharing an LED. While playing, the top row shows the track (one LED for each of tracks 0 to 4). The tables are in the format document.


## AI Use
Gemini was used to investigate the timings for the sounds, radio, leds, etc, which included examples of Makecode Blocks I could use to implement the timings.

Claude was used to produce the XM music files, and some Python code for how that mod file can be used in Makecode (waveforms, note pitches, sequences, tracks, etc). Generated files are all under the Claude folder in this project.

Claude Code has been used to create the .XM file conversion app, and associated code generation to include that in the Makecode app. 

The intention of using AI in this way is to allow me to quickly use the app I've coded to have a cool tune, and then allow students to explore changing both the code and the music. 

Claude (in the Claude desktop app, with access to this project) also helped to document the tracker format, converted the code to that format, wrote the 12 sound functions and the hardcoded versions of all three tunes, created the Canon in D and Ode to Joy .xm files, fixed the radio timing between patterns, and shrank the demo video. Its drafts are in `Claude/suggestions` and its .xm files in `Claude/mods`.
