import os
import shutil
import zipfile
from pathlib import Path

import gradio as gr

from app.quotes import load_quotes
from app.typography import create_quote_image
from app.renderer import render_reel


def generate_reels(excel_file, video_files):

    # ----------------------------
    # Validate Inputs
    # ----------------------------

    if excel_file is None:
        raise gr.Error("Please upload an Excel file.")

    if not video_files:
        raise gr.Error("Please upload at least one video.")

    # ----------------------------
    # Prepare folders
    # ----------------------------

    shutil.rmtree("quotes", ignore_errors=True)
    shutil.rmtree("videos", ignore_errors=True)
    shutil.rmtree("output", ignore_errors=True)

    os.makedirs("quotes", exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # ----------------------------
    # Copy uploaded files
    # ----------------------------

    shutil.copy(excel_file.name, "quotes/Simple Quotes.xlsx")

    for video in video_files:
        shutil.copy(video.name, f"videos/{Path(video.name).name}")

    # ----------------------------
    # Load Quotes
    # ----------------------------

    try:
        quotes = load_quotes("quotes/Simple Quotes.xlsx")
    except Exception as e:
        raise gr.Error(f"Unable to read Excel file.\n\n{e}")

    if len(quotes) == 0:
        raise gr.Error("No quotes found inside the Excel file.")

    videos = list(Path("videos").glob("*"))

    if len(videos) == 0:
        raise gr.Error("No videos found.")

    # ----------------------------
    # Generate Reels
    # ----------------------------

    for i, quote in enumerate(quotes):

        image = create_quote_image(quote)

        try:

            render_reel(
                str(videos[i % len(videos)]),
                image,
                f"output/reel_{i+1:03d}.mp4"
            )

        except Exception as e:
            raise gr.Error(f"Error generating Reel {i+1}\n\n{e}")

    # ----------------------------
    # Create ZIP
    # ----------------------------

    zip_path = "output/reels.zip"

    with zipfile.ZipFile(zip_path, "w") as zipf:

        for file in Path("output").glob("*.mp4"):
            zipf.write(file, arcname=file.name)

    return zip_path


demo = gr.Interface(
    fn=generate_reels,
    inputs=[
        gr.File(
            label="📄 Upload Excel File"
        ),
        gr.File(
            label="🎥 Upload Videos",
            file_count="multiple"
        ),
    ],
    outputs=gr.File(
        label="📥 Download Generated Reels"
    ),
    title="🎬 Quote Reel Studio v1.0",
    description="""
Generate multiple Instagram quote reels automatically.

Steps:

1. Upload your Excel file.
2. Upload one or more background videos.
3. Click Submit.
4. Download reels.zip.
"""
)


if __name__ == "__main__":
    demo.launch(share=True)