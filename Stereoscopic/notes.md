# Stereoscopic Notes

GStreamerTesting contains a working pipeling that takes two camera streams and displays them side by side, the single stream test is in Handheld CVG 
Next step is to learn how the frames need to be transformed to produce stereovision

## PROBLEM

The challenge is to implement stereoscopic NIR imaging in the CVG headset

## BRAINSTORM
1. 2 camera setups, project each separately onto the eyes, easiest solution
2. depth mapping with structured light, turn that into stereoscopic vision
3. polarized 3d, personal favorite, glasses have a 120 hz display so its definitely possible 4
4. might have to use gstreamer, as rpi cannot support 4 cameras -could just use two cameras, just for IR? AR type final product

## PLAN
1. get two images to display side by side using openCV **Complete**
2. get two streams to display side by side using openCV **Too easy**
3. get two streams to display side by side using gstreamer **Complete**
4. look into the matrix transformation things

## RESOURCES
Mela-2015-Stereoscopic Integrated Imaging Gogg.pdf
	check the Image Acquisition, Processing, Registration and Display 
 	section for information on how they aligned their cameras mathematically
https://lubosz.wordpress.com/2016/07/04/introducing-gstreamer-vr-plug-ins-
and-sphvr/
	Gstreamer stereoscopic things
https://lubosz.wordpress.com/2013/08/28/view-side-by-side-stereoscopic-
video-with-gstreamer-and-oculus-rift/
	anotha one
hconcat (opencv) concatenates two images horizontally
https://coaxion.net/blog/2014/08/concatenate-multiple-streams-gaplessly-
with-gstreamer/
	concatenate with gstreamer
https://github.com/simondlevy/OpenCV_GStreamer/blob/master/Source/Sender.cpp
	example gstreamer cpp code, use as template
https://github.com/Digital1O1/Onboard_VS_Streaming_LINUX/blob/main
/Testing%20Dual%20GStreamerPipeline/main.cpp
	Chris's work for receiver, use as reference but not too much useful here
https://github.com/Digital1O1/Onboard_VS_Streaming_RPI/blob/master/
GStreamer%20Folder/GStreamer%20Dual%20Pipeline/doubleCameraPipeline.sh
	Chris RPI thing
https://stackoverflow.com/questions/46219454/how-to-open-a-gstreamer-
pipeline-from-opencv-with-videowriter
	useful template for cpp gstreamer code
https://indico.freedesktop.org/event/5/contributions/255/attachments/112/170/
%5BFINAL%5D%20libcamerasrc_%20Introduction%20and%20usage%20of%20libcamera%
27s%20GStreamer%20element.pdf
	libcamerasrc info
