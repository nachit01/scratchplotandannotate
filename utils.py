import cv2
import math

def AnnotateOnImage(img, top_left= (0, 0),area=100,color=(0,255,0),thickness=2):
    # Calculate the side length of the square
    side_length = math.sqrt(area)
    # Convert tuple to integer
    tl = tuple(int(x-side_length/2) for x in top_left)
    # Calculate the bottom-right coordinate
    bottom_right = (int(tl[0] + side_length), int(tl[1] + side_length))
    c=color  # Green color in BGR format
    th=thickness  # Thickness of the rectangle borde
    # Draw the rectangle on the image
    cv2.rectangle(img, tl, bottom_right, c, th)

