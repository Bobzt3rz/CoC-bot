from vision import Vision
import cv2 as cv
import numpy as np
from hsvfilter import HsvFilter



img = cv.imread("testbase.jpg")
cv.imshow('test', img)
if cv.waitKey(0) == ord('q'):
    cv.destroyAllWindows()

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
cv.imshow('test', hsv)
if cv.waitKey(0) == ord('q'):
    cv.destroyAllWindows()

def get_hsv_filter_from_controls(self):
    # Get current positions of all trackbars
    hsv_filter = HsvFilter()
    hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
    hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
    hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
    hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
    hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
    hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
    hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
    hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
    hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
    hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
    return hsv_filter
