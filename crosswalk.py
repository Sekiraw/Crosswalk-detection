import cv2
import numpy as np


class Beadando:
    def __init__(self):
        input = cv2.imread('3.png')

        # resize the image if its too big
        self.size(input)

        self.contours_combined = []

    def size(self, input):
        # print("input shapes \n" + str(input.shape[0]) + " height \n" + str(input.shape[1]) + " width")

        if input.shape[0] > 1000 or input.shape[1] > 1000:
            scale_percent = 60  # percent of original size
            width = int(input.shape[1] * scale_percent / 100)
            height = int(input.shape[0] * scale_percent / 100)
            dim = (width, height)
        else:
            dim = (input.shape[1], input.shape[0])
        # print(dim)

        self.img = cv2.resize(input, dim, interpolation=cv2.INTER_AREA)

    def filter(self):
        _, self.thresh = cv2.threshold(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY),
                                            140, 255, cv2.THRESH_BINARY)

        kernel = np.ones((3, 3), np.uint8)
        morph = cv2.morphologyEx(self.thresh, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((5, 5), np.uint8)
        morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
        return morph

    def filter_by_area(self, morph):
        cntrs = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cntrs = cntrs[0] if len(cntrs) == 2 else cntrs[1]
        self.contours = self.img.copy()
        good_contours = []
        for c in cntrs:
            area = cv2.contourArea(c)
            if area > 800:
                cv2.drawContours(self.contours, [c], -1, (0, 0, 255), thickness=cv2.FILLED)
                good_contours.append(c)

        # combine good contours
        self.contours_combined = np.vstack(good_contours)

        return self.contours_combined

    def s_and_s(self):
        cv2.imwrite("eredmeny.jpg", self.contours)

        cv2.imshow("Eredmeny", self.contours)

    def run(self):
        self.filter_by_area(self.filter())
        self.s_and_s()

        cv2.waitKey(0)


if __name__ == "__main__":
    bead = Beadando()
    bead.run()