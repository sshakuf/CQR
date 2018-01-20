# import the necessary packages
import argparse
import cv2

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = (0,0)
cropping = False

font = cv2.FONT_HERSHEY_SIMPLEX


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping
    refPt = (x, y)
    
    
	# # if the left mouse button was clicked, record the starting
	# # (x, y) coordinates and indicate that cropping is being
	# # performed
    # if event == cv2.EVENT_LBUTTONDOWN:
    #     refPt = [(x, y)]
    #     cropping = True

    # # check to see if the left mouse button was released
    # elif event == cv2.EVENT_LBUTTONUP:
    #     # record the ending (x, y) coordinates and indicate that
    #     # the cropping operation is finished
    #     refPt.append((x, y))
    #     cropping = False

    #     # draw a rectangle around the region of interest
    #     cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
    #     cv2.imshow("image", image)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="Path to the image", default = 'Images/IMG_2082_1008.jpg')
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
    clone = image.copy()
    
    (x, y) = refPt
    g = image[y][x][0]
    b = image[y][x][1]
    r = image[y][x][2]
    txt = "x={0}, y={1} r={2}, g={3}, b={4}".format( x,y,r,g,b )
    cv2.putText(clone, txt, (230, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("image", clone)
    # cv2.imshow("image", image[:][:][1])

    # display the image and wait for a keypress
    # cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        image = clone.copy()

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break

# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
	cv2.imshow("ROI", roi)
	cv2.waitKey(0)
 
# close all open windows
cv2.destroyAllWindows()







# b = image.copy()
# # set green and red channels to 0
# b[:, :, 1] = 0
# b[:, :, 2] = 0


# g = image.copy()
# # set blue and red channels to 0
# g[:, :, 0] = 0
# g[:, :, 2] = 0

# r = image.copy()
# # set blue and green channels to 0
# r[:, :, 0] = 0
# r[:, :, 1] = 0


# # RGB - Blue
# cv2.imshow('B-RGB', b)

# # RGB - Green
# cv2.imshow('G-RGB', g)

# # RGB - Red
# cv2.imshow('R-RGB', r)

