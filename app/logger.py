"""
Logger
"""

from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "generation_log.txt"
ERROR_FILE = LOG_DIR / "error_log.txt"


def timestamp():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def log(message):

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"[{timestamp()}] {message}\n"
        )


def error(message):

    with open(
        ERROR_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"[{timestamp()}] {message}\n"
        )


def start_project(
    project,
    theme,
    total_reels,
):

    log("=" * 60)
    log("PROJECT STARTED")
    log(f"Project : {project}")
    log(f"Theme   : {theme}")
    log(f"Reels   : {total_reels}")
    log("=" * 60)


def finish_project():

    log("=" * 60)
    log("PROJECT COMPLETED")
    log("=" * 60)