import pygame
import sys

def display_sbs_3d_image(image_path):
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

    try:
        # Load the image
        image = pygame.image.load(image_path)
        
        # Resize the image if it's not exactly 1280x480
        if image.get_size() != (1920, 1080):
            image = pygame.transform.scale(image, (1920, 1080))
        
        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

            # Draw the image
            screen.blit(image, (0, 0))

            # Update the display
            pygame.display.flip()

    except pygame.error as e:
        print(f"Error loading image: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Replace 'path_to_your_image.jpg' with the actual path to your SBS 3D image
    display_sbs_3d_image('./wideTest.jpg')