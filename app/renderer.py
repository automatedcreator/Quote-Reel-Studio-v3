import random

from moviepy.editor import (
    VideoFileClip,
    CompositeVideoClip,
    ColorClip,
    ImageClip
)

from app.config import WIDTH, HEIGHT, FPS


CLIP_DURATION = 20


def prepare_video(video_path):

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


def build_overlay(duration):

    return (
        ColorClip(
            (WIDTH, HEIGHT),
            color=(0, 0, 0)
        )
        .set_duration(duration)
        .set_opacity(0.35)
    )


def build_quote(image_path, duration):

    return (
        ImageClip(image_path)
        .set_duration(duration)
        .set_position("center")
        .fadein(0.6)
        .fadeout(0.6)
    )
    def render_reel(
    video_path,
    quote_image,
    output_path,
):

    video = prepare_video(video_path)

    overlay = build_overlay(
        video.duration
    )

    quote = build_quote(
        quote_image,
        video.duration
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