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
        
        if not ret:
            print(f"Chessboard corners not found in: {filename}")

print("Processing complete.")