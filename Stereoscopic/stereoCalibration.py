import cv2
import numpy as np
import glob
import json

def stereo_calibrate(mtx1, dist1, mtx2, dist2, frames_folder):
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints1 = [] # 2d points in image plane.
    imgpoints2 = [] # 2d points in image plane.

    images1 = glob.glob(frames_folder + '/left*.jpg')
    images2 = glob.glob(frames_folder + '/right*.jpg')

    image_size = None

    for i, fname in enumerate(images1):
        img1 = cv2.imread(images1[i])
        img2 = cv2.imread(images2[i])

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        if image_size is None:
            image_size = gray1.shape[::-1]

        # Find the chess board corners
        ret1, corners1 = cv2.findChessboardCorners(gray1, (7,6), None)
        ret2, corners2 = cv2.findChessboardCorners(gray2, (7,6), None)

        # If found, add object points, image points (after refining them)
        if ret1 and ret2:
            objpoints.append(objp)

            corners1 = cv2.cornerSubPix(gray1,corners1,(11,11),(-1,-1),criteria)
            imgpoints1.append(corners1)

            corners2 = cv2.cornerSubPix(gray2,corners2,(11,11),(-1,-1),criteria)
            imgpoints2.append(corners2)

    # Perform stereo calibration
    flags = 0 
    flags |= cv2.CALIB_FIX_INTRINSIC

    ret, mtx1, dist1, mtx2, dist2, R, T, E, F = cv2.stereoCalibrate(
        objpoints, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2,
        image_size, criteria, flags)

    # Save the calibration results
    calibration_data = {
        'mtx1': mtx1.tolist(),
        'dist1': dist1.tolist(),
        'mtx2': mtx2.tolist(),
        'dist2': dist2.tolist(),
        'R': R.tolist(),
        'T': T.tolist(),
        'E': E.tolist(),
        'F': F.tolist()
    }

    with open('stereo_calibration.json', 'w') as f:
        json.dump(calibration_data, f)

    print("Stereo calibration complete. Results saved to stereo_calibration.json")
    print(f"Calibration RMS error: {ret}")

    return calibration_data

# Load individual camera calibrations
with open('intrinsicParams0.json', 'r') as f:
    calib1 = json.load(f)
with open('intrinsicParams1.json', 'r') as f:
    calib2 = json.load(f)

mtx1 = np.array(calib1['camera_matrix'])
dist1 = np.array(calib1['dist_coeffs'])
mtx2 = np.array(calib2['camera_matrix'])
dist2 = np.array(calib2['dist_coeffs'])

# Perform stereo calibration
frames_folder = '/StereoChess'
stereo_calibrate(mtx1, dist1, mtx2, dist2, frames_folder)