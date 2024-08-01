// UNTESTED chatgpt vomit
#include <fcntl.h>
#include <xf86drm.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    int fd;

    // Open the DRM device
    fd = open("/dev/dri/card0", O_RDWR | O_CLOEXEC); // New master will be card0
    if (fd < 0) {
        perror("open");
        return EXIT_FAILURE;
    }

    // Set DRM master
    if (drmSetMaster(fd) < 0) {
        perror("drmSetMaster");
        close(fd);
        return EXIT_FAILURE;
    }
    printf("DRM master set successfully.\n");

    // Perform your rendering operations here

    // Drop DRM master
    if (drmDropMaster(fd) < 0) {
        perror("drmDropMaster");
        close(fd);
        return EXIT_FAILURE;
    }
    printf("DRM master dropped successfully.\n");

    close(fd);
    return EXIT_SUCCESS;
}
