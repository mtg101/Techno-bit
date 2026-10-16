def play_note(note: str):
    if "x" == note:
        music.stop_all_sounds()
    if "wave kick" == note:
        music.play(music.create_sound_expression(WaveShape.SQUARE,
                200,
                1,
                255,
                0,
                100,
                SoundExpressionEffect.NONE,
                InterpolationCurve.CURVE),
            music.PlaybackMode.IN_BACKGROUND)
    if "wave snare" == note:
        music.play(music.create_sound_expression(WaveShape.NOISE,
                523,
                1,
                255,
                0,
                100,
                SoundExpressionEffect.WARBLE,
                InterpolationCurve.LOGARITHMIC),
            music.PlaybackMode.IN_BACKGROUND)
def play_pattern(pattern: List[any]):
    for index in range(32):
        play_note(pattern_1[index])
        basic.pause(200)

def on_button_pressed_a():
    basic.clear_screen()
    play_pattern(pattern_1)
input.on_button_pressed(Button.A, on_button_pressed_a)

def led_show_not_playing():
    basic.show_leds("""
        . . . # .
        . . # . .
        . # . . .
        # # # # #
        # # # # #
        """)

def on_button_pressed_b():
    music.stop_all_sounds()
    led_show_not_playing()
input.on_button_pressed(Button.B, on_button_pressed_b)

def create_pattern_arrays():
    global pattern_1
    pattern_1 = ["wave kick"]
    pattern_1.append("-")
    pattern_1.append("wave kick")
    pattern_1.append("-")
    pattern_1.append("wave kick")
    pattern_1.append("-")
    pattern_1.append("wave kick")
    pattern_1.append("-")
    pattern_1.append("wave kick")
    pattern_1.append("-")
    pattern_1.append("wave kick")
    pattern_1.append("-")
    pattern_1.append("wave kick")
    pattern_1.append("-")
    pattern_1.append("wave kick")
    pattern_1.append("-")
    pattern_1.append("wave kick")
    pattern_1.append("wave snare")
    pattern_1.append("wave kick")
    pattern_1.append("wave snare")
    pattern_1.append("wave kick")
    pattern_1.append("wave snare")
    pattern_1.append("wave kick")
    pattern_1.append("wave snare")
    pattern_1.append("wave kick")
    pattern_1.append("wave snare")
    pattern_1.append("wave kick")
    pattern_1.append("wave snare")
    pattern_1.append("wave kick")
    pattern_1.append("wave snare")
    pattern_1.append("wave kick")
    pattern_1.append("wave snare")
pattern_1: List[str] = []
music.stop_all_sounds()
music.set_built_in_speaker_enabled(True)
music.set_volume(255)
led_show_not_playing()
create_pattern_arrays()