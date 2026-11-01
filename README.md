Messing about with Micro:bits https://microbit.org/ to make tracker music, like back in the good old Amiga days. But with each Micro:bit playing a single track, and a conductor broadcasting radio signals to play patterns.

Plus I think it makes a cool demo to show the students at our local coding club what you can do with a few cheap Micro:bits. (and so I've got a good tune to demo with I'm enlisting some help from an AI to create a track to test this with that I can use to demo - I'll be creative after I've inspired them :smile: )

The python saved here is taken from the Makecode project https://makecode.microbit.org/S26000-11508-29408-02742 which I'm making in blocks so anyone can understand it. I'm just putting it here in GitHub for version control. OK it turns out that the Makecode site does that... kinda - I trust this more. Plus I can document and have multiple block projects collected here if I want. 

To use in MakeCode:
- copy/pasta the Python into the MakeCode project
- flip back to blocks and it should all render properly

To build manually in VSCode:
- check "from microbit import *" is at the  start of main.py (I copy & paste over from MakeCode a lot and I won't be adding this all the time...)
- use normal commands from the palette like "Put-this-file" to send to Micro:bit


## The tune and the tracker format

The tune is a techno version of the traditional folk tune Korobeiniki (the one behind Tetris), arranged for 4 channels: `Claude/mods/korobeiniki_techno_4ch_microbit.xm`. You can open the .xm file in a tracker such as [OpenMPT](https://openmpt.org/) and change it.

The music on the Micro:bits is stored in a very simple tracker format, with one row every 200ms (an eighth note at 150 BPM) and 32 rows to a pattern. It is described for students in [Claude/microbit_tracker_format_students.md](Claude/microbit_tracker_format_students.md): how notes (`tone D-6`), sounds (`wave kick`), silence (`x`) and rests (`-`) are written, and how the Micro:bit plays them.


## Techno:bit controls

### Playing Patterns
On startup the Techno:bit shows the current 'track' it's going to play. 

Press the A button to cycle between the tracks:
- 1 = Lead (the melody)
- 2 = Acid bass
- 3 = Voice lane (a few tone phrases, plus claps, crashes, toms, pews and Hoover stabs)
- 4 = Drums (kick and hats, plus snare and toms in the fills)

Press the B button to select the track. Then the Techno:bit will show which pattern it's going to play.

Now press the A button to cycle between the 16 patterns, A to P (see the format document for what each one is).

Press the Micro:bit logo to switch to playing the song:
- \* = the whole song (64 patterns, about 6m50s)

Now press the B button to play that pattern/song using that track.

While playing press the B button to stop playing.

### Conducting via Radio
When in track selection, press the Micro:bit logo to enter Conductor mode. The track number will now show 0.

Now when you select a pattern/song the microbit will broadcast for other microbits to start playing their tracks, while this microbit plays a metronome beat.

So with 5 Techno:bits... one conductor makes the other 4 play the full 4 tracks of the pattern/song!

Radio group 23 is used, so every Techno:bit needs to be on the same group.

### What the lights show
The LEDs show what each Techno:bit is playing: one LED for each note (but not its octave) or sound, with related sounds sharing an LED. The tables are in the format document.


## AI Use
Gemini was used to investigate the timings for the sounds, radio, leds, etc, which included examples of Makecode Blocks I could use to implement the timings.

Claude was used to produce the XM music files, and some Python code for how that mod file can be used in Makecode (waveforms, note pitches, sequences, tracks, etc). Generated files are all under the Claude folder in this project.

Claude Code has been used to create the .XM file conversion app, and associated code generation to include that in the Makecode app. 

The intention of using AI in this way is to allow me to quickly use the app I've coded to have a cool tune, and then allow students to explore changing both the code and the music. 

Claude (in the Claude desktop app, with access to this project) also helped to document the tracker format, converted the code to that format, and wrote the 12 sound functions and the hardcoded version of the tune. Its drafts are in `Claude/suggestions`.
