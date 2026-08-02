import random

from moviepy.editor import (
    VideoFileClip,
    CompositeVideoClip,
    ColorClip,
    ImageClip,
)

from app.config import WIDTH, HEIGHT, FPS
from app.themes import get_theme

CLIP_DURATION = 20


def prepare_video(video_path, theme):

    video = VideoFileClip(video_path)

    if video.duration > CLIP_DURATION:

        start = random.uniform(
            0,
            video.duration - CLIP_DURATION
        )

        video = video.subclip(
            start,
            start + CLIP_DURATION
        )

    video = video.resize(height=HEIGHT)

    if video.w > WIDTH:

        video = video.crop(
            x_center=video.w / 2,
            width=WIDTH
        )

    return video


def build_overlay(duration, theme):

    return (
        ColorClip(
            (WIDTH, HEIGHT),
            color=(0, 0, 0)
        )
        .set_duration(duration)
        .set_opacity(
            theme["overlay_opacity"]
        )
    )


def build_quote(image_path, duration, theme):

    animation = theme["animation"]

    clip = (
        ImageClip(image_path)
        .set_duration(duration)
    )

    if animation == "slide_up":

        clip = clip.set_position(
            lambda t: (
                "center",
                HEIGHT * 0.75 - min(t * 120, 120)
            )
        )

    elif animation == "slide_down":

        clip = clip.set_position(
            lambda t: (
                "center",
                HEIGHT * 0.10 + min(t * 120, 120)
            )
        )

    else:

        clip = clip.set_position("center")

    clip = (
        clip
        .fadein(0.7)
        .fadeout(0.7)
    )

    return clip


def render_reel(
    video_path,
    quote_image,
    output_path,
    theme_name="apple",
):

    theme = get_theme(theme_name)

    video = prepare_video(
        video_path,
        theme
    )

    overlay = build_overlay(
        video.duration,
        theme
    )

    quote = build_quote(
        quote_image,
        video.duration,
        theme
    )

    final = CompositeVideoClip(
        [
            video,
            overlay,
            quote
        ],
        size=(WIDTH, HEIGHT)
    )

    final.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="medium"
    )

    final.close()
    video.close()