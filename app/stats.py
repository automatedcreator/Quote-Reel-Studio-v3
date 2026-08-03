"""
Statistics Manager
"""

import json
import time
from pathlib import Path
from datetime import datetime


OUTPUT_DIR = Path("output")


def ensure_output():

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )


def save_stats(

    project,

    theme,

    total_reels,

    start_time,

):

    ensure_output()

    end_time = time.time()

    total_time = end_time - start_time

    average = 0

    if total_reels > 0:

        average = total_time / total_reels

    stats = {

        "project": project,

        "theme": theme,

        "total_reels": total_reels,

        "total_time_seconds": round(
            total_time,
            2
        ),

        "average_time_per_reel": round(
            average,
            2
        ),

        "generated_on": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),

        "resolution": "1080x1920",

        "fps": 30,

        "status": "Completed"

    }

    with open(

        OUTPUT_DIR / "stats.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            stats,

            f,

            indent=4,

            ensure_ascii=False

        )

    return OUTPUT_DIR / "stats.json"