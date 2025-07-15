"""
Defines the abstract base class for quote ingestors.
"""

from abc import ABC, abstractmethod
from typing import List
from .QuoteModel import QuoteModel


class IngestorInterface(ABC):
    """
    Abstract base class for ingesting various file types to extract quotes.
    All concrete ingestors must inherit from this class.
    """

    allowed_extensions = []  # List of file extensions this ingestor can handle

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determines if the ingestor can process the given file based on its extension.

        Args:
            path (str): The full path to the file.

        Returns:
            bool: True if the file extension is in `allowed_extensions`, False otherwise.
        """
        file_extension = path.split('.')[-1].lower()
        return file_extension in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parses the specified file and extracts quotes.

        This is an abstract method that must be implemented by concrete ingestors.

        Args:
            path (str): The full path to the file to be parsed.

        Returns:
            List[QuoteModel]: A list of QuoteModel objects extracted from the file.
        """
        pass
