"""
Quote Reel Studio Pro
Main Entry Point
"""

from pathlib import Path

from app.quotes import load_quotes
from app.utils import random_video


def main():

    print("=" * 50)
    print("Quote Reel Studio Pro")
    print("=" * 50)

    quote_files = list(Path("quotes").glob("*.xlsx"))

    if not quote_files:
        print("❌ No Excel file found in quotes/")
        return

    quotes = load_quotes(quote_files[0])

    print(f"✅ Quotes Loaded : {len(quotes)}")

    try:
        video = random_video("videos")
        print(f"✅ Sample Video : {video.name}")
    except Exception:
        print("⚠️ No videos found in videos/")

    print("\n✅ Project Ready")


if __name__ == "__main__":
    main()
