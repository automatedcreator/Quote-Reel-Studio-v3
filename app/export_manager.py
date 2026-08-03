"""
Export Manager
"""

import shutil
import zipfile
from pathlib import Path
from datetime import datetime


OUTPUT_DIR = Path("output")


def ensure_output():

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )


def get_reels():

    ensure_output()

    return sorted(
        OUTPUT_DIR.glob("*.mp4")
    )


def export_zip(

    zip_name="reels.zip"

):

    ensure_output()

    zip_path = OUTPUT_DIR / zip_name

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for reel in get_reels():

            zipf.write(
                reel,
                arcname=reel.name
            )

    return str(zip_path)


def export_selected(

    files,

    zip_name="selected_reels.zip"

):

    ensure_output()

    zip_path = OUTPUT_DIR / zip_name

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for file in files:

            file = Path(file)

            if file.exists():

                zipf.write(
                    file,
                    arcname=file.name
                )

    return str(zip_path)


def create_summary(

    theme,

    total_reels,

    project_name="Quote Reel Studio"

):

    ensure_output()

    summary = OUTPUT_DIR / "summary.txt"

    with open(
        summary,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f"""
Project : {project_name}

Theme : {theme}

Total Reels : {total_reels}

Generated :
{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}
"""
        )

    return str(summary)


def create_caption_file(

    captions

):

    ensure_output()

    file = OUTPUT_DIR / "captions.txt"

    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:

        for i, caption in enumerate(
            captions,
            start=1
        ):

            f.write(
                f"Reel {i:03d}\n"
            )

            f.write(
                caption.strip()
            )

            f.write("\n\n")

    return str(file)


def create_hashtag_file(

    hashtags

):

    ensure_output()

    file = OUTPUT_DIR / "hashtags.txt"

    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(hashtags)
        )

    return str(file)


def copy_thumbnail(

    image_path,

    reel_number

):

    ensure_output()

    dst = OUTPUT_DIR / f"thumbnail_{reel_number:03d}.png"

    shutil.copy(
        image_path,
        dst
    )

    return str(dst)