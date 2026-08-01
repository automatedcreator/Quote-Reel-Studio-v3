from app.quotes import load_quotes
from app.typography import create_quote_image


def main():

    quotes = load_quotes("quotes/Simple Quotes.xlsx")

    create_quote_image(quotes[0])

    print("✅ Quote image created")


if __name__ == "__main__":
    main()