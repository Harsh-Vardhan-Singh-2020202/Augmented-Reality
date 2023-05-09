import cv2
import os
import numpy as np
from matplotlib import pyplot as plt


def calibrate_camera(num_corners, image_file_path):

    # Defining the criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Prepare the calibration pattern points in real-world coordinates
    obj_points = np.zeros((num_corners[0] * num_corners[1], 3), np.float32)
    obj_points[:, :2] = np.mgrid[0:num_corners[0], 0:num_corners[1]].T.reshape(-1, 2)

    # Create empty lists to store object points and image points from all images
    # 3D points in real-world space
    obj_points_list = []
    # 2D points in image plane
    img_points_list = []

    # Get a list of calibration images

    image_list = [os.path.join(image_file_path, file) for file in os.listdir(image_file_path) if file.endswith('.jpg')]

    # Loop over all calibration images and detect corners

    image_common = cv2.imread(image_list[0])
    gray_common = cv2.cvtColor(image_common, cv2.COLOR_BGR2GRAY)

    counter = 0

    for image_path in image_list:
        # Load the image
        image = cv2.imread(image_path)
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Find chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, num_corners,
                                                 cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        # If corners are found, add object points and image points
        if ret:
            obj_points_list.append(obj_points)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            img_points_list.append(corners2)

            # Refine corner locations
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            # Draw the detected corners and the re-projected corners onto the image
            image_corners = cv2.drawChessboardCorners(image, num_corners, corners2, ret)
            plt.imshow(cv2.cvtColor(image_corners, cv2.COLOR_BGR2RGB))
            plt.title(f"Detected corners in image {counter+1}")
            plt.axis('off')
            plt.show()
            counter += 1

    # Calibrate the camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points_list, img_points_list, gray_common.shape[::-1], None, None)

    # Get intrinsic camera parameters

    fx, fy, cx, cy, skew = cv2.calibrationMatrixValues(mtx, gray_common.shape[::-1], 0, 0)

    print("Estimated Intrinsic Camera Parameters:")
    print("Focal Length (x):", fx)
    print("Focal Length (y):", fy)
    print("Principal Point (x):", cx)
    print("Principal Point (y):", cy)
    print("Skew Parameter:", skew)

    return mtx
