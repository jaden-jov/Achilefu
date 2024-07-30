# Stereoscopic Notes

GStreamerTesting contains a working pipeling that takes two camera streams and displays them side by side, the single stream test is in Handheld CVG 
Next step is to learn how the frames need to be transformed to produce stereovision. Requires opencv with gstreamer compatability on the pi and linux laptop, bash script for that is in handheld branch, as well as pygame (sudo apt install python3-pygame)

skipping FOV mismatch and color calibration because the plan is just to take the pixels that see tumor and make them a bright color, and it should be in the middle of the FOV

libcamera-still --camera 1 --width 640 --height 480 --iso 100 --shutter 10000 --timeout 2000 -o image1.jpg

run instrinsic calibration again after putting the bandpass filter on

glob doesn't sort by itself

sbs 3d can be achieved using ian's repo to turn sbs 3d mode on and then rescaling a double wide image to 1920 x 1080 and displaying it using pygame. A more elegant solution would be to create a custom edid to allow the pi to ignore the default display driver's resolution and send a double wide image, but this may not even be possible from the device side if it is meant to split a 1920 x 1080 image, and would take more time

transparency will require the pykms library to handle the drm, sending a 0 0 0 image does not work as intended, use the alpha gstreamer element to add that channel
github.com/tomba/pykms

hdmi_mode=87
hdmi_cvt=1280 480 60
^^these changes to boot config tells the pi that the display is a custom display capable of displaying those parameters

tvservice -e 'DMT {width} {height} {refresh_rate}
fbset -depth 8; fbset -depth 16
^^this is a way to change it from the command line so it can be done through the program using subprocess, probably do this before initializing pygame or opencv

def process_frame(frame):
	b, g, r, a = cv2.split(frame)
	mask = a > 0
        b = b * mask
	g = g * mask
	r = r * mask
	return cv2.merge([b, g, r, a])
 ^^turns pixels with 0 alpha to black 

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

1. Intrinsic Calibration of Cameras **DONE**
Intrinsic calibration involves determining the internal characteristics of each camera, such as focal length, optical center, and lens distortion
parameters. You can use a calibration tool like OpenCV to perform this task. The steps are:
	1. Capture multiple images of a known calibration pattern (like a chessboard or a grid) at different orientations and positions.
	2. Use OpenCV functions like cv2.findChessboardCorners() and cv2.calibrateCamera() to calculate the intrinsic parameters of each camera.
	3. Save the intrinsic parameters (camera matrix and distortion coefficients) for each camera.
2. Extrinsic Calibration of Cameras **DONE**
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
Ensure that both cameras are capturing images simultaneously to avoid any temporal misalignment. (adding chatgpt script to calibration testing but that's a problem for another day)
5. Display
   	1. Find out how to display SBS 3d content on the glasses using raspberry pi
7. Calibration with the HMD
To ensure the virtual imagery aligns with the real-world view seen through the HMD:
	1. Determine the position and orientation of the cameras relative to the HMD. This might involve physically measuring the distances and angles or using a tracking system.
	2. Calibrate the display parameters of the HMD, such as the field of view (FOV), eye-to-screen distance, and any lens distortion.
8. Alignment with User’s View
This step ensures that the stereoscopic vision aligns with the user's view through the HMD lenses:
	1. Display calibration patterns (like grids or crosshairs) on the HMD and align them with the real-world view.
	1. Adjust the virtual camera parameters (like the position and orientation) in the AR software to match the user's perspective through the HMD.
	1. Perform user testing and fine-tuning to ensure that the alignment feels natural and accurate.
9. Color Calibration (Optional)
If the color reproduction of the fluorescent imaging is critical, perform color calibration to ensure accurate color representation.
	1. Capture images of a color calibration target under the fluorescent lighting.
	2. Adjust the color balance and settings of the cameras to match the expected colors.
10. Latency Calibration:
	1. Measure and minimize the delay between camera capture and display output.
	2. This is crucial for maintaining a comfortable AR experience.
 11. Field of View (FOV) Matching:
	1. Ensure the cameras' FOV matches or slightly exceeds the HMD's FOV.
	2. Adjust camera placement or use lenses to match FOVs if necessary.
12. Depth Calibration:
	1. Calibrate the stereo system's depth perception to real-world measurements.
	2. This is important for accurate AR overlay placement.
13. User-specific Calibration:
	1. Develop a quick calibration routine for individual users to fine-tune the system.
	2. This might include adjusting for different face shapes and eye positions.
14. Dynamic Calibration:
	1. Implement a system to maintain calibration during use, accounting for potential shifts in camera or HMD position.
15. Fluorescence-specific Calibration:
	1. Calibrate the system for the specific fluorescent markers or dyes you're using.
	2. This may involve spectral calibration to accurately detect and display fluorescent signals.

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
- https://www.reddit.com/r/raspberry_pi/comments/5fz4jb/it_is_a_pita_to_find_the_datasheet_for_the_sony/
- https://github.com/rellimmot/Sony-IMX219-Raspberry-Pi-V2-CMOS

  	information about the camera
- https://forums.raspberrypi.com/viewtopic.php?t=351197
- 	3d tings
- OpenCV: For camera calibration, stereo rectification, and image processing.
- OpenHMD: For interfacing with various HMDs and obtaining HMD-specific parameters.
- ROS (Robot Operating System): For synchronization and handling multiple sensor data streams if needed.
