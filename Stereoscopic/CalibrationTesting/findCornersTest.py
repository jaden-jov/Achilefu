import cv2
import numpy as np
import os

# Ask for the directory path
directory = input("Enter the path to the directory containing .jpg files: ")

# Iterate through all .jpg files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        # Construct full file path
        file_path = os.path.join(directory, filename)
        
        # Read the image file
        image = cv2.imread(file_path)
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Define the chessboard dimensions (9x6)
        pattern_size = (9, 6)
        
        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        if ret:
            # Draw the chessboard corners
            cv2.drawChessboardCorners(image, pattern_size, corners, ret)
            # Display the image
            cv2.imshow('Chessboard Corners', image)
            # Wait for a key press to continue to the next image
            cv2.waitKey(0)
        else:
            print(f"Chessboard corners not found in: {filename}")

# Close all OpenCV windows
cv2.destroyAllWindows()

print("Processing complete.")
