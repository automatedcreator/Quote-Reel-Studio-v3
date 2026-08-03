import os
import shutil
import time
from pathlib import Path

import gradio as gr

from app.quotes import load_quotes
from app.typography import create_quote_image
from app.renderer import render_reel

from app.themes import list_themes
from app.presets import list_presets

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

from app.logger import (
    start_project,
    finish_project,
    log,
    error,
)

from app.progress import ProgressTracker
from app.stats import save_stats


# --------------------------------------------------
# Main Generator
# --------------------------------------------------

def generate_reels(

    excel_file,
    video_files,
    theme_name,
    preset_name,

):

    start_time = time.time()

    try:

        # ---------------------------------
        # Validation
        # ---------------------------------

        if excel_file is None:
            raise gr.Error("Please upload an Excel file.")

        if not video_files:
            raise gr.Error("Please upload at least one video.")

        # ---------------------------------
        # Clean Old Folders
        # ---------------------------------

        for folder in [

            "quotes",
            "videos",
            "output",

        ]:

            shutil.rmtree(
                folder,
                ignore_errors=True
            )

            os.makedirs(
                folder,
                exist_ok=True
            )

        # ---------------------------------
        # Copy Files
        # ---------------------------------

        excel_destination = (
            "quotes/Simple Quotes.xlsx"
        )

        shutil.copy(
            excel_file.name,
            excel_destination
        )

        for video in video_files:

            shutil.copy(

                video.name,

                f"videos/{Path(video.name).name}"

            )

        # ---------------------------------
        # Load Quotes & Videos
        # ---------------------------------

        quotes = load_quotes(
            excel_destination
        )

        videos = sorted(
            Path("videos").glob("*")
        )

        if len(quotes) == 0:
            raise gr.Error("No quotes found.")

        if len(videos) == 0:
            raise gr.Error("No videos found.")

        # ---------------------------------
        # Project Setup
        # ---------------------------------

        project = Path(
            excel_file.name
        ).stem

        tracker = ProgressTracker(
            len(quotes)
        )

        start_project(
            project,
            theme_name,
            len(quotes)
        )

        save_project(
            project,
            theme_name,
            len(quotes)
        )

        copy_quotes(
            excel_file.name,
            project
        )

        for video in video_files:

            copy_video(
                video.name,
                project
            )

        captions = []

        hashtags = [

            "#quotes",
            "#motivation",
            "#mindset",
            f"#{theme_name}",

        ]
        # ---------------------------------
        # Generate Reels
        # ---------------------------------

        for i, quote in enumerate(quotes):

            image = create_quote_image(

                quote,

                theme_name=theme_name,

                preset_name=preset_name,

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

                theme_name,

                preset_name,

            )

            copy_reel(

                output,

                project,

            )

            captions.append(

                quote

            )

            tracker.update()

            log(

                tracker.status()

            )

        # ---------------------------------
        # Export Files
        # ---------------------------------

        create_summary(

            theme_name,

            len(quotes),

            project,

        )

        create_caption_file(

            captions,

        )

        create_hashtag_file(

            hashtags,

        )

        save_stats(

            project,

            theme_name,

            len(quotes),

            start_time,

        )

        finish_project()

        return export_zip()

    except Exception as e:

        error(

            str(e)

        )

        raise gr.Error(

            str(e)

        )
# --------------------------------------------------
# Gradio UI
# --------------------------------------------------

demo = gr.Interface(

    fn=generate_reels,

    inputs=[

        gr.File(

            label="📄 Quotes Excel"

        ),

        gr.File(

            label="🎥 Videos",

            file_count="multiple",

        ),

        gr.Dropdown(

            choices=list_themes(),

            value="apple",

            label="🎨 Theme",

        ),

        gr.Dropdown(

            choices=list_presets(),

            value="Apple Minimal",

            label="✨ Preset",

        ),

    ],

    outputs=[

        gr.File(

            label="📦 Download ZIP"

        )

    ],

    title="🎬 Quote Reel Studio v3",

    description="""
Generate Premium Instagram Reels

✅ Multiple Themes
✅ Premium Presets
✅ Dynamic Typography
✅ Automatic Project Manager
✅ Progress Tracking
✅ Statistics
✅ ZIP Export
""",

    allow_flagging="never",

)


# --------------------------------------------------
# Launch
# --------------------------------------------------

if __name__ == "__main__":

    demo.launch(

        share=True,

        debug=False,

    )