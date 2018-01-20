import cv2
import numpy as np
import imutils
from imutils.video import FPS
from imutils.video import VideoStream
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,default = 'Images/IMG_2082_1008.jpg',
	help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args['image'])

def nothing(x):
    pass

cv2.namedWindow('Image')
cv2.createTrackbar('R','Image',20,255,nothing)  #100
cv2.createTrackbar('V','Image',5,255,nothing)  #200

# r = cv2.getTrackbarPos('R','image')

import cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
# if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.90 and ar <= 1.05 else "rectangle"
            # if w > 30:
            #     shape ="QR"

		# if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"

        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"

        # return the name of the shape
        return shape




sd = ShapeDetector()
ratio =1


run = 1

if (run==1):
    resized = imutils.resize(image, width=600)
    ratio = image.shape[0] / float(resized.shape[0])
    
    # Grayscale
    gray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
    while (True):
        # Find Canny edges
        r = cv2.getTrackbarPos('R','Image')
        v = cv2.getTrackbarPos('V','Image')
        
        edged = cv2.Canny(gray, r, v)
        # Finding Contours
        # Use a copy of your image e.g. edged.copy(), since findContours alters the image
        # _, contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.dilate(edged,kernel,iterations = 1)
        dst = cv2.bitwise_not ( closed)

        _, contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            area = cv2.contourArea(c, False)
            if (area >200):
                shape = sd.detect(c)
                # c = c.astype("float")
                # c *= ratio
                # c = c.astype("int")
                cv2.drawContours(resized, [c], -1, (0, 255, 0), 2)
            # print (area)


        # closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        cv2.imshow("Closed", dst)
        cv2.waitKey(1)

        print("Number of Contours found = " + str(len(contours)))
        cnts =  contours
        cv2.imshow("Image", resized)
        cv2.waitKey(500)
        # break    
    
    

if (run==2):
    resized = imutils.resize(image, width=600)
    ratio = image.shape[0] / float(resized.shape[0])
    gray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Image", thresh)
    cv2.waitKey(0)
    
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    contours = cnts

# loop over the contours
# cv2.drawContours(image, contours, -1, (0,255,0), 3)
print("Number of Contours found = " + str(len(contours)))
i=0
for c in cnts:
    print(i)
    i=i+1
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    M = cv2.moments(c)

    shape =''
    if (M["m00"] > 0):
        shape = sd.detect(c)

    if (shape == 'rectangle' ):#or shape == 'rectangle'):
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        # cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(1)

# Draw all contours
# Use '-1' as the 3rd parameter to draw all
# cv2.drawContours(image, contours, -1, (0,255,0), 3)

cv2.imshow('Contours', image)
# cv2.waitKey(0)

cv2.waitKey(0)
# k = cv2.waitKey(1) & 0xff
# if k == 27 :
#     print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
#     print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()