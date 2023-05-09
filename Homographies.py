import cv2
import numpy as np
from matplotlib import pyplot as plt


def compute_homography(images1, images2):
    # Load the images
    img1 = cv2.imread(images1)
    img2 = cv2.imread(images2)

    # Convert the images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Create a SIFT object
    sift = cv2.SIFT_create()

    # Detect keypoints and extract descriptors for the first two images
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    # Draw keypoints on the original images
    img_kp1 = cv2.drawKeypoints(img1, kp1, None)

    # Display the feature in our base image
    plt.imshow(cv2.cvtColor(img_kp1, cv2.COLOR_BGR2RGB))
    plt.title("keypoints In the base image")
    plt.axis('off')
    plt.show()

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    MIN_MATCH_COUNT = 10

    if len(good) > MIN_MATCH_COUNT:

        # Extract the keypoints from the good matches
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        # Estimate homography matrix using RANSAC
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        h, w = img1.shape[0], img1.shape[1]
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, H)
        img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
    else:
        print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
        matchesMask = None

    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                       singlePointColor=None,
                       matchesMask=matchesMask,  # draw only inliers
                       flags=2)
    img12 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

    # Display the matches
    plt.imshow(cv2.cvtColor(img12, cv2.COLOR_BGR2RGB))
    plt.title("matches found")
    plt.axis('off')
    plt.show()

    # Print the number matches found
    print("No. of good matches found", len(good))

    # Return the homography matrix
    return H
