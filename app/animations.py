"""
Quote Reel Studio
Animation Engine
"""

from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout


# -----------------------------------
# Basic
# -----------------------------------

def none(clip):
    return clip


# -----------------------------------
# Fade
# -----------------------------------

def fade(clip, duration=0.8):
    return (
        clip
        .fx(fadein, duration)
        .fx(fadeout, duration)
    )


# -----------------------------------
# Slide Up
# -----------------------------------

def slide_up(clip):

    duration = clip.duration

    return (
        clip
        .set_position(
            lambda t: (
                "center",
                150 - min(t * 120, 120)
            )
        )
        .fx(fadein, 0.6)
        .fx(fadeout, 0.6)
    )


# -----------------------------------
# Slide Down
# -----------------------------------

def slide_down(clip):

    return (
        clip
        .set_position(
            lambda t: (
                "center",
                -100 + min(t * 120, 120)
            )
        )
        .fx(fadein, 0.6)
        .fx(fadeout, 0.6)
    )


# -----------------------------------
# Zoom In
# -----------------------------------

def zoom_in(clip):

    duration = clip.duration

    clip = clip.resize(
        lambda t: 0.85 + (0.15 * (t / duration))
    )

    return (
        clip
        .fx(fadein, 0.5)
        .fx(fadeout, 0.5)
    )


# -----------------------------------
# Zoom Out
# -----------------------------------

def zoom_out(clip):

    duration = clip.duration

    clip = clip.resize(
        lambda t: 1.15 - (0.15 * (t / duration))
    )

    return (
        clip
        .fx(fadein, 0.5)
        .fx(fadeout, 0.5)
    )


# -----------------------------------
# Bounce
# -----------------------------------

def bounce(clip):

    def y(t):

        if t < 0.4:
            return 180 - t * 220

        return 92

    return (
        clip
        .set_position(
            lambda t: ("center", y(t))
        )
        .fx(fadein, 0.5)
        .fx(fadeout, 0.5)
    )


# -----------------------------------
# Animation Map
# -----------------------------------

ANIMATIONS = {

    "none": none,

    "fade": fade,

    "slide_up": slide_up,

    "slide_down": slide_down,

    "zoom_in": zoom_in,

    "zoom_out": zoom_out,

    "bounce": bounce,

}