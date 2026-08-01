"""
Quote Loader
Supports:
- Excel (.xlsx)
- CSV (.csv)
"""

from pathlib import Path
import pandas as pd


SUPPORTED_EXTENSIONS = {".xlsx", ".csv"}


def load_quotes(file_path):
    """
    Load quotes from an Excel or CSV file.
    Returns a list of strings.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {file_path.suffix}"
        )

    if file_path.suffix.lower() == ".xlsx":
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

    quotes = (
        df.iloc[:, 0]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    quotes = [q for q in quotes if q]

    return quotes


if __name__ == "__main__":
    print("Quote Loader Ready")
