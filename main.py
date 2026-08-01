from pathlib import Path

from app.quotes import load_quotes
from app.typography import create_quote_image
from app.renderer import render_reel


def main():

    quotes = load_quotes("quotes/Simple Quotes.xlsx")

    videos = list(Path("videos").glob("*"))

    Path("output").mkdir(exist_ok=True)

    for i, quote in enumerate(quotes):

        image = create_quote_image(quote)

        video = videos[i % len(videos)]

        render_reel(
            str(video),
            image,
            f"output/reel_{i+1:03d}.mp4"
        )

        print(f"✅ Reel {i+1} Created")

    print("\n🎉 All reels generated")


if __name__ == "__main__":
    main()