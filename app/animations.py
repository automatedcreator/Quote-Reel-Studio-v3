"""
Animation Engine
"""

from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout


def apply_fade(clip, duration=0.5):
    clip = fadein(clip, duration)
    clip = fadeout(clip, duration)
    return clip


def apply_quote_animation(clip):
    return apply_fade(clip, 0.6)