import pykms
import numpy as np
from PIL import Image

def load_image(path):
    with Image.open(path) as img:
        img = img.convert('RGBA')
        return np.array(img, dtype=np.uint8)

def main():
    # Initialize KMS
    card = pykms.Card()
    res = pykms.ResourceManager(card)
    conn = res.reserve_connector()
    crtc = res.reserve_crtc(conn)
    
    # Find 1920x1080 mode
    mode = conn.get_mode(1920, 1080)
    
    # Create framebuffer
    fb = pykms.DumbFramebuffer(card, mode.hdisplay, mode.vdisplay, "XR24")
    crtc.set_mode(conn, fb, mode)

    # Map the framebuffer
    buf = fb.map(pykms.DrmFormat.XRGB8888)

    # Load image
    image = load_image('./transTest.png')

    # Render image to buffer, skipping transparent pixels
    # for y in range(mode.vdisplay):
    #     for x in range(mode.hdisplay):
    #         r, g, b, a = image[y, x]
    #         if a > 0:
    #             offset = (y * mode.hdisplay + x) * 4
    #             buf[offset:offset+4] = [b, g, r, 255]

    # Create a mask for non-transparent pixels
    mask = image[:, :, 3] > 0

    # Prepare the buffer data
    buffer_data = np.zeros((mode.vdisplay, mode.hdisplay, 4), dtype=np.uint8)
    buffer_data[mask] = image[mask]
    buffer_data[:, :, 3] = 255  # Set alpha to 255 for all non-transparent pixels
    
    # Flatten and copy the data to the buffer
    np.copyto(buf, buffer_data.flatten())

    # Keep the program running
    input("Press Enter to exit...")

    # Clean up
    crtc.set_mode(None)

if __name__ == "__main__":
    main()