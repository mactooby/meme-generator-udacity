"""
Ingestor for Microsoft Word (.docx) files.
"""

from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel

# To install: pip install python-docx
try:
    from docx import Document
    from docx.opc.exceptions import PackageNotFoundError
except ImportError:
    Document = None
    PackageNotFoundError = None
    print("Warning: python-docx library not found. DOCX ingestion will be disabled.")


class DOCXIngestor(IngestorInterface):
    """
    Concrete ingestor for DOCX files.

    It extracts text from paragraphs and attempts to parse quotes
    in the format '"body" - Author' or 'body - Author'.
    Requires 'python-docx' library.
    """

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parses a .docx file and extracts quotes.

        Args:
            path (str): The path to the .docx file.

        Returns:
            List[QuoteModel]: A list of QuoteModel objects.

        Raises:
            ImportError: If 'python-docx' is not installed.
            Exception: For other file access or parsing errors.
        """
        if not cls.can_ingest(path):
            raise Exception(f"Cannot ingest file type for {path}. Expected .docx")

        if Document is None:
            raise ImportError(
                "The 'python-docx' library is not installed. "
                "Please install it using 'pip install python-docx' to enable DOCX ingestion."
            )

        quotes = []
        try:
            document = Document(path)
            for paragraph in document.paragraphs:
                line = paragraph.text.strip()
                if not line:  # Skip empty lines
                    continue

                if ' - ' in line:
                    parts = line.split(' - ', 1)
                    body = parts[0].strip().strip('"')
                    author = parts[1].strip()
                    if body and author:
                        quotes.append(QuoteModel(body, author))
                    else:
                        print(f"Warning: Skipped malformed paragraph in {path} (body or author missing): '{line}'")
                else:
                    print(f"Warning: Skipped paragraph in {path} due to missing ' - ' separator: '{line}'")
        except FileNotFoundError:
            print(f"Error: File not found at {path}")
        except PackageNotFoundError:
            print(f"Error: Invalid or corrupt DOCX file at {path}")
        except Exception as e:
            print(f"An unexpected error occurred while parsing {path}: {e}")
        return quotes
