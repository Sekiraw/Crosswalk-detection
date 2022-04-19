import cv2
import numpy as np


class Beadando:
    def __init__(self):
        self.img = cv2.imread("crosswalk.jpg")
        self.img_lab = cv2.cvtColor(self.img, cv2.COLOR_BGR2Lab)

        self.blurred = None
        self.threshed = None
        self.edged = None
        self.img_np_edge = None
        self.colored = None
        self.im_thresh = None
        self.max_vals = None

        self.color_red = [0, 0, 255]

    def base(self):
        cv2.imshow("base", self.img)

    def blur(self):
        self.blurred = cv2.GaussianBlur(self.img_lab, (15, 15), 4)
        cv2.imshow("blured", self.blurred)

    def split(self):
        self.null, self.green, self.blue = cv2.split(self.img_lab)
        # we can give it the blurred one too
        lower = 90
        upper = 255
        self.null[self.null > upper] = upper
        self.null[self.null < lower] = lower
        self.max_vals = cv2.normalize(self.null, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        cv2.imshow("gr", self.max_vals)

    def thresh(self):
        ret, self.threshed = cv2.threshold(self.max_vals, 100, 255, cv2.THRESH_BINARY)

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
        self.split()
        self.thresh()
        self.segment()
        self.color(self.img_np_edge)
        self.save_img()

        while True:
            key = cv2.waitKey(1)
            if key == 27:  # q
                break
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    beadando = Beadando()
    beadando.run()
