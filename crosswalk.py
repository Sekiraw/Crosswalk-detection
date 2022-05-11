import cv2
import numpy as np


class Beadando:
    def __init__(self, location, result_name):
        input = cv2.imread(location)

        # setup
        self.res_name = result_name
        self.img = None
        self.thresh = None
        self.contours = None

        # resize the image if its too big
        self.resize(input)

    def resize(self, input):
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
        # a 2. blur nélkül pontatlanabb a színek detektálása
        kernel = np.ones((5, 5), np.uint8)
        morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
        return morph

    def filter_by_area(self, morph):
        self.contours = self.img.copy()

        contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 2:
            contours = contours[0]
        else:
            contours = contours[1]

        for c in contours:
            area = cv2.contourArea(c)
            if area > 800:
                cv2.drawContours(self.contours, [c], -1, (0, 0, 255), thickness=cv2.FILLED)

    def s_and_s(self):
        cv2.imwrite("result-of-" + self.res_name + ".jpg", self.contours)
        cv2.imshow("Eredmeny-" + self.res_name, self.contours)

    def run(self):
        self.filter_by_area(self.filter())
        self.s_and_s()


if __name__ == "__main__":
    kep1 = Beadando('1.jpeg', "kep1")
    kep2 = Beadando('2.jpg', "kep2")
    kep3 = Beadando('3.png', "kep3")
    kep1.run()
    kep2.run()
    kep3.run()

    cv2.waitKey(0)
