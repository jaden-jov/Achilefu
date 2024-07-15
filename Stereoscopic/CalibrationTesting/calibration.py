import cv2
import numpy as np
import glob

# intrinsic calibration, run for each camera

def calibrate_camera(images_path):
    
    # Termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Prepare object points (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    images = glob.glob(images_path + '/*.jpg')
    
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (9,6), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, (9,6), corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(500)

    cv2.destroyAllWindows()

    # Calibration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return mtx, dist

# extrinsic calibration

def stereo_calibrate(images_path1, images_path2, mtx1, dist1, mtx2, dist2):
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

    objpoints = []  # 3d points in real world space
    imgpoints1 = []  # 2d points in image plane of camera 1
    imgpoints2 = []  # 2d points in image plane of camera 2

    images1 = glob.glob(images_path1 + '/*.jpg')
    images2 = glob.glob(images_path2 + '/*.jpg')

    for fname1, fname2 in zip(images1, images2):
        img1 = cv2.imread(fname1)
        img2 = cv2.imread(fname2)
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        ret1, corners1 = cv2.findChessboardCorners(gray1, (9,6), None)
        ret2, corners2 = cv2.findChessboardCorners(gray2, (9,6), None)

        if ret1 == True and ret2 == True:
            objpoints.append(objp)

            corners1 = cv2.cornerSubPix(gray1, corners1, (11,11), (-1,-1), criteria)
            corners2 = cv2.cornerSubPix(gray2, corners2, (11,11), (-1,-1), criteria)

            imgpoints1.append(corners1)
            imgpoints2.append(corners2)

    ret, mtx1, dist1, mtx2, dist2, R, T, E, F = cv2.stereoCalibrate(
        objpoints, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2, gray1.shape[::-1],
        criteria=criteria, flags=cv2.CALIB_FIX_INTRINSIC)
    
    return R, T

# stereo rectification

def stereo_rectify(mtx1, dist1, mtx2, dist2, R, T, image_size):
    R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(mtx1, dist1, mtx2, dist2, image_size, R, T)
    
    map1x, map1y = cv2.initUndistortRectifyMap(mtx1, dist1, R1, P1, image_size, cv2.CV_16SC2)
    map2x, map2y = cv2.initUndistortRectifyMap(mtx2, dist2, R2, P2, image_size, cv2.CV_16SC2)
    
    return map1x, map1y, map2x, map2y, Q

# Example usage
camera1_intrinsics = calibrate_camera('/path/to/camera1/images')
camera2_intrinsics = calibrate_camera('/path/to/camera2/images')
R, T = stereo_calibrate('/path/to/camera1/images', '/path/to/camera2/images', *camera1_intrinsics, *camera2_intrinsics)
image_size = (640, 480)
map1x, map1y, map2x, map2y, Q = stereo_rectify(*camera1_intrinsics, *camera2_intrinsics, R, T, image_size)

# Load a pair of stereo images
img1 = cv2.imread('/path/to/camera1/image.jpg')
img2 = cv2.imread('/path/to/camera2/image.jpg')

# Rectify the images using the rectification maps
rectified_img1 = cv2.remap(img1, map1x, map1y, cv2.INTER_LINEAR)
rectified_img2 = cv2.remap(img2, map2x, map2y, cv2.INTER_LINEAR)

# Convert rectified images to grayscale
gray_img1 = cv2.cvtColor(rectified_img1, cv2.COLOR_BGR2GRAY)
gray_img2 = cv2.cvtColor(rectified_img2, cv2.COLOR_BGR2GRAY)

# Compute the disparity map using StereoBM or StereoSGBM
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(gray_img1, gray_img2)

# Reproject points to 3D
points_3D = cv2.reprojectImageTo3D(disparity, Q)

# Normalize the disparity map for visualization
disparity_normalized = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
disparity_normalized = np.uint8(disparity_normalized)

# Display the images
cv2.imshow('Rectified Image 1', rectified_img1)
cv2.imshow('Rectified Image 2', rectified_img2)
cv2.imshow('Disparity Map', disparity_normalized)
cv2.waitKey(0)
cv2.destroyAllWindows()
