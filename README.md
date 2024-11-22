# Augmented Reality Object Insertion on a Plane

## Overview
This project demonstrates an Augmented Reality (AR) application that inserts 3D objects onto planar surfaces in real-time using computer vision techniques. The system utilizes camera calibration, feature detection, homographies, and object tracking for accurate and stable AR experiences.

## Features
* Real-Time AR Object Placement: Inserts and stabilizes virtual 3D objects on planar surfaces.
* Camera Calibration: Ensures distortion-free rendering using intrinsic parameters.
* Feature Detection: Utilizes SIFT and FLANN-based matching for reliable keypoint detection.
* Object Tracking: Tracks the object's orientation and position with high accuracy.
* 3D Rendering: Renders .obj models directly onto the detected plane.

## Methodology
* Camera Calibration: Captured 25 images of a checkerboard to calibrate the camera using OpenCV.
* Feature Detection & Homography:
* Used SIFT for keypoint detection.
* Employed FLANN for robust planar homographies.
* 3D Object Rendering: Parsed .obj files and rendered them using OpenCV.
* Tracking: Leveraged homographies and RANSAC for real-time tracking.

## Challenges
* Jittering: Occurred during unstable homography computation.
* False Positives: Misidentified base points in certain scenarios.
* Lighting Variations: Affected object stability and projection accuracy.

## Results
The system successfully inserted 3D objects onto planar surfaces in live video, providing a functional but improvable AR experience. Example results and videos are available in the results folder.

## References
* [Augmented Reality with Python and OpenCV - Part 1](https://bitesofcode.wordpress.com/2017/09/12/augmented-reality-with-python-and-opencv-part-1/)
* [Augmented Reality with Python and OpenCV - Part 2](https://bitesofcode.wordpress.com/2018/09/16/augmented-reality-with-python-and-opencv-part-2/)
* [GitHub: Augmented Reality Project](https://github.com/juangallostra/augmented-reality)
