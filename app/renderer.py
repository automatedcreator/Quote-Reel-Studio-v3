import random

from moviepy.editor import (
    VideoFileClip,
    CompositeVideoClip,
    ColorClip,
    ImageClip,
    vfx,
)

from app.config import WIDTH, HEIGHT, FPS
from app.themes import get_theme

CLIP_DURATION = 20


# ----------------------------------------------------
# Prepare Background Video
# ----------------------------------------------------

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

    brightness = theme.get(
        "brightness",
        1.0
    )

    if brightness != 1:

        video = video.fx(
            vfx.colorx,
            brightness
        )

    return video


# ----------------------------------------------------
# Overlay
# ----------------------------------------------------

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


# ----------------------------------------------------
# Quote Animation
# ----------------------------------------------------

def build_quote(image_path, duration, theme):

    clip = (

        ImageClip(image_path)

        .set_duration(duration)

    )

    animation = theme.get(
        "animation",
        "fade"
    )

    if animation == "fade":

        clip = (

            clip

            .fadein(0.8)

            .fadeout(0.8)

        )

    elif animation == "slide_up":

        clip = (

            clip

            .set_position(
                lambda t: (
                    "center",
                    HEIGHT * 0.60 - min(t * 100, 100)
                )
            )

            .fadein(0.5)

            .fadeout(0.5)

        )

    elif animation == "slide_down":

        clip = (

            clip

            .set_position(
                lambda t: (
                    "center",
                    HEIGHT * 0.40 + min(t * 100, 100)
                )
            )

            .fadein(0.5)

            .fadeout(0.5)

        )

    else:

        clip = clip.set_position("center")

    return clip


# ----------------------------------------------------
# Cinematic Zoom
# ----------------------------------------------------

def apply_ken_burns(video, theme):

    zoom_speed = theme.get(
        "zoom_speed",
        1.06
    )

    return video.resize(

        lambda t:

        1 +

        (

            (zoom_speed - 1)

            *

            t

            /

            video.duration

        )

    )


# ----------------------------------------------------
# Render Reel
# ----------------------------------------------------

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

    video = apply_ken_burns(
        video,
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

        preset="medium",

        threads=4,

    )

    final.close()

    video.close()