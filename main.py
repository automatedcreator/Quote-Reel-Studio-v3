from pathlib import Path

from app.quotes import load_quotes
from app.typography import create_quote_image
from app.renderer import render_reel


def main():

    quotes = load_quotes("quotes/Simple Quotes.xlsx")

    quote = quotes[0]

    image = create_quote_image(quote)

    video = list(Path("videos").glob("*"))[0]

    Path("output").mkdir(exist_ok=True)

    render_reel(
        str(video),
        image,
        "output/reel.mp4"
    )

    print("\n✅ Reel Created")
    print("output/reel.mp4")


if __name__ == "__main__":
    main()