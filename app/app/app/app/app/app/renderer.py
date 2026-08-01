"""
Video Renderer
"""

from moviepy.editor import (
    VideoFileClip,
    CompositeVideoClip,
    ColorClip,
    ImageClip,
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


def create_quote_layer(image_path, duration):

    return (
        ImageClip(str(image_path))
        .set_duration(duration)
        .set_position("center")
    )


def render_reel(
    video_path,
    quote_image,
    output_path
):

    video = prepare_video(video_path)

    overlay = create_overlay(video.duration)

    quote = create_quote_layer(
        quote_image,
        video.duration
    )

    final = CompositeVideoClip([
        video,
        overlay,
        quote
    ])

    final.write_videofile(
        str(output_path),
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )

    return output_path
