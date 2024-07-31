import cv2
import numpy as np

img = cv2.imread('./image1.jpg', cv2.IMREAD_UNCHANGED)

# Change to rgba
if len(img.shape) == 2:  # Grayscale
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
elif img.shape[2] == 3:  # BGR
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
elif img.shape[2] == 4:  # BGRA
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
else:
    raise ValueError(f"Unexpected number of channels: {img.shape[2]}")

height, width = img.shape[:2]

# Calculate the coordinates for the center square
start_y = (height - 100) // 2
end_y = start_y + 100
start_x = (width - 100) // 2
end_x = start_x + 100

# Set the alpha channel to 0 for the center square
img[start_y:end_y, start_x:end_x, 3] = 0

# Display image
cv2.imshow('RGBA Image', rgba_image)
cv2.waitKey(0)
