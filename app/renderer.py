from moviepy.editor import ( random
    VideoFileClip,
    CompositeVideoClip,
    ColorClip,
    ImageClip
)

WIDTH = 1080
HEIGHT = 1920


def render_reel(video_path, quote_image, output_path):

    video = VideoFileClip(video_path)

if video.duration > 20:
    start = random.randint(0, int(video.duration - 20))
    video = video.subclip(start, start + 20)

video = video.resize(height=HEIGHT)

    if video.w > WIDTH:
        video = video.crop(
            x_center=video.w / 2,
            width=WIDTH
        )

    overlay = (
        ColorClip(
            (WIDTH, HEIGHT),
            color=(0, 0, 0)
        )
        .set_duration(video.duration)
        .set_opacity(0.35)
    )

    quote = (
        ImageClip(quote_image)
        .set_duration(video.duration)
        .set_position("center")
    )

    final = CompositeVideoClip([
        video,
        overlay,
        quote
    ])

    final.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )