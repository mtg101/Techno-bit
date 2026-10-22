def create_track_drums_1():
    global track_drums_1
    track_drums_1 = ["wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat",
        "wave kick",
        "wave hihat"]

def on_received_number(receivedNumber):
    if not (is_playing):
        if current_pattern != 0:
            play_current_pattern()
radio.on_received_number(on_received_number)

def play_note(noteName: str):
    global led_x, led_y
    if "x" == noteName:
        music.stop_all_sounds()
        led.unplot(led_x, led_y)
    if "wave kick" == noteName:
        music.stop_all_sounds()
        music.play(music.create_sound_expression(WaveShape.SQUARE,
                200,
                1,
                255,
                0,
                100,
                SoundExpressionEffect.NONE,
                InterpolationCurve.CURVE),
            music.PlaybackMode.IN_BACKGROUND)
        led.unplot(led_x, led_y)
        led_x = 4
        led_y = 1
        led.plot(led_x, led_y)
    if "wave snare" == noteName:
        music.stop_all_sounds()
        music.play(music.create_sound_expression(WaveShape.NOISE,
                523,
                1,
                255,
                166,
                100,
                SoundExpressionEffect.WARBLE,
                InterpolationCurve.LOGARITHMIC),
            music.PlaybackMode.IN_BACKGROUND)
        led.unplot(led_x, led_y)
        led_x = 3
        led_y = 1
        led.plot(led_x, led_y)
    if "wave hihat" == noteName:
        music.stop_all_sounds()
        music.play(music.create_sound_expression(WaveShape.NOISE,
                5000,
                3460,
                255,
                0,
                50,
                SoundExpressionEffect.NONE,
                InterpolationCurve.LINEAR),
            music.PlaybackMode.IN_BACKGROUND)
        led.unplot(led_x, led_y)
        led_x = 2
        led_y = 1
        led.plot(led_x, led_y)
    if "wave bass" == noteName:
        music.stop_all_sounds()
        music.play(music.create_sound_expression(WaveShape.SINE,
                210,
                1,
                255,
                0,
                5000,
                SoundExpressionEffect.WARBLE,
                InterpolationCurve.CURVE),
            music.PlaybackMode.IN_BACKGROUND)
        led.unplot(led_x, led_y)
        led_x = 1
        led_y = 1
        led.plot(led_x, led_y)
    if "wave lopew" == noteName:
        music.stop_all_sounds()
        music.play(music.create_sound_expression(WaveShape.SQUARE,
                1374,
                1,
                255,
                0,
                200,
                SoundExpressionEffect.NONE,
                InterpolationCurve.CURVE),
            music.PlaybackMode.IN_BACKGROUND)
        led.unplot(led_x, led_y)
        led_x = 4
        led_y = 2
        led.plot(led_x, led_y)
    if "wave hipew" == noteName:
        music.stop_all_sounds()
        music.play(music.create_sound_expression(WaveShape.SQUARE,
                3789,
                1,
                255,
                0,
                200,
                SoundExpressionEffect.NONE,
                InterpolationCurve.CURVE),
            music.PlaybackMode.IN_BACKGROUND)
        led.unplot(led_x, led_y)
        led_x = 3
        led_y = 2
        led.plot(led_x, led_y)
    if "fx hello" == noteName:
        music.stop_all_sounds()
        music.play(music.builtin_playable_sound_effect(soundExpression.hello),
            music.PlaybackMode.IN_BACKGROUND)
        led.unplot(led_x, led_y)
        led_x = 0
        led_y = 1
        led.plot(led_x, led_y)
    if "tone" == noteName.split(" ")[0]:
        music.stop_all_sounds()
        play_tone(noteName.split(" ")[1],
            parse_float(noteName.split(" ")[2]),
            1000)
    if "-" == noteName:
        led.unplot(led_x, led_y)
def play_pattern(pattern: List[any]):
    global next_note_time
    for index in range(32):
        next_note_time = input.running_time() + 200
        play_note(convert_to_text(pattern[index]))
        basic.pause(max(0, next_note_time - input.running_time()))
    music.stop_all_sounds()

def on_button_pressed_a():
    global current_pattern
    if not (is_playing):
        if current_pattern == num_patterns:
            current_pattern = 0
        else:
            current_pattern = current_pattern + 1
        show_pattern()
input.on_button_pressed(Button.A, on_button_pressed_a)

def play_tone(name: str, octave: number, ms: number):
    global tone_index, tone_freq, led_x, led_y
    tone_index = tone_name.index_of(name)
    if tone_index < 0:
        tone_index = tone_sharp.index_of(name)
    if tone_index < 0:
        tone_index = tone_flat.index_of(name)
    if tone_index >= 0:
        tone_freq = tone_hz[tone_index]
        for index2 in range(octave - 3):
            tone_freq = tone_freq * 2
        music.ring_tone(tone_freq)
        led.unplot(led_x, led_y)
        if tone_index < 5:
            led_x = tone_index
            led_y = 4
            led.plot(led_x, led_y)
        elif tone_index < 10:
            led_x = tone_index - 5
            led_y = 3
            led.plot(led_x, led_y)
        elif tone_index < 15:
            led_x = tone_index - 10
            led_y = 2
            led.plot(led_x, led_y)
def show_pattern():
    if current_pattern == 0:
        basic.show_leds("""
            # . . . .
            . # . . .
            . . # . .
            . . . # #
            . . . # #
            """)
    else:
        basic.show_number(current_pattern)
def create_track_metronome():
    global track_metronome
    track_metronome = ["wave snare",
        "-",
        "wave hihat",
        "-",
        "wave hihat",
        "-",
        "wave hihat",
        "-",
        "wave snare",
        "-",
        "wave hihat",
        "-",
        "wave hihat",
        "-",
        "wave hihat",
        "-",
        "wave snare",
        "-",
        "wave hihat",
        "-",
        "wave hihat",
        "-",
        "wave hihat",
        "-",
        "wave snare",
        "-",
        "wave hihat",
        "-",
        "wave hihat",
        "-",
        "wave hihat",
        "-"]
def play_current_pattern():
    global is_playing
    is_playing = True
    basic.clear_screen()
    led.plot(current_pattern, 0)
    if current_pattern == 0:
        play_pattern(track_metronome)
    if current_pattern == 1:
        play_pattern(track_drums_1)
    if current_pattern == 2:
        play_pattern(track_drums_2)
    if current_pattern == 3:
        play_pattern(track_bass)
    if current_pattern == 4:
        play_pattern(track_melody)
    show_pattern()
    is_playing = False
def create_track_melody():
    global track_melody
    track_melody = ["tone E 4",
        "-",
        "tone B 3",
        "tone C 4",
        "tone D 4",
        "-",
        "tone C 4",
        "tone B 3",
        "tone A 3",
        "-",
        "tone A 3",
        "tone C 4",
        "tone E 4",
        "-",
        "tone D 4",
        "tone C 4",
        "tone B 3",
        "-",
        "-",
        "tone C 4",
        "tone D 4",
        "-",
        "tone E 4",
        "-",
        "tone C 4",
        "-",
        "tone A 3",
        "-",
        "tone A 3",
        "-",
        "-",
        "-"]

def on_button_pressed_b():
    if not (is_playing):
        if current_pattern == 0:
            radio.send_number(0)
        play_current_pattern()
input.on_button_pressed(Button.B, on_button_pressed_b)

def create_track_bass():
    global track_bass
    track_bass = ["wave bass",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "wave bass",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "wave bass",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "wave bass",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-"]
def create_track_drums_2():
    global track_drums_2
    track_drums_2 = ["-",
        "-",
        "wave snare",
        "-",
        "-",
        "-",
        "wave snare",
        "-",
        "-",
        "-",
        "wave snare",
        "-",
        "-",
        "-",
        "wave snare",
        "-",
        "-",
        "-",
        "wave snare",
        "-",
        "-",
        "-",
        "wave snare",
        "-",
        "-",
        "=",
        "wave snare",
        "-",
        "=",
        "-",
        "wave snare",
        "-"]
def create_patterns():
    global num_patterns, current_pattern, is_playing
    num_patterns = 4
    current_pattern = 0
    is_playing = False
    create_track_metronome()
    create_track_drums_1()
    create_track_drums_2()
    create_track_bass()
    create_track_melody()
def create_tones():
    global tone_name, tone_sharp, tone_flat, tone_hz
    tone_name = ["C", "", "D", "", "E", "F", "", "G", "", "A", "", "B"]
    tone_sharp = ["", "C#", "", "D#", "", "", "F#", "", "G#", "", "A#", ""]
    tone_flat = ["", "Db", "", "Eb", "", "", "Gb", "", "Ab", "", "Bb", ""]
    tone_hz = [131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247]
track_melody: List[str] = []
track_bass: List[str] = []
track_drums_2: List[str] = []
track_metronome: List[str] = []
tone_hz: List[number] = []
tone_freq = 0
tone_flat: List[str] = []
tone_sharp: List[str] = []
tone_name: List[str] = []
tone_index = 0
num_patterns = 0
next_note_time = 0
current_pattern = 0
is_playing = False
track_drums_1: List[str] = []
led_y = 0
led_x = 0
radio.set_group(23)
music.stop_all_sounds()
music.set_built_in_speaker_enabled(True)
music.set_volume(255)
led_x = -1
led_y = -1
show_pattern()
create_patterns()
create_tones()