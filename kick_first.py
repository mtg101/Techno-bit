def led_show_not_playing():
    basic.show_leds("""
        . . . # .
        . . # . .
        . # . . .
        # # # # #
        # # # # #
        """)
music.stop_all_sounds()
music.set_built_in_speaker_enabled(True)
music.set_volume(255)
led_show_not_playing()