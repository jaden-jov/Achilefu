// receive and display rpi streams (hopefully) side by side
#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/core.hpp>
using namespace cv;

#include <iostream>
using namespace std;

int main(){
    VideoCapture cap0("gst-launch-1.0 udpsrc port=5000 caps=application/x-rtp ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink",CAP_GSTREAMER);
    VideoCapture cap1("gst-launch-1.0 udpsrc port=5001 caps=application/x-rtp ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink",CAP_GSTREAMER);
    if(!cap0.isOpened() || !cap1.isOpened())
    {
        cout<<"VideoCapture not opened"<<endl;
        exit(-1);
    }

    Mat frame0;
    Mat frame1;
    Mat frame;

    while(true){
        cap0.read(frame0);
        cap1.read(frame1);
        if(frame0.empty() || frame1.empty()){
            break;
        }
        hconcat(frame0,frame1,frame);
        imshow("Receiver", frame);
        if(waitKey(1)=='q'){
            break;
        }
    }
    destroyWindow("Receiver");
}