import pykms
import numpy as np # allows matrix operations and greatly reduces runtime by removing the need to iterate through pixels with a for loop
from PIL import Image
import contextlib # make sure everything closes even when theres an error

def load_image(path):
    with Image.open(path) as img:
        img = img.convert('RGBA')
        return np.array(img, dtype=np.uint8)

@contextlib.contextmanager
def kms_context():
    card = pykms.Card()
    res = pykms.ResourceManager(card)
    conn = res.reserve_connector()
    crtc = res.reserve_crtc(conn)
    try:
        yield card, res, conn, crtc
    finally:
        crtc.disable_mode()

def main():
    # Initialize KMS
    with kms_context() as (card, res, conn, crtc):
        
        # Find 1920x1080 mode
        modes = conn.get_modes()
        mode = next((m for m in modes if m.hdisplay == 1920 and m.vdisplay == 1080), None)
        
        # Create framebuffer
        fb = pykms.DumbFramebuffer(card, mode.hdisplay, mode.vdisplay, "XR24")
        crtc.set_mode(conn, fb, mode)

        # Map the framebuffer
        # buf = fb.map(pykms.DrmFormat.XRGB8888) << bad syntax, keeping because that is the correct format for the image
        mapping = fb.map()
        buf = mapping.data

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
        mask = image[..., 3] > 0

        # Prepare the buffer data, making sure to convert from rgba to xrgb
        buffer_data = np.zeros((mode.vdisplay, mode.hdisplay, 4), dtype=np.uint8)
        buffer_data[mask, 0 ] = 255
        buffer_data[mask, 1:] = image[mask, :3] 
        
        # Flatten and copy the data to the buffer
        np.copyto(buf, buffer_data.flatten())

        # Keep the program running
        input("Press Enter to exit...")

        # Clean up
        crtc.disable_mode()

if __name__ == "__main__":
    main()