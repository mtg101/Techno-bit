# =====================================================================
#  XM NOTE NAMES -> FREQUENCY (Hz)     (MakeCode Python, block compatible)
#  Three full octaves: C-4 to B-6  (XM note numbers 49 to 84, 36 notes)
#  The two lists line up: note_names[i] is the name of note_hz[i].
#  Names are written the way the tracker shows them: C-4, C#4, D-4, D#4 ...
#  Formula behind the numbers: Hz = 440 x 2^((note - 58) / 12)   (A-4 = note 58 = 440 Hz)
# =====================================================================

note_names = [
    "C-4", "C#4", "D-4", "D#4", "E-4", "F-4", "F#4", "G-4", "G#4", "A-4", "A#4", "B-4", "C-5",
    "C#5", "D-5", "D#5", "E-5", "F-5", "F#5", "G-5", "G#5", "A-5", "A#5", "B-5", "C-6", "C#6",
    "D-6", "D#6", "E-6", "F-6", "F#6", "G-6", "G#6", "A-6", "A#6", "B-6"
]

note_hz = [
    262, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494, 523, 554, 587, 622, 659, 698, 740,
    784, 831, 880, 932, 988, 1047, 1109, 1175, 1245, 1319, 1397, 1480, 1568, 1661, 1760, 1865,
    1976
]


# Look up a name such as "E-5" and give back its frequency (0 = silence if the name isn't found).
# Use it like this:   start_tone(note_to_hz("E-5"))
def note_to_hz(note_name: str):
    i = note_names.index_of(note_name)
    if i < 0:
        return 0
    return note_hz[i]
