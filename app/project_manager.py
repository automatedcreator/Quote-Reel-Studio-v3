"""
Project Manager
"""

import json
import shutil
from pathlib import Path
from datetime import datetime


PROJECTS_DIR = Path("Projects")


def ensure_projects():

    PROJECTS_DIR.mkdir(
        exist_ok=True
    )


def create_project(project_name):

    ensure_projects()

    project = PROJECTS_DIR / project_name

    (project / "Videos").mkdir(
        parents=True,
        exist_ok=True
    )

    (project / "Quotes").mkdir(
        exist_ok=True
    )

    (project / "Reels").mkdir(
        exist_ok=True
    )

    (project / "Captions").mkdir(
        exist_ok=True
    )

    (project / "Thumbnails").mkdir(
        exist_ok=True
    )

    return project


def save_project(

    project_name,
    theme,
    total_reels

):

    project = create_project(
        project_name
    )

    data = {

        "project": project_name,

        "theme": theme,

        "total_reels": total_reels,

        "created": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

    }

    with open(

        project / "project.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )

    return project


def copy_quotes(

    excel_file,

    project_name

):

    project = create_project(
        project_name
    )

    dst = project / "Quotes" / Path(excel_file).name

    shutil.copy(
        excel_file,
        dst
    )

    return dst


def copy_video(

    video,

    project_name

):

    project = create_project(
        project_name
    )

    dst = project / "Videos" / Path(video).name

    shutil.copy(
        video,
        dst
    )

    return dst


def copy_reel(

    reel,

    project_name

):

    project = create_project(
        project_name
    )

    dst = project / "Reels" / Path(reel).name

    shutil.copy(
        reel,
        dst
    )

    return dst


def list_projects():

    ensure_projects()

    return sorted(

        [

            p.name

            for p in PROJECTS_DIR.iterdir()

            if p.is_dir()

        ]

    )


def load_project(project_name):

    file = (

        PROJECTS_DIR

        / project_name

        / "project.json"

    )

    if not file.exists():

        return None

    with open(

        file,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)