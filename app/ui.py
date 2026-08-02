import os
import shutil
import zipfile
from pathlib import Path

import gradio as gr

from app.quotes import load_quotes
from app.typography import create_quote_image
from app.renderer import render_reel
from app.themes import list_themes


# --------------------------------------------------
# Main Generator
# --------------------------------------------------

def generate_reels(
    excel_file,
    video_files,
    theme_name,
):

    if excel_file is None:
        raise gr.Error("Upload Excel File")

    if not video_files:
        raise gr.Error("Upload at least one video")

    shutil.rmtree("quotes", ignore_errors=True)
    shutil.rmtree("videos", ignore_errors=True)
    shutil.rmtree("output", ignore_errors=True)

    os.makedirs("quotes", exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    os.makedirs("output", exist_ok=True)

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

    if len(quotes) == 0:
        raise gr.Error("No Quotes Found")

    if len(videos) == 0:
        raise gr.Error("No Videos Found")

    for i, quote in enumerate(quotes):

        image = create_quote_image(
            quote,
            theme_name=theme_name
        )

        render_reel(
            str(videos[i % len(videos)]),
            image,
            f"output/reel_{i+1:03d}.mp4"
        )
            # -------------------------------
    # Create ZIP
    # -------------------------------

    zip_path = "output/reels.zip"

    with zipfile.ZipFile(zip_path, "w") as zipf:

        for file in Path("output").glob("*.mp4"):
            zipf.write(file, arcname=file.name)

    return zip_path


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
            label="🎥 Background Videos",
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

    title="🎬 Quote Reel Studio v1.1",

    description="""
Generate premium Instagram quote reels.

Workflow

1. Upload Quotes Excel

2. Upload Videos

3. Select Theme

4. Generate

5. Download ZIP
"""

)


if __name__ == "__main__":

    demo.launch(
        share=True
    )