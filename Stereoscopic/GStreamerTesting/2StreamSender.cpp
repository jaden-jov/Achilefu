// Send streams from cameras 0 and 1 to laptop from rpi
// pipeline: gst-launch-1.0 libcamerasrc camera-name=/base/soc/i2c0mux/i2c@0/imx219@10 ! video/x-raw,width=640,height=480,framerate=30/1 ! v4l2convert ! v4l2h264enc ! 'video/x-h264,level=(string)4.2,profile=(string)baseline' ! h264parse ! rtph264pay config-interval=-1 ! udpsink host=172.17.141.179 port=5000 
#include <opencv2/opencv.hpp>
using namespace cv;

#include <iostream>
using namespace std;

int main(){
    String ip("172.17.141.179");
    VideoCapture cap0("gst-launch-1.0 libcamerasrc camera-name=/base/soc/i2c0mux/i2c@0/imx219@10 ! video/x-raw,width=640,height=480,framerate=30/1 ! appsink",CAP_GSTREAMER);
    VideoCapture cap1("gst-launch-1.0 libcamerasrc camera-name=/base/soc/i2c0mux/i2c@1/imx219@10 ! video/x-raw,width=640,height=480,framerate=30/1 ! appsink",CAP_GSTREAMER);
    VideoWriter out0("gst-launch-1.0 appsrc ! v4l2convert ! v4l2h264enc ! 'video/x-h264,level=(string)4.2,profile=(string)baseline' ! h264parse ! rtph264pay config-interval=-1 ! udpsink host=172.17.141.179 port=5000", 0, 30.0, {640, 480}, 1);
    VideoWriter out1("gst-launch-1.0 appsrc ! v4l2convert ! v4l2h264enc ! 'video/x-h264,level=(string)4.2,profile=(string)baseline' ! h264parse ! rtph264pay config-interval=-1 ! udpsink host=172.17.141.179 port=5001", 0, 30.0, {640, 480}, 1);
    
    //if(!cap0.isOpened() || !out0.isOpened() || !cap1.isOpened() || !out1.isOpened()){
    if(!cap0.isOpened() || !cap1.isOpened())
    {
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
