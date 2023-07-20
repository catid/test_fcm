import numpy as np
import skfuzzy as fuzz
from skimage import io, color, transform
from PIL import Image

print("Loading image...")

# Load the image and convert it to L*a*b color space
image_rgb = io.imread('image.png')

if image_rgb.shape[2] == 4:
    image_rgb = image_rgb[:, :, :3]  # Discard the alpha channel

image_lab = color.rgb2lab(image_rgb)

min_w = 1024

# Check if the smallest dimension is greater than min_w
if min(image_lab.shape[:2]) > min_w:
    # Calculate the new dimensions, keeping aspect ratio
    aspect_ratio = image_lab.shape[1] / image_lab.shape[0]
    if image_lab.shape[0] < image_lab.shape[1]:
        new_shape = (min_w, int(min_w * aspect_ratio))
    else:
        new_shape = (int(min_w / aspect_ratio), min_w)

    print(f"Resizing image to {new_shape}")

    # Resize the image
    image_lab = transform.resize(image_lab, new_shape, mode='reflect', 
                                 anti_aliasing=True, preserve_range=True)

# Reshape the image to be a list of pixels
pixels = image_lab.reshape(-1, 3)

print("Perform fuzzy c-means clustering...")

# Perform fuzzy c-means clustering
centers, _, _, _, _, _, _ = fuzz.cluster.cmeans(
    pixels.T, 16, 2, error=0.005, maxiter=1000)

print("Assign each pixel to the nearest cluster...")

# Assign each pixel to the nearest cluster
labels = fuzz.cluster.cmeans_predict(pixels.T, centers, 2, error=0.005, maxiter=1000)[0]

print("Find the cluster with the highest probability...")

# Find the cluster with the highest probability
labels = np.argmax(labels, axis=0)

print("Finalizing image...")

# Replace each pixel with the center of its cluster
quantized_pixels = centers[labels]

# Reshape the quantized pixels to the original image shape
quantized_image = quantized_pixels.reshape(image_lab.shape)

# Convert the quantized image back to RGB
quantized_image_rgb = color.lab2rgb(quantized_image)

# Scale the values to [0, 255] and convert to uint8
quantized_image_rgb = (quantized_image_rgb * 255).astype(np.uint8)

print("Saving output image...")

# Save the quantized image
#io.imsave('straight_quantized_image.png', quantized_image_rgb)

# Create a PIL Image object
image_pil = Image.fromarray(quantized_image_rgb)

# Reduce the number of colors to 16
image_pil = image_pil.convert('P', palette=Image.ADAPTIVE, colors=16)

# Save the quantized image
image_pil.save('final_quantized_image.png')