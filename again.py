import cv2
import numpy as np

def a():
    img = cv2.imread("crosswalk.jpg", cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray,
                               (15, 15), 6)

    ret, thresh = cv2.threshold(blurred,
                                180, 255,
                                cv2.THRESH_BINARY)

    contours, hier = cv2.findContours(thresh.copy(),
                                      cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        # if the contour is not sufficiently large, ignore it
        if  cv2.contourArea(c) < 500:
            continue

        # get the min area rect
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        # convert all coordinates floating point values to int
        box = np.int0(box)
        # draw a red 'nghien' rectangle
        cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
        cv2.imshow('img', img)
        cv2.imshow("contours", img)

def b():
    image = cv2.imread('crosswalk.jpg', -1)
    ret, thresh_gray = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
                                     150, 255, cv2.THRESH_BINARY)
    contours, hier = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        if cv2.contourArea(c) < 1000:
            continue
        print(c)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        # convert all coordinates floating point values to int
        box = np.int0(box)
        # draw a green 'nghien' rectangle
        cv2.drawContours(image, [box], 0, (0, 255, 0), 1)

    cv2.imshow('paper', image)

    cv2.waitKey(0)

while True:
    b()
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()