import cv2
import numpy as np
import glob
import json
import os

def calibrate_camera(image_folder, checkerboard_size=(9,6), camera_number=0):
    # Prepare object points
    objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1,2)

    # Arrays to store object points and image points from all images
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane

    # Get list of image files
    images = glob.glob(os.path.join(image_folder, '*.jpg'))

    # Iterate through all images
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)

        # If found, add object points, image points
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)

    # Calibrate camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # Calculate reprojection error
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error

    total_error = mean_error/len(objpoints)

    # Prepare data for JSON
    calibration_data = {
        "camera_matrix": mtx.tolist(),
        "dist_coeffs": dist.tolist(),
        "reprojection_error": total_error
    }

    # Create filename with camera number
    filename = f'intrinsicParams{camera_number}.json'

    # Save to JSON file
    with open(filename, 'w') as f:
        json.dump(calibration_data, f, indent=4)

    print(f"Calibration parameters saved to {filename}")
    print(f"Reprojection Error (ideally below 0.3): {total_error}")

    return calibration_data

calibrate_camera("./Cam0Chess", (9,6), 0)
calibrate_camera("./Cam1Chess", (9,6), 1)

