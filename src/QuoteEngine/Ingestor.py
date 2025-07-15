"""
The main Ingestor class that orchestrates quote parsing based on file type.
"""

from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .CSVIngestor import CSVIngestor
from .DOCXIngestor import DOCXIngestor
from .PDFIngestor import PDFIngestor
from .TextIngestor import TextIngestor

import os

class Ingestor(IngestorInterface):
    """
    The central Ingestor class that selects and uses the appropriate
    strategy object (concrete ingestor) to parse a given file.

    It encapsulates all helper ingestor classes and provides a unified
    interface for quote extraction.
    """

    # List of concrete ingestor classes in order of precedence (if applicable,
    # though here order doesn't strictly matter as only one matches per extension)
    ingestors = [TextIngestor, CSVIngestor, DOCXIngestor, PDFIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parses the file at the given path using the appropriate ingestor.

        Iterates through registered ingestors and uses the first one that
        can handle the file's extension.

        Args:
            path (str): The full path to the file to be parsed.

        Returns:
            List[QuoteModel]: A list of QuoteModel objects extracted from the file.

        Raises:
            ValueError: If no suitable ingestor is found for the file type.
        """
        # Ensure the path exists before attempting to parse
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        if not os.path.isfile(path):
            raise IsADirectoryError(f"Path is a directory, not a file: {path}")

        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                print(f"Using {ingestor.__name__} for {os.path.basename(path)}")
                return ingestor.parse(path)
        
        # If no ingestor can handle the file type
        raise ValueError(
            f"No ingestor found for file type of: {path}. "
            f"Supported extensions: {', '.join(sorted(list(set(ext for ing in cls.ingestors for ext in ing.allowed_extensions))))}"
        )

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Checks if any of the registered ingestors can handle the given file path.

        Args:
            path (str): The full path to the file.

        Returns:
            bool: True if any ingestor can process the file, False otherwise.
        """
        return any(ingestor.can_ingest(path) for ingestor in cls.ingestors)
