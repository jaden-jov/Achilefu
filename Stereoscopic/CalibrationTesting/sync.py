import time
import threading
import libcamera
from libcamera import controls
import numpy as np
import cv2

class CameraCapture(threading.Thread):
    def __init__(self, camera_id, camera_manager, lock, images):
        threading.Thread.__init__(self)
        self.camera_id = camera_id
        self.camera_manager = camera_manager
        self.lock = lock
        self.images = images

    def run(self):
        camera = self.camera_manager.get(self.camera_id)
        config = camera.generate_configuration([libcamera.StreamRole.Viewfinder])
        stream = config.at(0)
        stream.pixel_format = 'BGR888'
        stream.size = (640, 480)
        camera.configure(config)

        # Create a request
        buffer = np.empty((stream.size.height, stream.size.width, 3), dtype=np.uint8)
        request = camera.create_request()
        request.add_buffer(stream, buffer)

        camera.start()

        while True:
            camera.queue_request(request)
            request = camera.dequeue_request()
            with self.lock:
                self.images[self.camera_id] = buffer.copy()

            time.sleep(0.033)  # Wait for roughly 30 FPS

        camera.stop()

def main():
    camera_manager = libcamera.CameraManager()
    camera_manager.start()

    if len(camera_manager.cameras) < 2:
        print("Error: Two cameras are required.")
        return

    images = [None, None]
    lock = threading.Lock()

    cam1_thread = CameraCapture(0, camera_manager, lock, images)
    cam2_thread = CameraCapture(1, camera_manager, lock, images)

    cam1_thread.start()
    cam2_thread.start()

    while True:
        with lock:
            img1 = images[0]
            img2 = images[1]

        if img1 is not None and img2 is not None:
            cv2.imshow('Camera 1', img1)
            cv2.imshow('Camera 2', img2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam1_thread.join()
    cam2_thread.join()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
