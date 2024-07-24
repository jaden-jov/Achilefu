# turn jpg into png and add a hole to test transparency

from PIL import Image
import numpy as np
import sys

def process_image(input_path, output_path):
    # Open the JPG image
    img = Image.open(input_path)

    # Check if the image is 640x480
    if img.size != (640, 480):
        raise ValueError("Input image must be 640x480 pixels")

    # Convert to RGBA mode (this also converts JPG to PNG internally)
    img = img.convert("RGBA")

    # Convert to numpy array for faster processing
    data = np.array(img)

    # Calculate the coordinates for the 40x40 square in the center
    center_x, center_y = 320, 240  # Center of 640x480 image
    square_size = 100
    x1 = center_x - square_size // 2
    y1 = center_y - square_size // 2
    x2 = x1 + square_size
    y2 = y1 + square_size

    # Set alpha to 0 for the center square, 255 for everything else
    data[:, :, 3] = 255  # Set all alpha values to 255 (fully opaque)
    data[y1:y2, x1:x2, 3] = 0  # Set alpha to 0 (fully transparent) for center square

    # Convert back to PIL Image
    result = Image.fromarray(data)

    # Save as PNG
    result.save(output_path, "PNG")

    print(f"Processed image saved as {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: transformer.py input_image.jpg output_image.png")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        process_image(input_path, output_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)