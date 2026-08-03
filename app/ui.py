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


def generate_reels(

    excel_file,

    video_files,

    theme_name,

    preset_name,

):

    start_time = time.time()

    try:

        if excel_file is None:
            raise gr.Error("Upload Excel")

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

        if len(quotes) == 0:

            raise gr.Error("No Quotes Found")

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

            f"#{theme_name}"

        ]

        for i, quote in enumerate(quotes):

            image = create_quote_image(

                quote,

                theme_name=theme_name,

            )

            output = f"output/reel_{i+1:03d}.mp4"

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

                project

            )

            captions.append(

                quote

            )

            tracker.update()

            log(

                tracker.status()

            )
        create_summary(

            theme_name,

            len(quotes),

            project

        )

        create_caption_file(

            captions

        )

        create_hashtag_file(

            hashtags

        )

        save_stats(

            project,

            theme_name,

            len(quotes),

            start_time

        )

        finish_project()

        return export_zip()

    except Exception as e:

        error(

            str(e)

        )

        raise


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

        gr.Dropdown(

            choices=list_presets(),

            value="Apple Minimal",

            label="✨ Preset"

        ),

    ],

    outputs=[

        gr.File(

            label="📦 Download ZIP"

        )

    ],

    title="🎬 Quote Reel Studio v1.1",

    description="""

Generate Premium Instagram Reels

✅ Themes

✅ Premium Presets

✅ Typography Engine

✅ Project Manager

✅ Statistics

✅ ZIP Export

"""

)

if __name__ == "__main__":

    demo.launch(

        share=True

    )