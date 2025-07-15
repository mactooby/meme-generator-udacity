import os
import random
from PIL import Image, ImageDraw, ImageFont

class MemeEngine:
    """
    A class to create memes by manipulating and drawing text onto images.

    This engine handles loading, resizing, adding text, and saving images.
    """

    def __init__(self, output_dir='./tmp'):
        """
        Initializes the MemeEngine with an output directory for generated memes.

        Args:
            output_dir (str): The directory where the manipulated images will be saved.
                              Defaults to './tmp'.
        """
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        """
        Creates a meme by adding text and author to an image and resizing it.

        Args:
            img_path (str): The path to the input image file.
            text (str): The quote body to be added to the image.
            author (str): The author of the quote to be added to the image.
            width (int): The maximum width of the output image. The height
                         will be scaled proportionally. Defaults to 500px.

        Returns:
            str: The path to the newly created meme image.

        Raises:
            FileNotFoundError: If the specified image file does not exist.
            IOError: If there is an error loading or saving the image.
            Exception: For other unexpected errors during meme generation.
        """
        try:
            with Image.open(img_path) as img:
                # Resize the image
                original_width, original_height = img.size
                if original_width > width:
                    height = int(width * original_height / original_width)
                    img = img.resize((width, height), Image.Resampling.LANCZOS)

                draw = ImageDraw.Draw(img)

                # Define text properties (you might need to provide a font file path)
                try:
                    # Attempt to load a common font, or use default if not found
                    font_size = int(img.size[1] / 15)  # Dynamic font size
                    font = ImageFont.truetype("arial.ttf", font_size)
                except IOError:
                    # Fallback to default font if arial.ttf is not found
                    font = ImageFont.load_default()
                    font_size = 15 # Set a default size for the fallback font

                # Calculate text position (simple centering for now, can be improved)
                # Adjust position to be at the bottom and slightly above
                text_margin = 10
                text_position_y = img.size[1] - (2 * font_size) - text_margin

                # Add quote body
                draw.text((10, text_position_y), text, font=font, fill=(255, 255, 255))

                # Add author
                author_position_y = img.size[1] - font_size - text_margin
                draw.text((10, author_position_y), f"- {author}", font=font, fill=(255, 255, 255))

                # Generate a unique filename
                output_filename = f"meme_{random.randint(0, 1000000)}.png"
                output_path = os.path.join(self.output_dir, output_filename)

                # Save the manipulated image
                img.save(output_path)
                return output_path

        except FileNotFoundError:
            raise FileNotFoundError(f"Image file not found at: {img_path}")
        except IOError as e:
            raise IOError(f"Error loading or saving image: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")
