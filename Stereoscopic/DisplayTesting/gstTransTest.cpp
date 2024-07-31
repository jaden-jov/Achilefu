#include <opencv2/opencv.hpp>
using namespace cv;

#include <iostream>
using namespace std;

int main(){
    // Define pipelines
    VideoCapture cap("gst-launch-1.0 filesrc location=./image1.jpg ! jpegdec ! videoconvert ! video/x-raw, format=RGB ! alpha alpha=1.0 ! video/x-raw, format=RGBA ! appsink", CAP_GSTREAMER);
    VideoWriter out("appsrc ! videoconvert ! video/x-raw, format=RGBA ! kmssink ")
    
    // Define variables
    Mat frame;
    Size newSize(1920, 1080);
    Mat newframe;

    // Read and resize frame
    cap.read(frame);
    resize(frame, newframe, newSize);

    // Display
    out.write(newframe);
}