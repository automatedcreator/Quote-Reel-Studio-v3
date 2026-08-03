"""
Quote Reel Studio Launcher
"""

import webbrowser
import threading
import time

from app.ui import demo


def open_browser():

    time.sleep(2)

    webbrowser.open(
        "http://127.0.0.1:7860"
    )


if __name__ == "__main__":

    threading.Thread(
        target=open_browser,
        daemon=True
    ).start()

    demo.launch(
        share=False,
        inbrowser=False
    )