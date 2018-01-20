import cv2
import numpy as np
import imutils
from imutils.video import FPS
from imutils.video import VideoStream
import argparse
from pprint import pprint


def nothing(x):
    pass

# cv2.namedWindow('Image')
# cv2.createTrackbar('R','Image',20,255,nothing)  #100
# cv2.createTrackbar('V','Image',5,255,nothing)  #200

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


class QRDetector:
    def __init__(self):
        self._rects = []
        self._QRrects = []
        self.ColorRects = {}
        self.minColorBoxArea = 200
        self.maxDiffVertical = 5
        self.maxSpaceBetweenX = 10
        self.maxSpaceBetweenY = 10
        self.colorTreshhold = 150
        self.colorGrayTreshhold = 130
        pass

    def GetBoundingBox(self, c):
        found = False
        (x, y, w, h) = (0,0,0,0)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        if len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            found = True

        return found, np.array([x, y, w, h])

    # def VerifyBoxesAsQR(self):
    #     if len(self._rects)
    #     for (r in self._rects)

    def CheckSiblingRect(self, r1, r2):
        (dx,dy,dw,dh) = r2 - r1
        if (dx ==0 and dy == 0):
            return False
        if (dx < self.maxDiffVertical): #rects are vertical
            #check that the space between is not larger than maxSpaceBetweenY
            if (dy < self.maxSpaceBetweenY): #check that the space between is not larger than maxSpaceBetweenX
                return True
        elif (dy < self.maxDiffVertical): #rects are horizontal
            if (dx < self.maxSpaceBetweenX): #check that the space between is not larger than maxSpaceBetweenX
                return True
        return False

    def AppendRects(self, r,blue, green,red):
        dontAdd = False
        (x,y,w,h) = r
        for q in self._QRrects:
            (x1,y1,_,_) = q['rect']
            if (x==x1 and y==y1 ):
                dontAdd = True
        if dontAdd == False:
            self._QRrects.append({'rect':(r), 'RGB':(red,green,blue)})


    def IdentifyColor(self, r):
        # get the RBG of the rect in the middle 
        (x,y,w,h) = r
        px = x+(w/2)
        py = y+(h/2)
        blue = self.image[py,px,0]
        green = self.image[py,px,1]
        red = self.image[py,px,2]
        # print ("PX=" + str(px) + " PY=" + str(py) + ": B=" + str(blue) + ", G=" +str(green) + " R="+str(red))
        self.AppendRects(r,blue, green,red)

    def IdentifyColorRects(self):
        for r in self._rects:
            self.IdentifySibilingRect(r)

    def IdentifySibilingRect(self, r1):
        #find 4 rects that are simular and are horizontal
        #make sure we have 4 rects atleast
        for i in range(len(self._rects)-1):
            if (self.CheckSiblingRect(r1, self._rects[i])):
                self.IdentifyColor(r1)
                self.IdentifyColor(self._rects[i])
                break



    def getQRRects(self, image):
        self.image = image
        self.resized = imutils.resize(image, width=600)
        ratio = image.shape[0] / float(self.resized.shape[0])

        # Grayscale
        gray = cv2.cvtColor(self.resized,cv2.COLOR_BGR2GRAY)
        # Find Canny edges
        r = 20 # cv2.getTrackbarPos('R','Image')
        v = 5 # cv2.getTrackbarPos('V','Image')
        
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
            if (area > self.minColorBoxArea):
                # shape = sd.detect(c)
                found, rect = self.GetBoundingBox(c)
                if (found):
                    rect = rect.astype("float")
                    rect *= ratio
                    rect = rect.astype("int")
                    self._rects.append(rect)
                    cv2.drawContours(self.resized, [c], -1, (0, 255, 0), 2)

                    c = c.astype("float")
                    c *= ratio
                    c = c.astype("int")
                    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)


            # print (area)
        self.IdentifyColorRects()

        for r in self._QRrects:
            # for i in range(r['rect'][3]):
            #     for j in range(r['rect'][2]):
            #         image[r['rect'][1]+i,r['rect'][0]+j,0]=0    
            #         image[r['rect'][1]+i,r['rect'][0]+j,1]=0    
            #         image[r['rect'][1]+i,r['rect'][0]+j,2]=0    
            # print ("X=" + str(r['rect'][0]) + " Y=" + str(r['rect'][1]) + ": R=" + str(r['RGB'][0]) + ", G=" +str(r['RGB'][1]) + " B="+str(r['RGB'][2]))
            R = r['RGB'][0]
            G = r['RGB'][1]
            B = r['RGB'][2]

            if (R >= self.colorTreshhold and G < self.colorTreshhold and B < self.colorTreshhold ):
                self.ColorRects['Red'] = (R,G,B)
            elif (R < self.colorTreshhold and G >= self.colorTreshhold and B < self.colorTreshhold ):
                self.ColorRects['Green'] = (R,G,B)
            elif (R < self.colorTreshhold and G < self.colorTreshhold and B >= self.colorTreshhold ):
                self.ColorRects['Blue'] = (R,G,B)
            elif (R >= self.colorGrayTreshhold and G >= self.colorGrayTreshhold and B >= self.colorGrayTreshhold ):
                self.ColorRects['Gray'] = (R,G,B)
            
            # cv2.imshow("Image", image)
            # cv2.waitKey()

        pass

        # closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow("Closed", dst)
        # cv2.waitKey(1)

        # cv2.imshow("resized", self.resized)
        # cv2.imshow("Image", image)
        # cv2.waitKey()
        
        # cv2.destroyAllWindows()


if __name__ == '__main__' :

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False,default = 'Images/IMG_2082_1008.jpg',
        help="path to the input image")
    args = vars(ap.parse_args())

    image = cv2.imread(args['image'])


    qr = QRDetector()
    qr.getQRRects(image)
    pprint (qr.ColorRects)    

    #adjust Colors 
    

    red = image[:,:,2]
    green = image[:,:,1]
    blue = image[:,:,0]

    red = red + 100    

    image2 = cv2.merge((blue, green, red)) # merge channels into one BGR image
    cv2.imshow("Image", image2)
    cv2.waitKey()
