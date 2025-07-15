import random
import os
import requests
from flask import Flask, render_template, abort, request
import tempfile


# @TODO Import your Ingestor and MemeEngine classes

from MemeEngine import MemeEngine
from QuoteEngine import Ingestor
#import QuoteEngine

import os 


app = Flask(__name__)

# Initialize MemeEngine with the static output directory
meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for f in quote_files:
        try:
            quotes.extend(Ingestor.parse(f))
        except Exception as e:
            print(f"Could not parse {f}: {e}")

    images_path = "./_data/photos/dog/"
    imgs = []
    if os.path.exists(images_path):
        for root, dirs, files in os.walk(images_path):
            for file in files:
                if file.endswith(('.jpg', '.png', '.jpeg')):
                    imgs.append(os.path.join(root, file))
    else:
        print(f"Warning: Image directory not found: {images_path}")
        # Add a placeholder image if the directory doesn't exist
        # This makes the app runnable even if no images are provided
        placeholder_img = os.path.join(os.path.dirname(__file__), '_data')
        if os.path.exists(placeholder_img):
            imgs.append(placeholder_img)
        else:
            print("Error: No images found and no fallback placeholder available.")


    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = None
    if imgs:
        img = random.choice(imgs)
    else:
        print("No images available for random meme generation.")
        # Fallback to a placeholder if no images are found
        img = os.path.join(os.path.dirname(__file__), '_data')
        if not os.path.exists(img):
            return "Error: No images to generate random meme.", 500

    quote = None
    if quotes:
        quote = random.choice(quotes)
    else:
        print("No quotes available for random meme generation.")
        # Fallback to a default quote
        quote = QuoteModel("No quotes found!", "Admin")

    path = meme.make_meme(img, quote.body, quote.author)
    if path:
        # Flask expects paths relative to 'static' for url_for,
        # but here we're passing a direct file path.
        # We need to strip the 'static/' part for the template.
        #display_path = path.replace('static/', '')
        display_path = path
        return render_template('meme.html', path=display_path)
    else:
        return "Error generating random meme.", 500


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """
    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')

    if not image_url:
        return "Image URL is required.", 400

    temp_img_path = None
    path = None

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status() # Raise an exception for HTTP errors

        # Create a temporary file to save the image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_img_path = temp_file.name

        path = meme.make_meme(temp_img_path, body, author)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return f"Error downloading image: {e}", 400
    except Exception as e:
        print(f"Error creating meme: {e}")
        return f"Error creating meme: {e}", 500
    finally:
        # Remove the temporary saved image
        if temp_img_path and os.path.exists(temp_img_path):
            os.remove(temp_img_path)

    if path:
        #display_path = path.replace('static/', '')
        print(path)
        display_path = path
        return render_template('meme.html', path=display_path)
    else:
        return "Error creating user-defined meme.", 500


if __name__ == "__main__":
    # Ensure necessary directories exist
    os.makedirs('./_data/DogQuotes', exist_ok=True)
    os.makedirs('./_data/photos/dog', exist_ok=True)
    os.makedirs('./static', exist_ok=True)

    # Create dummy files for setup to work if they don't exist
    for ext in ['.txt', '.docx', '.pdf', '.csv']:
        dummy_file = f'./_data/DogQuotes/dummy{ext}'
        if not os.path.exists(dummy_file):
            with open(dummy_file, 'w') as f:
                f.write(f'This is a dummy {ext} file.\n')

    # Create a dummy image for setup to work if no images are present
    dummy_image = './_data/photos/dog/xander_1.jpg'
    if not os.path.exists(dummy_image):
        try:
            # Attempt to download a small placeholder image
            img_data = requests.get('https://placehold.co/100x100/000000/FFFFFF?text=Dog').content
            with open(dummy_image, 'wb') as f:
                f.write(img_data)
            print(f"Created a dummy image at {dummy_image}")
        except Exception as e:
            print(f"Could not create dummy image: {e}")


if __name__ == "__main__":
    app.run()
