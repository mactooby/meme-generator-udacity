"""
Ingestor for plain text (.txt) files.
"""

from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class TextIngestor(IngestorInterface):
    """
    Concrete ingestor for plain text files.

    It parses each line, expecting the format '"body" - Author' or 'body - Author'.
    """

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parses a .txt file and extracts quotes.

        Args:
            path (str): The path to the .txt file.

        Returns:
            List[QuoteModel]: A list of QuoteModel objects.

        Raises:
            Exception: If the file cannot be opened or read.
        """
        if not cls.can_ingest(path):
            raise Exception(f"Cannot ingest file type for {path}. Expected .txt")

        quotes = []
        try:
            with open(path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue

                    if ' - ' in line:
                        parts = line.split(' - ', 1)  # Split only on the first ' - '
                        body = parts[0].strip().strip('"')  # Remove potential surrounding quotes
                        author = parts[1].strip()
                        if body and author: # Ensure both parts are non-empty
                            quotes.append(QuoteModel(body, author))
                        else:
                            print(f"Warning: Skipped malformed line in {path}: '{line}' (body or author missing)")
                    else:
                        print(f"Warning: Skipped line in {path} due to missing ' - ' separator: '{line}'")
        except FileNotFoundError:
            print(f"Error: File not found at {path}")
        except PermissionError:
            print(f"Error: Permission denied when trying to read {path}")
        except Exception as e:
            print(f"An unexpected error occurred while parsing {path}: {e}")
        return quotes
