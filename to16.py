from PIL import Image
from skimage import io, color
import numpy as np

def convert_to_16_colors(input_image_path, output_image_path):
    # Load the image
    image_rgb = io.imread(input_image_path)
    if image_rgb.shape[2] == 4:
        image_rgb = image_rgb[:, :, :3]  # Discard the alpha channel if it exists

    # Create a PIL Image object
    image_pil = Image.fromarray(image_rgb)

    # Reduce the number of colors to 16
    image_pil = image_pil.convert('P', palette=Image.ADAPTIVE, colors=16)

    # Save the image
    image_pil.save(output_image_path)

convert_to_16_colors('IMG_1811_16_colors2.png', 'test.png')
