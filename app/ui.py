import os
import shutil
import zipfile
from pathlib import Path

import gradio as gr

from app.quotes import load_quotes
from app.typography import create_quote_image
from app.renderer import render_reel


def generate_reels(excel_file, video_files, progress=gr.Progress()):

    # Clean old folders
    shutil.rmtree("quotes", ignore_errors=True)
    shutil.rmtree("videos", ignore_errors=True)
    shutil.rmtree("output", ignore_errors=True)

    os.makedirs("quotes", exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # Copy Excel
    shutil.copy(excel_file.name, "quotes/Simple Quotes.xlsx")

    # Copy Videos
    for video in video_files:
        shutil.copy(video.name, f"videos/{Path(video.name).name}")

    quotes = load_quotes("quotes/Simple Quotes.xlsx")
    videos = list(Path("videos").glob("*"))

    total = len(quotes)

    for i, quote in enumerate(quotes):

        progress(
            (i + 1) / total,
            desc=f"Generating Reel {i+1}/{total}"
        )

        image = create_quote_image(quote)

        render_reel(
            str(videos[i % len(videos)]),
            image,
            f"output/reel_{i+1:03d}.mp4"
        )

    # Create ZIP
    zip_path = "output/reels.zip"

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in Path("output").glob("*.mp4"):
            zipf.write(file, arcname=file.name)

    return zip_path


demo = gr.Interface(
    fn=generate_reels,
    inputs=[
        gr.File(label="Excel File"),
        gr.File(
            label="Videos",
            file_count="multiple"
        ),
    ],
    outputs=gr.File(label="Download Reels ZIP"),
    title="Quote Reel Studio v1.0",
    description="Upload an Excel file and one or more videos to generate reels."
)


if __name__ == "__main__":
    demo.launch(share=True)