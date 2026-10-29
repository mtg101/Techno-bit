def play_track(track: List[any]):
    global track_row, next_note_time
    track_row = 0
    while track_row < 32 and is_playing:
        next_note_time = input.running_time() + 200
        play_note(convert_to_text(track[track_row]))
        basic.pause(max(0, next_note_time - input.running_time()))
        track_row += 1
    music.stop_all_sounds()
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
def show_track_name():
    basic.clear_screen()
    basic.show_string("" + (track_names[current_track]))
def create_songs():
    global song_1, song_2, current_song, num_songs, song_list, song_names
    song_1 = [0, 1, 0, 1]
    song_2 = [1, 0, 1, 0]
    current_song = 0
    num_songs = 2
    song_list = [song_1, song_2]
    song_names = ["*", "+"]
def create_track_bass_alt():
    global track_bass_alt
    track_bass_alt = ["wave bass",
        "x",
        "-",
        "-",
        "wave bass",
        "-",
        "x",
        "-",
        "wave bass",
        "x",
        "-",
        "-",
        "wave bass",
        "-",
        "x",
        "-",
        "wave bass",
        "x",
        "-",
        "-",
        "wave bass",
        "-",
        "x",
        "-",
        "wave bass",
        "x",
        "-",
        "-",
        "wave bass",
        "-",
        "x",
        "-"]
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
        led_x = 0
        led_y = 1
        led.plot(led_x, led_y)
    if "wave tom" == noteName:
        music.stop_all_sounds()
        music.play(music.create_sound_expression(WaveShape.TRIANGLE,
                300,
                200,
                255,
                0,
                75,
                SoundExpressionEffect.NONE,
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
        led_x = 2
        led_y = 1
        led.plot(led_x, led_y)
    if "tone" == noteName.split(" ")[0]:
        music.stop_all_sounds()
        play_tone(noteName.split(" ")[1],
            parse_float(noteName.split(" ")[2]),
            1000)
    if "-" == noteName:
        led.unplot(led_x, led_y)

def on_button_pressed_a():
    global current_song, current_pattern, current_track
    if not (is_playing):
        if choosing_pattern:
            if choosing_song:
                if current_song == num_songs - 1:
                    current_song = 0
                else:
                    current_song = current_song + 1
                show_song_name()
            else:
                if current_pattern == num_patterns - 1:
                    current_pattern = 0
                else:
                    current_pattern = current_pattern + 1
                show_pattern_name()
        else:
            if current_track == num_tracks:
                current_track = 1
            else:
                current_track = current_track + 1
            show_track_name()
input.on_button_pressed(Button.A, on_button_pressed_a)

def create_track_drums_2_alt():
    global track_drums_2_alt
    track_drums_2_alt = ["wave tom",
        "-",
        "wave tom",
        "-",
        "-",
        "-",
        "wave tom",
        "-",
        "wave tom",
        "-",
        "wave tom",
        "-",
        "-",
        "-",
        "wave tom",
        "-",
        "wave tom",
        "-",
        "wave tom",
        "-",
        "-",
        "-",
        "wave tom",
        "-",
        "wave tom",
        "=",
        "wave snare",
        "-",
        "=",
        "-",
        "wave snare",
        "-"]
def play_tone(name: str, octave: number, ms: number):
    global tone_index, tone_freq, led_x, led_y
    tone_index = tone_name.index_of(name)
    if tone_index < 0:
        tone_index = tone_sharp.index_of(name)
    if tone_index < 0:
        tone_index = tone_flat.index_of(name)
    if tone_index >= 0:
        tone_freq = tone_hz[tone_index]
        for index in range(octave - 3):
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
        elif True:
            led_x = tone_index - 10
            led_y = 2
            led.plot(led_x, led_y)
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
    led.plot(current_track, 0)
    play_track(song_tracks[current_track][current_pattern])
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

def on_received_string(receivedString):
    global receiving_song, is_playing, current_pattern, start_track
    if receivedString == "stop":
        receiving_song = False
        is_playing = False
    elif receivedString == "start song":
        receiving_song = True
    elif receivedString == "end song":
        receiving_song = False
    else:
        if not (is_playing):
            if current_track != 0:
                current_pattern = parse_float(receivedString)
                start_track = True
radio.on_received_string(on_received_string)

def create_track_drums_1_alt():
    global track_drums_1_alt
    track_drums_1_alt = ["wave kick",
        "-",
        "-",
        "wave kick",
        "wave kick",
        "-",
        "wave kick",
        "-",
        "-",
        "wave kick",
        "wave kick",
        "-",
        "wave kick",
        "",
        "",
        "wave kick",
        "wave kick",
        "-",
        "wave kick",
        "-",
        "-",
        "wave kick",
        "wave kick",
        "-",
        "wave kick",
        "-",
        "-",
        "wave kick",
        "wave kick",
        "-",
        "wave kick",
        "-"]
def create_track_melody_alt():
    global track_melody_alt
    track_melody_alt = ["-",
        "tone D 4",
        "-",
        "tone F 4",
        "tone A 4",
        "-",
        "tone G 4",
        "tone F 4",
        "tone E 4",
        "-",
        "-",
        "tone C 4",
        "tone E 4",
        "-",
        "tone D 4",
        "tone C 4",
        "tone B 3",
        "- ",
        "tone B 3",
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

def on_logo_pressed():
    global current_track, choosing_song
    if not (is_playing):
        if not (choosing_pattern):
            current_track = 0
            show_track_name()
        else:
            choosing_song = not (choosing_song)
            if choosing_song:
                show_song_name()
            else:
                show_pattern_name()
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_pressed)

def create_patterns():
    global num_tracks, current_track, num_patterns, current_pattern, is_playing, patterns_metronome, patterns_drums_1, patterns_drums_2, patterns_bass, patterns_melody, song_tracks, track_names, pattern_names
    num_tracks = 4
    current_track = 1
    num_patterns = 2
    current_pattern = 0
    is_playing = False
    create_track_metronome()
    create_track_drums_1()
    create_track_drums_2()
    create_track_bass()
    create_track_melody()
    create_track_drums_1_alt()
    create_track_drums_2_alt()
    create_track_bass_alt()
    create_track_melody_alt()
    patterns_metronome = [track_metronome, track_metronome]
    patterns_drums_1 = [track_drums_1, track_drums_1_alt]
    patterns_drums_2 = [track_drums_2, track_drums_2_alt]
    patterns_bass = [track_bass, track_bass_alt]
    patterns_melody = [track_melody, track_melody_alt]
    song_tracks = [patterns_metronome,
        patterns_drums_1,
        patterns_drums_2,
        patterns_bass,
        patterns_melody]
    track_names = ["0", "1", "2", "3", "4"]
    pattern_names = ["A", "B"]
def create_tones():
    global tone_name, tone_sharp, tone_flat, tone_hz
    tone_name = ["C", "", "D", "", "E", "F", "", "G", "", "A", "", "B"]
    tone_sharp = ["", "C#", "", "D#", "", "", "F#", "", "G#", "", "A#", ""]
    tone_flat = ["", "Db", "", "Eb", "", "", "Gb", "", "Ab", "", "Bb", ""]
    tone_hz = [131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247]
def show_song_name():
    basic.clear_screen()
    basic.show_string("" + (song_names[current_song]))
def show_pattern_name():
    basic.clear_screen()
    basic.show_string("" + (pattern_names[current_pattern]))
current_song_position = 0
playing_song = False
pattern_names: List[str] = []
patterns_melody: List[List[str]] = []
patterns_bass: List[List[str]] = []
patterns_drums_2: List[List[str]] = []
patterns_drums_1: List[List[str]] = []
patterns_metronome: List[List[str]] = []
track_drums_2: List[str] = []
track_bass: List[str] = []
track_melody_alt: List[str] = []
track_drums_1_alt: List[str] = []
track_melody: List[str] = []
song_tracks: List[List[List[str]]] = []
track_metronome: List[str] = []
tone_hz: List[number] = []
tone_freq = 0
tone_flat: List[str] = []
tone_sharp: List[str] = []
tone_name: List[str] = []
tone_index = 0
track_drums_2_alt: List[str] = []
num_tracks = 0
num_patterns = 0
current_pattern = 0
choosing_song = False
track_bass_alt: List[str] = []
song_names: List[str] = []
song_list: List[List[number]] = []
num_songs = 0
current_song = 0
song_2: List[number] = []
song_1: List[number] = []
current_track = 0
track_names: List[str] = []
track_drums_1: List[str] = []
next_note_time = 0
is_playing = False
track_row = 0
receiving_song = False
choosing_pattern = False
start_track = False
led_y = 0
led_x = 0
radio.set_group(23)
music.stop_all_sounds()
music.set_built_in_speaker_enabled(True)
music.set_volume(255)
led_x = -1
led_y = -1
start_track = False
choosing_pattern = False
receiving_song = False
create_patterns()
show_track_name()
create_tones()
create_songs()

def on_forever():
    global current_pattern, current_song_position, start_track, choosing_pattern
    if start_track:
        if playing_song:
            while current_song_position < len(song_list[current_song]) and playing_song:
                if current_track == 0:
                    if current_song_position == len(song_list[current_song]) - 1:
                        radio.send_string("end song")
                    radio.send_string(convert_to_text(song_list[current_song][current_song_position]))
                current_pattern = song_list[current_song][current_song_position]
                play_current_pattern()
                current_song_position += 1
                if current_track == 0:
                    control.wait_micros(5000)
        else:
            play_current_pattern()
        start_track = False
        choosing_pattern = False
        if not (receiving_song):
            show_track_name()
basic.forever(on_forever)

def on_forever2():
    if input.light_level() < 30:
        music.set_volume(0)
    else:
        music.set_volume(255)
basic.forever(on_forever2)

def on_forever3():
    global playing_song, current_song_position, start_track, choosing_pattern, is_playing
    if input.button_is_pressed(Button.B):
        if not (is_playing):
            if choosing_pattern:
                if choosing_song:
                    playing_song = True
                    current_song_position = 0
                    if current_track == 0:
                        radio.send_string("start song")
                        radio.send_string(convert_to_text(song_list[current_song][current_song_position]))
                else:
                    playing_song = False
                    if current_track == 0:
                        radio.send_string(convert_to_text(current_pattern))
                start_track = True
            else:
                choosing_pattern = True
                show_pattern_name()
        else:
            if current_track == 0:
                radio.send_string("stop")
            playing_song = False
            is_playing = False
            choosing_pattern = False
        while input.button_is_pressed(Button.B):
            basic.pause(50)
basic.forever(on_forever3)
