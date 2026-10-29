Messing about with Micro:bits https://microbit.org/ to make tracker music, like back in the good old Amiga days. But with each Micro:bit playing a single track, and a conductor broadcasting radio signals to play patterns.

The python saved here is taken from the Makecode project https://makecode.microbit.org/S26000-11508-29408-02742 which I'm making in blocks so anyone can understand it. I'm just putting it here in GitHub for version control. OK it turns out that the Makecode site does that... kinda - I trust this more. Plus I can document and have multiple block projects collected here if I want. 

To build manually in VSCode:
- check "from microbit import *" is at the  start of main.py (I copy & paste over from MakeCode a lot abd forget...)
- use normal commands from the palatte like "Put-this-file" to send to Micro:bit

AI has been used in areas of this project, not for the code (beyond conversing with LLMs for advice), but for some of the musical and visual assets. I'm here to be creative with the code, and I've never meed able to make a good tracker tune :( Others are free to use this code or the idea to make their own music :)


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


