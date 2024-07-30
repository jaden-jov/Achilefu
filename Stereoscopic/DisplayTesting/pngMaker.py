from PIL import Image
import numpy as np

# Open the original JPG image
img = Image.open("image1.jpg")

# Resize the image to 640x480 if it's not already that size
img = img.resize((640, 480))

# Convert the image to PNG format
img = img.convert("RGBA")

# Create an alpha channel (all opaque initially)
alpha = Image.new('L', img.size, 255)

# Calculate the coordinates for the 100x100 square in the middle
width, height = img.size
left = (width - 100) // 2
top = (height - 100) // 2
right = left + 100
bottom = top + 100

# Create a mask for the square
mask = Image.new('L', img.size, 255)
mask_array = np.array(mask)
mask_array[top:bottom, left:right] = 0
mask = Image.fromarray(mask_array)

# Apply the mask to the alpha channel
alpha = Image.composite(Image.new('L', img.size, 0), alpha, mask)

# Apply the alpha channel to the image
img.putalpha(alpha)

# Save the result
img.save("transTest.png")

print("Image processed and saved as transTest.png")