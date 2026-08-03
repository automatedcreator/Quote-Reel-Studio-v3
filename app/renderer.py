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


# ---------------------------------------------------
# Prepare Video
# ---------------------------------------------------

def prepare_video(

    video_path,

    theme,

):

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


# ---------------------------------------------------
# Overlay
# ---------------------------------------------------

def build_overlay(

    duration,

    theme,

):

    overlay = ColorClip(

        (WIDTH, HEIGHT),

        color=(0, 0, 0)

    )

    overlay = overlay.set_duration(duration)

    overlay = overlay.set_opacity(

        theme.get(

            "overlay_opacity",

            0.30

        )

    )

    return overlay


# ---------------------------------------------------
# Quote Animation
# ---------------------------------------------------

def build_quote(

    image_path,

    duration,

    theme,

):

    animation = theme.get(

        "animation",

        "fade"

    )

    clip = (

        ImageClip(image_path)

        .set_duration(duration)

    )

    if animation == "slide_up":

        clip = clip.set_position(

            lambda t: (

                "center",

                HEIGHT * 0.62 - min(

                    t * 90,

                    90

                )

            )

        )

    elif animation == "slide_down":

        clip = clip.set_position(

            lambda t: (

                "center",

                HEIGHT * 0.35 + min(

                    t * 90,

                    90

                )

            )

        )

    elif animation == "zoom":

        clip = clip.resize(

            lambda t: 0.92 + min(

                t * 0.03,

                0.08

            )

        )

        clip = clip.set_position("center")

    else:

        clip = clip.set_position("center")

    clip = (

        clip

        .fadein(0.6)

        .fadeout(0.6)

    )

    return clip


# ---------------------------------------------------
# Render Reel
# ---------------------------------------------------

def render_reel(

    video_path,

    quote_image,

    output_path,

    theme_name="apple",

    preset_name=None,

):

    theme = get_theme(

        theme_name,

        preset_name

    )

    video = prepare_video(

        video_path,

        theme

    )

    zoom = theme.get(

        "zoom_speed",

        1.03

    )

    if zoom > 1:

        video = video.resize(

            lambda t:

            1 +

            (

                (zoom - 1)

                * t

                / video.duration

            )

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

        logger=None

    )

    final.close()

    video.close()