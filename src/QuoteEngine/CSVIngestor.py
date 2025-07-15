"""
Ingestor for Comma Separated Values (.csv) files.
"""

import pandas as pd
from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class CSVIngestor(IngestorInterface):
    """
    Concrete ingestor for CSV files.

    It assumes the CSV file has 'body' and 'author' columns.
    Uses pandas for robust CSV parsing.
    """

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parses a .csv file and extracts quotes.

        Assumes the CSV has 'body' and 'author' columns.

        Args:
            path (str): The path to the .csv file.

        Returns:
            List[QuoteModel]: A list of QuoteModel objects.

        Raises:
            Exception: If the file cannot be read or required columns are missing.
        """
        if not cls.can_ingest(path):
            raise Exception(f"Cannot ingest file type for {path}. Expected .csv")

        quotes = []
        try:
            # Use pandas to read CSV, which handles various delimiters, quotes, etc.
            df = pd.read_csv(path)

            # Check if 'body' and 'author' columns exist
            if 'body' not in df.columns or 'author' not in df.columns:
                raise ValueError(f"CSV file {path} must contain 'body' and 'author' columns.")

            for index, row in df.iterrows():
                body = str(row['body']).strip()
                author = str(row['author']).strip()
                if body and author: # Ensure both parts are non-empty
                    quotes.append(QuoteModel(body, author))
                else:
                    print(f"Warning: Skipped malformed row {index} in {path} (body or author missing): {row.to_dict()}")
        except FileNotFoundError:
            print(f"Error: File not found at {path}")
        except pd.errors.EmptyDataError:
            print(f"Error: CSV file {path} is empty or has no data.")
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV file {path}: {e}")
        except ValueError as e:
            print(f"Data error in CSV file {path}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while parsing {path}: {e}")
        return quotes
