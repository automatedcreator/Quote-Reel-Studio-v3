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

    # Load video
    video = VideoFileClip(video_path)

    # Random 20-second clip
    if video.duration > 20:
        start = random.uniform(0, video.duration - 20)
        video = video.subclip(start, start + 20)

    # Better resize
    if video.w / video.h < WIDTH / HEIGHT:
        video = video.resize(width=WIDTH)
    else:
        video = video.resize(height=HEIGHT)

    # Center crop
    video = video.crop(
        x_center=video.w / 2,
        y_center=video.h / 2,
        width=WIDTH,
        height=HEIGHT
    )

    # Slow cinematic zoom (Ken Burns)
    duration = video.duration

    video = video.resize(
        lambda t: 1 + (0.08 * (t / duration))
    )

    video = video.crop(
        x_center=lambda t: video.w * (1 + (0.08 * (t / duration))) / 2,
        y_center=lambda t: video.h * (1 + (0.08 * (t / duration))) / 2,
        width=WIDTH,
        height=HEIGHT
    )

    # Dark overlay
    overlay = (
        ColorClip((WIDTH, HEIGHT), color=(0, 0, 0))
        .set_duration(duration)
        .set_opacity(0.30)
    )

    # Quote
    quote = (
        ImageClip(quote_image)
        .set_duration(duration)
        .set_position("center")
    )

    # Final
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