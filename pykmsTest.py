import pykms
import time

# Initialize KMS
kms = pykms.KMS()

# Set a resolution (e.g., 1920x1080)
width, height = 1920, 1080
kms.set_mode(width, height)

# Create a framebuffer
fb = kms.create_framebuffer(width, height, format=pykms.PixelFormat.ARGB8888)

# Clear the framebuffer to black
fb.clear()

# Draw something (for example, a simple red rectangle)
fb.draw_rect(100, 100, 200, 200, color=(255, 0, 0, 255))

# Flip the framebuffer to the display
kms.flip(fb)

# Keep the display on for 10 seconds
time.sleep(10)
