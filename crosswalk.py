import cv2
import numpy as np


class Beadando:
    def __init__(self):
        self.img = cv2.imread("crosswalk.jpg", -1)
        self.contour_val = 500
        # self.img = cv2.resize(self.img, (800, 800))

    def thresh(self):
        _, self.thresh_gray = cv2.threshold(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY),
                                         150, 255, cv2.THRESH_BINARY)
        cv2.imshow('nev', self.thresh_gray)

    def contouring(self):
        self.contours, _ = cv2.findContours(self.thresh_gray,
                                          cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    def segment_large_objects(self):
        for c in self.contours:
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(c) < self.contour_val:
                continue

            # get the min area rect
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            # convert all coordinates floating point values to int
            box = np.int0(box)
            # draw a red 'nghien' rectangle
            cv2.drawContours(self.img, [box], 0, (0, 0, 255), 2)
            cv2.imshow('img', self.img)

    def save_img(self):
        cv2.imwrite("result.jpg", self.img)

    def run(self):
        self.thresh()
        self.contouring()
        self.segment_large_objects()
        # self.save_img()

        while True:
            key = cv2.waitKey(1)
            if key == 27:  # q
                break
        cv2.destroyAllWindows()


if __name__ == '__main__':
    beadando = Beadando()
    beadando.run()
