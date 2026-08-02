import gradio as gr
import shutil
from pathlib import Path

from main import main


def generate(excel_file, video_files):

    # Clean old folders
    shutil.rmtree("quotes", ignore_errors=True)
    shutil.rmtree("videos", ignore_errors=True)

    Path("quotes").mkdir(exist_ok=True)
    Path("videos").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)

    # Copy Excel
    shutil.copy(excel_file, "quotes/Simple Quotes.xlsx")

    # Copy videos
    for video in video_files:
        shutil.copy(video, f"videos/{Path(video).name}")

    # Generate reels
    main()

    return "✅ All reels generated! Check the output folder."


demo = gr.Interface(
    fn=generate,
    inputs=[
        gr.File(label="Excel File"),
        gr.File(label="Videos", file_count="multiple")
    ],
    outputs="text",
    title="Quote Reel Studio v1.0"
)

if __name__ == "__main__":
    demo.launch()