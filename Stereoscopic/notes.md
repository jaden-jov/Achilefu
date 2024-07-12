# Stereoscopic Notes

GStreamerTesting contains a working pipeling that takes two camera streams and displays them side by side, the single stream test is in Handheld CVG 
Next step is to learn how the frames need to be transformed to produce stereovision. Requires opencv with gstreamer compatability on the pi and linux laptop, bash script for that is in handheld branch

## PROBLEM

The challenge is to implement stereoscopic NIR imaging in the CVG headset

## BRAINSTORM
1. 2 camera setups, project each separately onto the eyes, easiest solution
2. depth mapping with structured light, turn that into stereoscopic vision
3. polarized 3d, personal favorite, glasses have a 120 hz display so its definitely possible 4
4. might have to use gstreamer, as rpi cannot support 4 cameras -could just use two cameras, just for IR? AR type final product

## PLAN

### General Plan
1. get two images to display side by side using openCV **Complete**
2. get two streams to display side by side using openCV **Too easy**
3. get two streams to display side by side using gstreamer **Complete**
4. look into the matrix transformation things

### Plan for AR (the matrix transformation things) from chatgpt because I have no idea how to do this

To achieve accurate stereoscopic vision with your head-mounted display (HMD) and the two IMX219 cameras for AR fluorescent imaging, you need to 
perform several calibration steps. These steps ensure that the virtual imagery aligns correctly with the real-world view seen through the HMD. Here 
are the key calibration steps:

1. Intrinsic Calibration of Cameras
Intrinsic calibration involves determining the internal characteristics of each camera, such as focal length, optical center, and lens distortion
parameters. You can use a calibration tool like OpenCV to perform this task. The steps are:
	1. Capture multiple images of a known calibration pattern (like a chessboard or a grid) at different orientations and positions.
	2. Use OpenCV functions like cv2.findChessboardCorners() and cv2.calibrateCamera() to calculate the intrinsic parameters of each camera.
	3. Save the intrinsic parameters (camera matrix and distortion coefficients) for each camera.
2. Extrinsic Calibration of Cameras
Extrinsic calibration determines the relative position and orientation between the two cameras. This step is crucial for achieving proper stereo 
vision.
	1. Capture images simultaneously from both cameras of the same calibration pattern.
	2. Use OpenCV’s stereo calibration functions such as cv2.stereoCalibrate() to find the rotation matrix and translation vector between the two cameras.
	3. Save the extrinsic parameters for use in stereo rectification.
3. Stereo Rectification
Stereo rectification aligns the images from both cameras to be on the same plane, which is necessary for correct depth perception.
	1. Use the intrinsic and extrinsic parameters obtained from the previous steps.
	2. Apply OpenCV’s cv2.stereoRectify() to compute the rectification transforms for each camera.
	3. Use cv2.initUndistortRectifyMap() and cv2.remap() to apply the rectification to the images captured by the cameras.
4. Synchronization
Ensure that both cameras are capturing images simultaneously to avoid any temporal misalignment.
5. Calibration with the HMD
To ensure the virtual imagery aligns with the real-world view seen through the HMD:
	1. Determine the position and orientation of the cameras relative to the HMD. This might involve physically measuring the distances and angles or using a tracking system.
	2. Calibrate the display parameters of the HMD, such as the field of view (FOV), eye-to-screen distance, and any lens distortion.
6. Alignment with User’s View
This step ensures that the stereoscopic vision aligns with the user's view through the HMD lenses:
	1. Display calibration patterns (like grids or crosshairs) on the HMD and align them with the real-world view.
	1. Adjust the virtual camera parameters (like the position and orientation) in the AR software to match the user's perspective through the HMD.
	1. Perform user testing and fine-tuning to ensure that the alignment feels natural and accurate.
7. Color Calibration (Optional)
If the color reproduction of the fluorescent imaging is critical, perform color calibration to ensure accurate color representation.
	1. Capture images of a color calibration target under the fluorescent lighting.
	2. Adjust the color balance and settings of the cameras to match the expected colors.

## RESOURCES
- Mela-2015-Stereoscopic Integrated Imaging Gogg.pdf
	check the Image Acquisition, Processing, Registration and Display 
 	section for information on how they aligned their cameras mathematically
- https://lubosz.wordpress.com/2016/07/04/introducing-gstreamer-vr-plug-ins-
and-sphvr/
	Gstreamer stereoscopic things
- https://lubosz.wordpress.com/2013/08/28/view-side-by-side-stereoscopic-
video-with-gstreamer-and-oculus-rift/
	anotha one
- hconcat (opencv) concatenates two images horizontally
- https://coaxion.net/blog/2014/08/concatenate-multiple-streams-gaplessly-
with-gstreamer/
	concatenate with gstreamer
- https://github.com/simondlevy/OpenCV_GStreamer/blob/master/Source/Sender.cpp
	example gstreamer cpp code, use as template
- https://github.com/Digital1O1/Onboard_VS_Streaming_LINUX/blob/main
/Testing%20Dual%20GStreamerPipeline/main.cpp
	Chris's work for receiver, use as reference but not too much useful here
- https://github.com/Digital1O1/Onboard_VS_Streaming_RPI/blob/master/
GStreamer%20Folder/GStreamer%20Dual%20Pipeline/doubleCameraPipeline.sh
	Chris RPI thing
- https://stackoverflow.com/questions/46219454/how-to-open-a-gstreamer-
pipeline-from-opencv-with-videowriter
	useful template for cpp gstreamer code
- https://indico.freedesktop.org/event/5/contributions/255/attachments/112/170/
%5BFINAL%5D%20libcamerasrc_%20Introduction%20and%20usage%20of%20libcamera%
27s%20GStreamer%20element.pdf
	libcamerasrc info
- OpenCV: For camera calibration, stereo rectification, and image processing.
- OpenHMD: For interfacing with various HMDs and obtaining HMD-specific parameters.
- ROS (Robot Operating System): For synchronization and handling multiple sensor data streams if needed.
