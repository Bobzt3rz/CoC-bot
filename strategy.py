import threading
import math
import cv2 as cv
import numpy as np
import imutils
from statistics import mean

class Strategy(threading.Thread):

    # threading properties
    running = True
    lock = None
    placeable_points = None

    def __init__(self):
        #initalize thread from thread class
        threading.Thread.__init__(self)
        #create a lock
        self.lock = threading.Lock()

        self.placeable_points = None

    def get_placement_points(self, target_points, placeable_points):
        for target_point in target_points:
            min_distance = 999999
            for placeable_point in placeable_points:
                distance = int(math.sqrt((target_point[1]-placeable_point[1])**2 + (target_point[0]-placeable_point[0])**2))
                if distance < min_distance:
                    min_distance = distance
                    print(min_distance)

    def find_placeable_points(self, image):
        blur = cv.GaussianBlur(image, (5,5), cv.BORDER_DEFAULT)
        gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
        kernel = np.ones((5,5), np.uint8)
        erode = cv.erode(gray, kernel, iterations=2)
        thresh = cv.threshold(erode, 100, 255, cv.THRESH_BINARY)[1]

        # Gets rid of areas that are smaller than desired
        cnts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)
        rect_areas = []
        # this method of using boundingrect may be problematic since its detecting only rectangles
        for c in cnts:
            (x, y, w, h) = cv.boundingRect(c)
            rect_areas.append(w * h)
        avg_area = mean(rect_areas)
        for c in cnts:
            (x, y, w, h) = cv.boundingRect(c)
            cnt_area = w * h
            if cnt_area < 4 * avg_area:
                thresh[y:y + h, x:x + w] = 0

        # Find placeable edge points for each contour
        placeable_edge_cnts, h = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        approx_edge_cnts = []

        # approximate points so there are less points for each contour
        for contours in placeable_edge_cnts:
            epsilon = 0.00025*cv.arcLength(contours,True)
            approx_edge_points = cv.approxPolyDP(contours,epsilon,False)
            approx_edge_cnts.append(approx_edge_points)

        self.lock.acquire()
        self.placeable_points = approx_edge_cnts
        self.lock.release()

    def stop(self):
        self.running = False

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while self.running:
            pass