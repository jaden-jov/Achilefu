import cv2

def display_transparency(image_path):
    
    img = cv2.imread(image_path)
    b, g, r, a = cv2.split(img)
    mask = a>0
    b = b * mask
    g = g * mask
    r = r * mask
    img = cv2.merge([b, g, r, a])
    cv2.imshow("window", img)
    cv2.waitKey(0)
    

if __name__ == "__main__":
    display_transparency('./alphaTest.png')