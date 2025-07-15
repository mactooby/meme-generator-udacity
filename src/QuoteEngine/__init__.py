"""
QuoteEngine package for ingesting and parsing various quote file types.
"""
from .QuoteModel import QuoteModel
from .Ingestor import Ingestor

# Define what gets imported when someone does `from QuoteEngine import *`
__all__ = ['QuoteModel', 'Ingestor']
