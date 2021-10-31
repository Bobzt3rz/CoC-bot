import cv2 as cv
import numpy as np
import threading
from time import time



class Detection(threading.Thread):

    # threading properties
    running = True
    lock = None
    rectangles = []
    # properties
    screenshot = None
    method = None
    needle_img = None
    needle_w = 0
    needle_h = 0
    threshold = 0
    max_results = 0

    def __init__(self, needle_img_path, method = cv.TM_CCOEFF_NORMED, threshold = 0.4, max_results = 10):
        #initalize thread from thread class
        threading.Thread.__init__(self)
        #create a lock
        self.lock = threading.Lock()
        # load the needle image
        self.method = method
        # haystack_img = cv.imread(haystack_img_path, cv.IMREAD_UNCHANGED)
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
        #load detection threshold and max max_results
        self.threshold = threshold
        self.max_results = max_results
        #numpy .shape method gives back [height, width, depth]
        # print(needle_img.shape)
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()
        # cv.imshow("test", screenshot)
        # if cv.waitKey(0) == ord('q'):
        #     cv.destroyAllWindows()
    
    def update_needle(self, needle):
        self.lock.acquire()
        self.needle_img = needle
        self.lock.release()
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]
        
    def stop(self):
        self.running = False

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while self.running:
            # print(time())
            if not self.screenshot is None:
                # do object detection
                # print(time())

                result = cv.matchTemplate(self.screenshot, self.needle_img, self.method)
                # print(result)
                # print(result.shape)
                locations = np.where(result >= self.threshold)
                locations = list(zip(*locations[::-1]))
                # print(locations)
                # if we found no results, return now. this reshape of the empty array allows us to 
                # concatenate together results without causing an error
                # if not locations:
                #     return np.array([], dtype=np.int32).reshape(0, 4)
                #grouping rectangles
                #create list of [x,y,w,h] rectangles
                rectangles = []
                for loc in locations:
                    rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
                    rectangles.append(rect)
                    rectangles.append(rect)
                rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
                # print(rectangles)
                # for performance reasons, return a limited number of results.
                # these aren't necessarily the best results.
                if len(rectangles) > self.max_results:
                    print('Warning: too many results, raise the threshold.')
                    rectangles = rectangles[:self.max_results]
                
                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()