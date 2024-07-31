#include <opencv2/opencv.hpp>
using namespace cv;

#include <iostream>
using namespace std;

int main(){
    VideoCapture cap("gst-launch-1.0 filesrc location=./image1.jpg ! jpegdec ! videoconvert ! video/x-raw, format=RGB ! alpha alpha=1.0 ! video/x-raw, format=RGBA ! appsink", CAP_GSTREAMER);
    VideoWriter out("appsrc ! videoconvert ! video/x-raw, format=RGBA ! kmssink ")
    Mat frame;
    cap.read(frame);
    out.write(frame);
}