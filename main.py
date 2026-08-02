from pathlib import Path

from app.quotes import load_quotes
from app.typography import create_quote_image
from app.renderer import render_reel


def main():

    quotes = load_quotes("quotes/Simple Quotes.xlsx")

    videos = list(Path("videos").glob("*"))

    if len(videos) == 0:
        raise Exception("No videos found inside videos folder.")

    Path("output").mkdir(exist_ok=True)

    print(f"Found {len(quotes)} quotes")
    print(f"Found {len(videos)} videos\n")

    for i, quote in enumerate(quotes):

        image = create_quote_image(quote)

        video = videos[i % len(videos)]

        output_file = f"output/reel_{i+1:03d}.mp4"

        print(f"Generating {output_file}")

        render_reel(
            str(video),
            image,
            output_file
        )

    print("\n🎉 DONE!")
    print("All reels saved in output/")


if __name__ == "__main__":
    main()