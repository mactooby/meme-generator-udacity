Command-Line Meme Generator
This project is a command-line application developed as part of an Intermediate Python class project.

Features
Random Meme Generation: Automatically selects a random image from a local directory and a random quote from various supported file types.

Custom Meme Creation: Allows users to specify an image (local path or URL), a quote body, and an author via command-line arguments.

Multi-format Quote Ingestion: Supports parsing quotes from .txt, .docx, .pdf, and .csv files.


Setup and Installation
Prerequisites
Python 3.7+

pip (Python package installer)

pdftotext: For PDF ingestion, you need the pdftotext command-line tool. This is typically part of the Xpdf or Poppler utilities.

On Linux (Debian/Ubuntu): sudo apt-get install poppler-utils

On macOS: brew install xpdf (or brew install poppler)

On Windows: Download Xpdf tools from xpdfreader.com and add the bin directory to your system's PATH.

Install Python Dependencies

pip3 install -r requirements.txt 

How to Run

first *Mandadory*

cd src 

Execute the script from your terminal:

Generate a Random Meme

exaple 1
python3 meme.py 

example 2

python3 meme.py --author tester3 --body "here aim again " --path _data/photos/dog/xander_3.jpg

example 3 

run flask server 

python3 app.py  

browse to (http://127.0.0.1:5000)


Class Roles
QuoteModel: A data structure to encapsulate a quote's body (text) and author.

IngestorInterface: An abstract base class defining the common interface (can_ingest, parse) for all quote ingestors.

TextIngestor: Concrete implementation of IngestorInterface for parsing quotes from plain .txt files. 


PDFIngestor: Concrete implementation for parsing quotes from .pdf files using the external pdftotext command-line tool.

DocxIngestor: Concrete implementation for parsing quotes from .docx files. 


CSVIngestor: Concrete implementation for parsing quotes from .csv files. 


Ingestor: A static dispatcher class that determines which specific IngestorInterface implementation can handle a given file and then calls its parse method.

MemeEngine: Handles the core meme creation logic. It takes an image path, quote body, and author, then uses the Pillow library to resize the image and overlay the text, saving the result to an output directory.