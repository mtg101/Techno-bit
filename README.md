Messing about with Micro:bits https://microbit.org/ to make tracker music, like back in the good old Amiga days. But with each Micro:bit playing a single track, and a conductor broadcasting radio signals to play patterns.

Plus I think it makes a cool demo to show the students at our local coding club what you can do with a few cheap Micro:bits. (and so I've got a good tune to demo with I'm enlisting some help from an AI to create a track to test this with that I can use to demo - I'll be creative after I've inspired them :smile: )

The python saved here is taken from the Makecode project https://makecode.microbit.org/S26000-11508-29408-02742 which I'm making in blocks so anyone can understand it. I'm just putting it here in GitHub for version control. OK it turns out that the Makecode site does that... kinda - I trust this more. Plus I can document and have multiple block projects collected here if I want. 

### Demo


https://github.com/user-attachments/assets/debd2a19-0f8b-4f12-831e-922c98faf1f4

(The video file itself is in [techno-bit/media/technobit-demo.mp4](techno-bit/media/technobit-demo.mp4).)


## How this project is organised

| Folder | What it is |
|---|---|
| **[techno-bit/](techno-bit/)** | **The Techno:bit itself: start here.** The program, the tunes, ready-to-flash files, and the documentation for using it and making your own tunes: see [techno-bit/README.md](techno-bit/README.md). |
| [planning/](planning/) | Where the project is planned. `planning/claude/` is where I work with Claude (an AI assistant): notes, and suggested changes that haven't made it into `techno-bit/` yet. |

The MakeCode project for the base program is https://makecode.microbit.org/S26000-11508-29408-02742.


## AI Use
Gemini was used to investigate the timings for the sounds, radio, leds, etc, which included examples of Makecode Blocks I could use to implement the timings.

Claude was used to produce the XM music files, and some Python code for how that mod file can be used in Makecode (waveforms, note pitches, sequences, tracks, etc). Generated files are all under the Claude folder in this project.

Claude Code has been used to create the .XM file conversion app, and associated code generation to include that in the Makecode app. 

The intention of using AI in this way is to allow me to quickly use the app I've coded to have a cool tune, and then allow students to explore changing both the code and the music. 

Claude (in the Claude desktop app, with access to this project) also helped to document the tracker format, converted the code to that format, wrote the 12 sound functions and the hardcoded versions of all three tunes, created the Canon in D and Ode to Joy .xm files and the 8-track Korobeiniki, fixed the radio timing between patterns, and shrank the demo video. Its notes and drafts are in `planning/claude`.
