"""
Video Renderer
"""

from moviepy.editor import (
    VideoFileClip,
    CompositeVideoClip,
    ColorClip,
)

WIDTH = 1080
HEIGHT = 1920


def prepare_video(video_path):

    clip = VideoFileClip(str(video_path))

    clip = clip.resize(height=HEIGHT)

    if clip.w > WIDTH:

        clip = clip.crop(
            x_center=clip.w / 2,
            width=WIDTH
        )

    else:

        clip = clip.resize(width=WIDTH)

    return clip.set_position("center")


def create_overlay(duration, opacity=0.35):

    return (
        ColorClip(
            size=(WIDTH, HEIGHT),
            color=(0, 0, 0)
        )
        .set_duration(duration)
        .set_opacity(opacity)
    )
