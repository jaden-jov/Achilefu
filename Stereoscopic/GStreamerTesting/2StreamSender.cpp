// Send streams from cameras 0 and 1 to laptop from rpi
#include <opencv2/opencv.hpp>
#include <openc2/videoio.hpp>
using namespace cv;

#include <iostream>
using namespace std;

int main(){
    String ip("172.17.141.179");
    VideoCapture cap0("libcamerasrc camera-name=/dev/video0 ! video/x-raw,width=640,height=480,framerate=30/1 ! appsink",CAP_GSTREAMER);
    VideoCapture cap1("libcamerasrc camera-name=/dev/video1 ! video/x-raw,width=640,height=480,framerate=30/1 ! appsink",CAP_GSTREAMER);
    VideoWriter out0("appsrc ! v4l2convert ! v4l2h264enc ! 'video/x-h264,level=(string)4.2,profile=(string)baseline' ! h264parse ! rtph264pay config-interval=-1 ! udpsink host="+ip+" port=5000");
    VideoWriter out1("appsrc ! v4l2convert ! v4l2h264enc ! 'video/x-h264,level=(string)4.2,profile=(string)baseline' ! h264parse ! rtph264pay config-interval=-1 ! udpsink host="+ip+" port=5001");
    
    if(!cap0.isOpened() || !out0.isOpened() || !cap1.isOpened() || !out1.isOpened()){
        cout << "Something did not open correctly" << endl;
        exit(-1);
    }

    Mat frame0;
    Mat frame1;

    while(true){
        cap0.read(frame0);
        cap1.read(frame1);
        if(frame0.empty() || frame1.empty()){
            break;
        }
        out0.write(frame0);
        out1.write(frame1);
        if(waitKey(1)=='q'){
            break;
        }
    }
    }