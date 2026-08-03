import random

from moviepy.editor import (

    VideoFileClip,

    CompositeVideoClip,

    ColorClip,

    ImageClip,

    vfx,

)

from app.config import (

    WIDTH,

    HEIGHT,

    FPS,

)

from app.themes import get_theme


CLIP_DURATION = 20


# ---------------------------------------------------
# Prepare Video
# ---------------------------------------------------

def prepare_video(

    video_path,

    theme,

):

    video = VideoFileClip(

        video_path

    )

    if video.duration > CLIP_DURATION:

        start = random.uniform(

            0,

            video.duration - CLIP_DURATION

        )

        video = video.subclip(

            start,

            start + CLIP_DURATION

        )

    video = video.resize(

        height=HEIGHT

    )

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
# Cinematic Zoom
# ---------------------------------------------------

def apply_zoom(

    clip,

    theme,

):

    zoom = theme.get(

        "zoom_speed",

        1.03

    )

    if zoom <= 1:

        return clip

    return clip.resize(

        lambda t:

        1 +

        (

            (zoom - 1)

            *

            (t / clip.duration)

        )

    )


# ---------------------------------------------------
# Vignette Overlay
# ---------------------------------------------------

def build_overlay(

    duration,

    theme,

):

    return (

        ColorClip(

            (WIDTH, HEIGHT),

            color=(0, 0, 0)

        )

        .set_duration(duration)

        .set_opacity(

            theme.get(

                "overlay_opacity",

                0.30

            )

        )

    )
# ---------------------------------------------------
# Premium Quote Animation
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

        ImageClip(

            image_path

        )

        .set_duration(

            duration

        )

    )

    # -------------------------
    # Fade
    # -------------------------

    if animation == "fade":

        clip = (

            clip

            .set_position(

                "center"

            )

            .fadein(

                0.7

            )

            .fadeout(

                0.7

            )

        )

    # -------------------------
    # Slide Up
    # -------------------------

    elif animation == "slide_up":

        clip = clip.set_position(

            lambda t: (

                "center",

                HEIGHT * 0.68

                -

                min(

                    t * 110,

                    110

                )

            )

        )

        clip = (

            clip

            .fadein(

                0.6

            )

            .fadeout(

                0.6

            )

        )

    # -------------------------
    # Slide Down
    # -------------------------

    elif animation == "slide_down":

        clip = clip.set_position(

            lambda t: (

                "center",

                HEIGHT * 0.22

                +

                min(

                    t * 110,

                    110

                )

            )

        )

        clip = (

            clip

            .fadein(

                0.6

            )

            .fadeout(

                0.6

            )

        )

    # -------------------------
    # Zoom
    # -------------------------

    elif animation == "zoom":

        clip = (

            clip

            .resize(

                lambda t:

                0.95

                +

                min(

                    t * 0.02,

                    0.08

                )

            )

            .set_position(

                "center"

            )

            .fadein(

                0.6

            )

            .fadeout(

                0.6

            )

        )

    # -------------------------
    # Floating
    # -------------------------

    elif animation == "float":

        clip = clip.set_position(

            lambda t: (

                "center",

                HEIGHT * 0.50

                +

                12

                *

                __import__("math").sin(

                    t * 1.5

                )

            )

        )

        clip = (

            clip

            .fadein(

                0.6

            )

            .fadeout(

                0.6

            )

        )

    else:

        clip = (

            clip

            .set_position(

                "center"

            )

            .fadein(

                0.6

            )

            .fadeout(

                0.6

            )

        )

    return clip    
# ---------------------------------------------------
# Main Renderer
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

    # -------------------------
    # Background Video
    # -------------------------

    video = prepare_video(

        video_path,

        theme

    )

    video = apply_zoom(

        video,

        theme

    )

    # -------------------------
    # Overlay
    # -------------------------

    overlay = build_overlay(

        video.duration,

        theme

    )

    # -------------------------
    # Quote
    # -------------------------

    quote = build_quote(

        quote_image,

        video.duration,

        theme

    )

    # -------------------------
    # Final Composition
    # -------------------------

    final = CompositeVideoClip(

        [

            video,

            overlay,

            quote

        ],

        size=(

            WIDTH,

            HEIGHT

        )

    )

    # -------------------------
    # Export
    # -------------------------

    final.write_videofile(

        output_path,

        fps=FPS,

        codec="libx264",

        audio_codec="aac",

        preset="medium",

        threads=4,

        bitrate="8000k",

        ffmpeg_params=[

            "-movflags",

            "+faststart"

        ],

        logger=None

    )

    # -------------------------
    # Cleanup
    # -------------------------

    final.close()

    quote.close()

    overlay.close()

    video.close()    