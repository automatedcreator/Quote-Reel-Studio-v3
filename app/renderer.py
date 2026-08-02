import random

from moviepy.editor import (
    VideoFileClip,
    CompositeVideoClip,
    ColorClip,
    ImageClip,
)

WIDTH = 1080
HEIGHT = 1920
FPS = 30


def render_reel(video_path, quote_image, output_path):

    video = VideoFileClip(video_path)

    if video.duration > 20:
        start = random.uniform(0, video.duration - 20)
        video = video.subclip(start, start + 20)

    if video.w / video.h < WIDTH / HEIGHT:
        video = video.resize(width=WIDTH)
    else:
        video = video.resize(height=HEIGHT)

    video = video.crop(
        x_center=video.w / 2,
        y_center=video.h / 2,
        width=WIDTH,
        height=HEIGHT
    )

    duration = video.duration

    # Cinematic Zoom
    video = video.resize(
        lambda t: 1 + (0.08 * (t / duration))
    )

    video = video.crop(
        x_center=lambda t: video.w * (1 + (0.08 * (t / duration))) / 2,
        y_center=lambda t: video.h * (1 + (0.08 * (t / duration))) / 2,
        width=WIDTH,
        height=HEIGHT
    )

    # Overlay
    overlay = (
        ColorClip((WIDTH, HEIGHT), color=(0, 0, 0))
        .set_duration(duration)
        .set_opacity(0.30)
    )

    # Premium Slide-Up Animation
quote = (
    ImageClip(quote_image)
    .set_duration(duration)
    .set_position(lambda t: ("center", 100 - min(t * 80, 80)))
    .fadein(0.8)
    .fadeout(0.8)
)

    final = CompositeVideoClip([
        video,
        overlay,
        quote
    ])

    final.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        threads=4
    )

    video.close()
    final.close()