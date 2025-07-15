import os
import random
import argparse

# @TODO Import your Ingestor and MemeEngine classes

from MemeEngine import MemeEngine
from QuoteEngine import Ingestor,QuoteModel


def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img_path = None
    quote = None

    # Determine image path
    if path is None:
        images_dir = "./_data/photos/dog/"
        imgs = []
        if os.path.exists(images_dir):
            for root, dirs, files in os.walk(images_dir):
                for file in files:
                    if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                        imgs.append(os.path.join(root, file))
        if not imgs:
            raise Exception("No images found in ./_data/photos/dog/. Please add image files.")
        img_path = random.choice(imgs)
    else:
        # If a path is provided, check if it's a URL
        if path.startswith('http://') or path.startswith('https://'):
            try:
                response = requests.get(path, stream=True)
                response.raise_for_status()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        temp_file.write(chunk)
                    img_path = temp_file.name
            except requests.exceptions.RequestException as e:
                raise Exception(f"Error downloading image from URL {path}: {e}")
        else:
            img_path = path # Assume it's a local file path

    # Determine quote
    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            try:
                quotes.extend(Ingestor.parse(f))
            except Exception as e:
                print(f"Warning: Could not parse {f}: {e}")

        if not quotes:
            raise Exception("No quotes found in ./_data/DogQuotes/. Please add quote files.")
        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    # Generate meme
    meme = MemeEngine('./tmp') # Output to a 'tmp' directory
    output_meme_path = meme.make_meme(img_path, quote.body, quote.author)

    # Clean up temporary image file if it was downloaded from a URL
    if path and (path.startswith('http://') or path.startswith('https://')) and img_path and os.path.exists(img_path):
        os.remove(img_path)

    return output_meme_path


if __name__ == "__main__":
    # Ensure necessary directories exist for CLI tool
    os.makedirs('./_data/DogQuotes', exist_ok=True)
    os.makedirs('./_data/photos/dog', exist_ok=True)
    os.makedirs('./tmp', exist_ok=True) # Output directory for CLI generated memes


    parser = argparse.ArgumentParser(description='Generate a meme.')
    parser.add_argument('--path', type=str,
                        help='Path to an image file (local or URL).')
    parser.add_argument('--body', type=str,
                        help='Quote body to add to the image.')
    parser.add_argument('--author', type=str,
                        help='Quote author to add to the image.')

    args = parser.parse_args()

    try:
        meme_output_path = generate_meme(args.path, args.body, args.author)
        if meme_output_path:
            print(f"Meme generated successfully at: {meme_output_path}")
        else:
            print("Failed to generate meme.")
    except Exception as e:
        print(f"An error occurred: {e}")

