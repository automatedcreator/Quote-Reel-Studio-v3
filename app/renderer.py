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
    VIDEO_BITRATE,
)

# ----------------------------------------
# Settings
# ----------------------------------------

CLIP_DURATION = 20

ZOOM_AMOUNT = 0.08

OVERLAY_OPACITY = 0.30

BRIGHTNESS = 1.08

FADE_DURATION = 0.8

PAN_AMOUNT = 25


# ----------------------------------------
# Helpers
# ----------------------------------------

def random_subclip(video):

    if video.duration <= CLIP_DURATION:
        return video

    start = random.uniform(
        0,
        video.duration - CLIP_DURATION
    )

    return video.subclip(
        start,
        start + CLIP_DURATION
    )


def smart_resize(video):

    target_ratio = WIDTH / HEIGHT
    video_ratio = video.w / video.h

    if video_ratio < target_ratio:

        video = video.resize(width=WIDTH)

    else:

        video = video.resize(height=HEIGHT)

    return video.crop(
        x_center=video.w / 2,
        y_center=video.h / 2,
        width=WIDTH,
        height=HEIGHT,
    )


def cinematic_motion(video):

    duration = video.duration

    def zoom(t):

        return 1 + ZOOM_AMOUNT * (t / duration)

    video = video.resize(zoom)

    def x_pos(t):

        scale = zoom(t)

        return (
            video.w * scale / 2
            + PAN_AMOUNT
            * ((t / duration) - 0.5)
        )

    def y_pos(t):

        scale = zoom(t)

        return (
            video.h * scale / 2
        )

    return video.crop(
        x_center=x_pos,
        y_center=y_pos,
        width=WIDTH,
        height=HEIGHT,
    )


def build_overlay(duration):

    return (
        ColorClip(
            (WIDTH, HEIGHT),
            color=(0, 0, 0)
        )
        .set_duration(duration)
        .set_opacity(OVERLAY_OPACITY)
    )


def build_quote(quote_image, duration):

    return (
        ImageClip(quote_image)
        .set_duration(duration)
        .set_position(
            lambda t: (
                "center",
                100 - min(t * 80, 80)
            )
        )
        .fadein(FADE_DURATION)
        .fadeout(FADE_DURATION)
    )


def prepare_video(video_path):

    video = VideoFileClip(video_path)

    video = random_subclip(video)

    video = smart_resize(video)

    video = cinematic_motion(video)

    video = video.fx(
        vfx.colorx,
        BRIGHTNESS
    )

    return video
    # ----------------------------------------
# Main Renderer
# ----------------------------------------

def render_reel(
    video_path,
    quote_image,
    output_path,
):

    video = prepare_video(video_path)

    duration = video.duration

    overlay = build_overlay(duration)

    quote = build_quote(
        quote_image,
        duration,
    )

    final = CompositeVideoClip(
        [
            video,
            overlay,
            quote,
        ],
        size=(WIDTH, HEIGHT),
    )

    final = final.set_duration(duration)

    final.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate=VIDEO_BITRATE,
        preset="medium",
        threads=4,
        temp_audiofile="temp/temp-audio.m4a",
        remove_temp=True,
        logger=None,
    )

    # Cleanup
    try:
        quote.close()
    except:
        pass

    try:
        overlay.close()
    except:
        pass

    try:
        final.close()
    except:
        pass

    try:
        video.close()
    except:
        pass