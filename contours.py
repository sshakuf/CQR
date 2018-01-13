import cv2
import numpy as np
import imutils
from imutils.video import FPS
from imutils.video import VideoStream

# Let's load a simple image with 3 black squares
# image = cv2.imread('images/shapes.jpg')
# cv2.imshow('Input Image', image)
# cv2.waitKey(0)

image = cv2.imread('IMG_2082.jpg')

# Grayscale
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# Find Canny edges
edged = cv2.Canny(gray, 30, 200)
# cv2.imshow('Canny Edges', edged)
# cv2.waitKey(0)

# Finding Contours
# Use a copy of your image e.g. edged.copy(), since findContours alters the image
_, contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# cv2.imshow('Canny Edges After Contouring', edged)
# cv2.waitKey(0)

print("Number of Contours found = " + str(len(contours)))


# Draw all contours
# Use '-1' as the 3rd parameter to draw all
cv2.drawContours(image, contours, -1, (0,255,0), 3)

cv2.imshow('Contours', image)
# cv2.waitKey(0)

k = cv2.waitKey(1) & 0xff
if k == 27 :
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()