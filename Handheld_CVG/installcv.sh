#!/usr/bin/bash

# Install dependencies
sudo apt-get update
sudo apt-get install -y build-essential cmake git libgtk2.0-dev pkg-config \
                        libavcodec-dev libavformat-dev libswscale-dev \
                        libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
                        python3-dev python3-numpy libx264-dev libjpeg-dev

# Install remaining GStreamer plugins
sudo apt-get install -y libgstreamer-plugins-bad1.0-dev \
                        gstreamer1.0-plugins-ugly \
                        gstreamer1.0-tools \
                        gstreamer1.0-gl \
                        gstreamer1.0-gtk3

# Clone OpenCV repository
cd ~
git clone https://github.com/opencv/opencv.git
cd opencv
git checkout 4.9.0

# Create build directory
mkdir build
cd build

# Configure build with GStreamer support
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_GENERATE_PKGCONFIG=YES \
      -D WITH_GSTREAMER=YES \
      -D WITH_GSTREAMER_0_10=OFF \
      -D WITH_FFMPEG=YES \
      -D WITH_OPENEXR=YES \
      -D BUILD_EXAMPLES=NO \
      -D BUILD_opencv_python2=NO \
      -D BUILD_opencv_python3=YES \
      -D PYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3 \
      -D OPENCV_PYTHON3_INSTALL_PATH=/usr/local/lib/python${PYTHON_VERSION}/dist-packages \
      -D OPENCV_ENABLE_NONFREE=YES \
      -D INSTALL_PYTHON_EXAMPLES=NO ..

# Build OpenCV
make -j$(nproc)

# Install OpenCV
sudo make install
sudo ldconfig

python3 -c "import cv2; print(cv2.__version__); print(cv2.getBuildInformation())"
