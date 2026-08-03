import os
import shutil
from pathlib import Path

import gradio as gr

from app.quotes import load_quotes
from app.typography import create_quote_image
from app.renderer import render_reel
from app.themes import list_themes

from app.export_manager import (
    export_zip,
    create_summary,
    create_caption_file,
    create_hashtag_file,
)

from app.project_manager import (
    save_project,
    copy_quotes,
    copy_video,
    copy_reel,
)


# --------------------------------------------------
# Generator
# --------------------------------------------------

def generate_reels(

    excel_file,

    video_files,

    theme_name,

):

    if excel_file is None:
        raise gr.Error("Upload Excel File")

    if not video_files:
        raise gr.Error("Upload Videos")

    shutil.rmtree(
        "quotes",
        ignore_errors=True
    )

    shutil.rmtree(
        "videos",
        ignore_errors=True
    )

    shutil.rmtree(
        "output",
        ignore_errors=True
    )

    os.makedirs(
        "quotes",
        exist_ok=True
    )

    os.makedirs(
        "videos",
        exist_ok=True
    )

    os.makedirs(
        "output",
        exist_ok=True
    )

    shutil.copy(

        excel_file.name,

        "quotes/Simple Quotes.xlsx"

    )

    for video in video_files:

        shutil.copy(

            video.name,

            f"videos/{Path(video.name).name}"

        )

    quotes = load_quotes(
        "quotes/Simple Quotes.xlsx"
    )

    videos = list(
        Path("videos").glob("*")
    )

    if not quotes:
        raise gr.Error("No Quotes Found")

    project_name = Path(
        excel_file.name
    ).stem

    save_project(

        project_name,

        theme_name,

        len(quotes)

    )

    copy_quotes(

        excel_file.name,

        project_name

    )

    for video in video_files:

        copy_video(

            video.name,

            project_name

        )

    captions = []

    hashtags = [

        "#quotes",

        "#motivation",

        "#mindset",

        f"#{theme_name}"

    ]

    for i, quote in enumerate(quotes):

        image = create_quote_image(

            quote,

            theme_name=theme_name

        )

        output = (

            f"output/reel_{i+1:03d}.mp4"

        )

        render_reel(

            str(

                videos[
                    i % len(videos)
                ]

            ),

            image,

            output,

            theme_name

        )

        copy_reel(

            output,

            project_name

        )

        captions.append(

            quote

        )

    create_summary(

        theme_name,

        len(quotes),

        project_name

    )

    create_caption_file(

        captions

    )

    create_hashtag_file(

        hashtags

    )

    return export_zip()


# --------------------------------------------------
# UI
# --------------------------------------------------

demo = gr.Interface(

    fn=generate_reels,

    inputs=[

        gr.File(

            label="📄 Quotes Excel"

        ),

        gr.File(

            label="🎥 Videos",

            file_count="multiple"

        ),

        gr.Dropdown(

            choices=list_themes(),

            value="apple",

            label="🎨 Theme"

        ),

    ],

    outputs=[

        gr.File(

            label="📦 Download ZIP"

        )

    ],

    title="🎬 Quote Reel Studio v1.2",

    description="""

Generate premium Instagram quote reels.

• Upload Excel

• Upload Videos

• Select Theme

• Generate

• Download ZIP

"""

)


if __name__ == "__main__":

    demo.launch(
        share=True
    )