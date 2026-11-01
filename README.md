Messing about with Micro:bits https://microbit.org/ to make tracker music, like back in the good old Amiga days. But with each Micro:bit playing a single track, and a conductor broadcasting radio signals to play patterns.

Plus I think it makes a cool demo to show the students at our local coding club what you can do with a few cheap Micro:bits. (and so I've got a good tune to demo with I'm enlisting some help from an AI to create a track to test this with that I can use to demo - I'll be creative after I've inspirce them :smile: )

The python saved here is taken from the Makecode project https://makecode.microbit.org/S26000-11508-29408-02742 which I'm making in blocks so anyone can understand it. I'm just putting it here in GitHub for version control. OK it turns out that the Makecode site does that... kinda - I trust this more. Plus I can document and have multiple block projects collected here if I want. 

To use in MakeCode:
- copy/pasta the Python into the MakeCode project
- flip back to blocks and it should all render properly

To build manually in VSCode:
- check "from microbit import *" is at the  start of main.py (I copy & paste over from MakeCode a lot and I won't be adding this all the time...)
- use normal commands from the palatte like "Put-this-file" to send to Micro:bit



## Techno:bit controls

### Playing Patterns
On startup the Techno:bit shows the current 'track' or instrument it's going to play. 

Press the A button to cycle between the tracks/instruments:
- 1 = Drums 1
- 2 = Drums 2
- 3 = Bass
- 4 = Melody

Press the B button to select the track/instrument. Then the Techno:bit will show which pattern it's going to play.

Now press the A button to cycle between the patterns:
- A = normal pattern
- B = alt pattern

Press the Micro:bit logo to switch to playing songs:
- \* = first song
- \+ = second song

Now press the B button to play that pattern/song using that track/instrument.

While playing press the B button to stop playing.

### Conducting via Radio
When in track/instrument selection, press the Micro:bit logo to enter Conductor mode. The track/instrument number will now show 0.

Now when you select a pattern/song the microbit will brodcast for other microbits to start playing their tracks, which this microbit plays a metronome beat.

So with 5 Techno:bits... one conductor makes the other 4 play the full 4 tracks of the pattern/song!


## AI Use
Gemini was used to investigate the timings for the sounds, radio, leds, etc, which included examples of Makecode Blocks I could use to implement the timings.

Claude was used to produce the XM music files, and some Python code for how that mod file can be used in Makecode (waveforms, note pitches, sequences, tracks, etc). Generated files are all under the Claude folder in this project.

Claude Code has been used to crate the .XM file conversion app, and associated code generation to include that in the Makcode app. 

The inetention of using AI in this way is to allow me to quickly use the app I've coded to have a cool tune, and then allow students to explore changing both the code and the music. 