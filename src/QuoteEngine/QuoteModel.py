"""
Contains the QuoteModel class for encapsulating quote body and author.
"""

class QuoteModel:
    """
    Represents a single quote with a body and an author.
    """

    def __init__(self, body: str, author: str):
        """
        Initializes a new QuoteModel instance.

        Args:
            body (str): The main text of the quote.
            author (str): The author of the quote.
        """
        self.body = body
        self.author = author

    def __repr__(self) -> str:
        """
        Returns a string representation of the QuoteModel object.

        Returns:
            str: A string in the format '"body" - Author'.
        """
        return f'"{self.body}" - {self.author}'

    def __eq__(self, other) -> bool:
        """
        Compares two QuoteModel objects for equality.

        Returns:
            bool: True if body and author are identical, False otherwise.
        """
        if not isinstance(other, QuoteModel):
            return NotImplemented
        return self.body == other.body and self.author == other.author

    def __hash__(self) -> int:
        """
        Returns the hash value for the QuoteModel object.

        Returns:
            int: Hash of the body and author.
        """
        return hash((self.body, self.author))
