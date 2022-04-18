import cv2
import numpy as np


class Beadando:
    def __init__(self):
        self.img = cv2.imread("crosswalk.jpg")
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.blurred = None
        self.threshed = None
        self.edged = None
        self.img_np_edge = None
        self.colored = None
        self.im_thresh = None

        self.color_red = [0, 0, 255]

    def base(self):
        cv2.imshow("base", self.img)

    def blur(self):
        self.blurred = cv2.GaussianBlur(self.gray, (15, 15), 6)
        cv2.imshow("blured", self.blurred)

    def thresh(self):
        ret, self.threshed = cv2.threshold(self.blurred, 100, 255, cv2.THRESH_BINARY)

    def segment(self):
        self.img_np_edge = np.ndarray(self.threshed.shape, self.threshed.dtype)
        self.img_np_edge.fill(0)
        self.img_np_edge[(self.threshed >= 1) & (self.threshed <= 255)] = 255
        cv2.imshow("segmented", self.img_np_edge)

    def color(self, img):
        self.colored = self.img.copy()
        self.colored[img > 0] = [0, 0, 255]
        cv2.imshow("colored", self.colored)

    def save_img(self):
        cv2.imwrite("result.jpg", self.colored)

    def run(self):
        self.base()
        self.blur()
        self.thresh()
        self.segment()
        self.color(self.img_np_edge)
        self.save_img()

        cv2.waitKey(0)

        while True:
            key = cv2.waitKey(1)
            if key == 27:
                break

        cv2.destroyAllWindows()


if __name__ == '__main__':
    beadando = Beadando()
    beadando.run()
