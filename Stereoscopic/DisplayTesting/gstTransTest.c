// Install dependencies: sudo apt-get update \ sudo apt-get install libdrm-dev gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly build-essential
// compile command (hopefully): gcc -o drm_gstreamer drm_gstreamer.c -ldrm

#include <fcntl.h>
#include <xf86drm.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void start_gstreamer_pipeline() {
    // Start your GStreamer pipeline here
    system("gst-launch-1.0 filesrc location=image1.jpg ! jpegdec ! videoconvert ! videoscale ! video/x-raw,width=1920,height=1080,format=RGB ! alpha alpha=0.0 ! video/x-raw,width=1920,height=1080,format=RGBA ! kmssink driver-name=vc4 connector-id=32 plane-id=84 render-rectangle="<0,0,1920,1080>"");
}

int main() {
    int fd = open("/dev/dri/card0", O_RDWR | O_CLOEXEC);
    if (fd < 0) {
        perror("open");
        return EXIT_FAILURE;
    }

    if (drmSetMaster(fd) < 0) {
        perror("drmSetMaster");
        close(fd);
        return EXIT_FAILURE;
    }
    printf("DRM master set successfully.\n");

    start_gstreamer_pipeline();

    if (drmDropMaster(fd) < 0) {
        perror("drmDropMaster");
        close(fd);
        return EXIT_FAILURE;
    }
    printf("DRM master dropped successfully.\n");

    close(fd);
    return EXIT_SUCCESS;
}
