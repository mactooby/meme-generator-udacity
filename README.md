# Command-Line Meme Generator

This project is a command-line application developed as part of an **Intermediate Python class project**. Its purpose is to demonstrate object-oriented programming, file handling, external command execution, and command-line argument parsing by generating memes.

## Features

* **Random Meme Generation**: Automatically selects a random image from a local directory and a random quote from various supported file types.

* **Custom Meme Creation**: Allows users to specify an image (local path or URL), a quote body, and an author via command-line arguments.

* **Multi-format Quote Ingestion**: Supports parsing quotes from `.txt`, `.docx`, `.pdf`, and `.csv` files.

## Setup and Installation

### Prerequisites

* Python 3.7+

* `pip` (Python package installer)

* **`pdftotext`**: For PDF ingestion, you need the `pdftotext` command-line tool. This is typically part of the Xpdf or Poppler utilities.

    * **On Linux (Debian/Ubuntu)**: `sudo apt-get install poppler-utils`

    * **On macOS**: `brew install xpdf` (or `brew install poppler`)

    * **On Windows**: Download Xpdf tools from [xpdfreader.com](https://www.xpdfreader.com/download.html) and add the `bin` directory to your system's PATH.

### Install Python Dependencies

Navigate to the directory where your `requirements.txt` file is located (typically the project root) and install the required Python packages:

```bash
pip3 install -r requirements.txt
```


## How to Run

First, navigate to the `src` directory where `meme.py` and `app.py` are located:

```bash
cd src
```

### Command-Line Meme Generation

Execute the script from your terminal:

**Example 1: Generate a Random Meme**

```bash
python3 meme.py
```

This will print the path to the newly generated meme file in the `./tmp` directory.

**Example 2: Create a Custom Meme (with local image)**

```bash
python3 meme.py --author tester3 --body "here i am again" --path _data/photos/dog/xander_3.jpg
```

### Run Flask Server (Web Application)

To run the web version of the meme generator:

```bash
python3 app.py
```

Browse to `http://127.0.0.1:5000` in your web browser.

## Class Roles

* **`QuoteModel`**: A data structure to encapsulate a quote's `body` (text) and `author`.

* **`IngestorInterface`**: An abstract base class defining the common interface (`can_ingest`, `parse`) for all quote ingestors.

* **`TextIngestor`**: Concrete implementation of `IngestorInterface` for parsing quotes from plain `.txt` files.

* **`PDFIngestor`**: Concrete implementation for parsing quotes from `.pdf` files using the external `pdftotext` command-line tool.

* **`DocxIngestor`**: Concrete implementation for parsing quotes from `.docx` files.

* **`CSVIngestor`**: Concrete implementation for parsing quotes from `.csv` files.

* **`Ingestor`**: A static dispatcher class that determines which specific `IngestorInterface` implementation can handle a given file and then calls its `parse` method.

* **`MemeEngine`**: Handles the core meme creation logic. It takes an image path, quote body, and author, then uses the Pillow library to resize the image and overlay the text, saving the result to an output directory.
