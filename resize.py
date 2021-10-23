import cv2 as cv
import numpy as np
import time
from vision import Vision

class Resize:
    def __init__(self):
        pass

    def resize_needle(self, img_path):
        base = cv.imread("hsv_image/testbase.jpg", cv.IMREAD_UNCHANGED)
        img = cv.imread(img_path, cv.IMREAD_UNCHANGED)
        print("dimensions: : ", img.shape)
        #loop through from 20% to 200% for needle image spaced out evenly 10 times
        for scale in np.linspace(0.2, 2.0, 10):
            width = int(img.shape[1] * scale)
            height = int(img.shape[0] * scale)
            dim = (width, height)
            resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
            # cv.imshow("Resized", resized)
            # cv.waitKey(0)
            # cv.destroyAllWindows()

            result = cv.matchTemplate(base, resized, cv.TM_CCOEFF_NORMED)
            (_, maxVal, _, maxLoc) = cv.minMaxLoc(result)
            print("maxVal: {} maxLoc: {}".format(maxVal, maxLoc))

            img_w = img.shape[1]
            img_h = img.shape[0]
            rect = [int(maxLoc[0]), int(maxLoc[1]), img_w, img_h]



        
vision = Vision()
resize = Resize()

resize.resize_needle("hsv_image\Elixir_Collector13.png")


