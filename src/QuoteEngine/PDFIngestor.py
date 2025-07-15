"""
Ingestor for pdf files (.pdf) extension
"""

import subprocess
import shutil # To check for pdftotext executable
from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
import os 

class PDFIngestor(IngestorInterface):
    """
    Concrete ingestor for PDF files using Xpdf's pdftotext.

    It extracts text from PDF files using the 'pdftotext' command-line tool
    and attempts to parse quotes in the format '"body" - Author' or 'body - Author'.
    Requires 'pdftotext' to be installed and accessible in the system's PATH.
    """

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parses a .pdf file and extracts quotes using pdftotext.

        Args:
            path (str): The path to the .pdf file.

        Returns:
            List[QuoteModel]: A list of QuoteModel objects.

        Raises:
            Exception: If 'pdftotext' is not found or for other parsing errors.
        """
        if not cls.can_ingest(path):
            raise Exception(f"Cannot ingest file type for {path}. Expected .pdf")

        # Check if pdftotext is available in the system's PATH
        if shutil.which("pdftotext") is None:
            raise Exception(
                "The 'pdftotext' command-line tool is not found. "
                "Please install Xpdf or Poppler utilities and ensure 'pdftotext' "
                "is in your system's PATH to enable PDF ingestion."
            )

        quotes = []
        try:
            # Execute pdftotext to extract text from the PDF
            # -layout preserves original layout, which can be helpful for quotes
            # - means output to stdout
            command = ['pdftotext', '-layout', path, '-']
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            text_content = result.stdout

            # Process the extracted text line by line
            for line in text_content.splitlines():
                line = line.strip()
                if not line:  # Skip empty lines
                    continue

                # Attempt to parse quotes in the format "body" - Author or body - Author
                if ' - ' in line:
                    parts = line.split(' - ', 1)
                    body = parts[0].strip().strip('"') # Remove leading/trailing quotes from body
                    author = parts[1].strip()
                    if body and author:
                        quotes.append(QuoteModel(body, author))
                    else:
                        print(f"Warning: Skipped malformed line in {path} (body or author missing): '{line}'")
                # else:
                    # Optional: Uncomment the line below for debugging if many lines are skipped
                    # print(f"Debug: Skipped line in {path} due to missing ' - ' separator: '{line}'")

        except FileNotFoundError:
            # This error occurs if the PDF file itself is not found
            raise Exception(f"Error: PDF file not found at {path}")
        except subprocess.CalledProcessError as e:
            # This error occurs if pdftotext command fails (e.g., corrupt PDF)
            raise Exception(f"Error running pdftotext on {path}: {e.stderr}")
        except Exception as e:
            # Catch any other unexpected errors during parsing
            raise Exception(f"An unexpected error occurred while parsing {path}: {e}")
        return quotes
