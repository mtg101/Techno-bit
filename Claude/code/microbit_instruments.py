# =====================================================================
#  KOROBEINIKI TECHNO  -  micro:bit V2 instrument library
#  MakeCode Python (block compatible).  Paste into the Python tab.
#  Needs a micro:bit V2 (sound expressions only work on V2).
# =====================================================================
#
#  10 instruments - the same numbers as the tracker file:
#     1  TONE      pitched: the only instrument that plays a melody
#     2  KICK      3  SNARE     4  CLAP     5  HAT     6  OPEN_HAT     7  CRASH
#     8  TOM       2 pitches:  variant 0 = low tom,   variant 1 = high tom
#     9  PEW       2 pitches:  variant 0 = low pew,   variant 1 = high pew
#    10  HOOVER    2 pitches:  variant 0 = E4 stab,   variant 1 = A4 stab
#
#  A player board does one of three things on each row (a row is 200 ms):
#     start_tone(freq)          a Tone note     (music.ring_tone)
#     play_hit(inst, variant)   any other instrument (variant only matters for 8, 9, 10)
#     stop_sound()              note-off: silence
#
#  Test program at the bottom:
#     Button A = next instrument      Button B = play it (low variant)
#     Buttons A+B = play it (high variant)
#     Touch the logo = 2-bar test groove, then a fill of toms, pew-pews and Hoover stabs
#
#  All the sounds are tuned for the tiny V2 speaker: nothing below about 170 Hz.

# ---------- instrument numbers ----------
TONE = 1
KICK = 2
SNARE = 3
CLAP = 4
HAT = 5
OPEN_HAT = 6
CRASH = 7
TOM = 8
PEW = 9
HOOVER = 10

# ---------- settings ----------
ROW_MS = 200               # one row = one eighth note at 150 BPM
CUT_PREVIOUS = True        # a new sound cuts off the old one (like a tracker channel)
sound_is_playing = False   # remembers if a sound effect might still be playing
current_instrument = 1

# test patterns (used by the logo-touch demo)
groove = [KICK, HAT, CLAP, HAT, KICK, HAT, CLAP, HAT]
fill_hits = [KICK, SNARE, TOM, TOM, PEW, PEW, PEW, PEW, HOOVER, HOOVER, CRASH]
fill_variants = [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0]


# ---------- the Tone instrument ----------
def start_tone(tone_freq: number):
    global sound_is_playing
    if sound_is_playing:
        music.stop_all_sounds()
        sound_is_playing = False
    music.ring_tone(tone_freq)


def stop_sound():
    global sound_is_playing
    music.stop_all_sounds()
    sound_is_playing = False


# ---------- the 9 sound-expression instruments ----------
# Each one: wave shape, start Hz, end Hz, start volume, end volume, length (ms), effect, curve.

def play_kick():
    music.play(music.create_sound_expression(WaveShape.SINE, 520, 170, 255, 0, 100, SoundExpressionEffect.NONE, InterpolationCurve.LOGARITHMIC), music.PlaybackMode.IN_BACKGROUND)


def play_snare():
    music.play(music.create_sound_expression(WaveShape.NOISE, 2500, 800, 210, 0, 140, SoundExpressionEffect.NONE, InterpolationCurve.LINEAR), music.PlaybackMode.IN_BACKGROUND)


def play_clap():
    music.play(music.create_sound_expression(WaveShape.NOISE, 3500, 1800, 190, 0, 100, SoundExpressionEffect.TREMOLO, InterpolationCurve.LINEAR), music.PlaybackMode.IN_BACKGROUND)


def play_hat():
    music.play(music.create_sound_expression(WaveShape.NOISE, 5000, 5000, 110, 0, 40, SoundExpressionEffect.NONE, InterpolationCurve.LINEAR), music.PlaybackMode.IN_BACKGROUND)


def play_open_hat():
    music.play(music.create_sound_expression(WaveShape.NOISE, 5000, 4000, 120, 0, 250, SoundExpressionEffect.NONE, InterpolationCurve.LINEAR), music.PlaybackMode.IN_BACKGROUND)


def play_crash():
    music.play(music.create_sound_expression(WaveShape.NOISE, 4500, 2500, 170, 0, 800, SoundExpressionEffect.NONE, InterpolationCurve.LOGARITHMIC), music.PlaybackMode.IN_BACKGROUND)


def play_tom(variant: number):
    if variant == 0:
        music.play(music.create_sound_expression(WaveShape.SINE, 420, 240, 240, 0, 180, SoundExpressionEffect.NONE, InterpolationCurve.LOGARITHMIC), music.PlaybackMode.IN_BACKGROUND)
    else:
        music.play(music.create_sound_expression(WaveShape.SINE, 630, 360, 240, 0, 120, SoundExpressionEffect.NONE, InterpolationCurve.LOGARITHMIC), music.PlaybackMode.IN_BACKGROUND)


def play_pew(variant: number):
    if variant == 0:
        music.play(music.create_sound_expression(WaveShape.SQUARE, 1500, 350, 200, 0, 150, SoundExpressionEffect.NONE, InterpolationCurve.LOGARITHMIC), music.PlaybackMode.IN_BACKGROUND)
    else:
        music.play(music.create_sound_expression(WaveShape.SQUARE, 3000, 700, 200, 0, 80, SoundExpressionEffect.NONE, InterpolationCurve.LOGARITHMIC), music.PlaybackMode.IN_BACKGROUND)


def play_hoover(variant: number):
    if variant == 0:
        music.play(music.create_sound_expression(WaveShape.SAWTOOTH, 555, 330, 230, 110, 200, SoundExpressionEffect.VIBRATO, InterpolationCurve.LOGARITHMIC), music.PlaybackMode.IN_BACKGROUND)
    else:
        music.play(music.create_sound_expression(WaveShape.SAWTOOTH, 740, 440, 230, 110, 200, SoundExpressionEffect.VIBRATO, InterpolationCurve.LOGARITHMIC), music.PlaybackMode.IN_BACKGROUND)


# ---------- play any instrument (2 to 10) by number ----------
def play_hit(inst: number, variant: number):
    global sound_is_playing
    if CUT_PREVIOUS:
        music.stop_all_sounds()
    sound_is_playing = True
    if inst == KICK:
        play_kick()
    elif inst == SNARE:
        play_snare()
    elif inst == CLAP:
        play_clap()
    elif inst == HAT:
        play_hat()
    elif inst == OPEN_HAT:
        play_open_hat()
    elif inst == CRASH:
        play_crash()
    elif inst == TOM:
        play_tom(variant)
    elif inst == PEW:
        play_pew(variant)
    elif inst == HOOVER:
        play_hoover(variant)


# ---------- test program ----------
def audition(variant: number):
    if current_instrument == TONE:
        if variant == 0:
            start_tone(440)
        else:
            start_tone(880)
        basic.pause(400)
        stop_sound()
    else:
        play_hit(current_instrument, variant)


def on_button_pressed_a():
    global current_instrument
    current_instrument += 1
    if current_instrument > 10:
        current_instrument = 1
    basic.show_number(current_instrument)
input.on_button_pressed(Button.A, on_button_pressed_a)


def on_button_pressed_b():
    audition(0)
input.on_button_pressed(Button.B, on_button_pressed_b)


def on_button_pressed_ab():
    audition(1)
input.on_button_pressed(Button.AB, on_button_pressed_ab)


def on_logo_pressed():
    for bar in range(2):
        for hit in groove:
            play_hit(hit, 0)
            basic.pause(ROW_MS)
    for i in range(len(fill_hits)):
        play_hit(fill_hits[i], fill_variants[i])
        basic.pause(ROW_MS)
    stop_sound()
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_pressed)

basic.show_number(current_instrument)
