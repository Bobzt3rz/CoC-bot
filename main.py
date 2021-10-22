import cv2 as cv
import numpy as np
import pyautogui
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
from threading import Thread
from detection import Detection

DEBUG = True

#list window names
WindowCapture.list_window_names()
# initialize the WindowCapture class
wincap = WindowCapture("SM-G975F")
# load the detector
detector = Detection('elixirlvl13hsv.jpg', cv.TM_CCOEFF_NORMED, threshold = 0.4, max_results = 10)
# load an empty Vision class
vision = Vision()

#initialize trackbar window
vision.init_control_gui()

#elxirlvl13 hsv filter
hsv_filter = HsvFilter(16, 136, 0, 28, 149, 255, 184, 116, 137, 20)

#global variable to detect if bot action is running
is_bot_in_action = False

#run function inside another thread
def bot_actions(rectangles):
    if len(rectangles) > 0:
        targets = vision.get_click_points(rectangles)
        target = wincap.get_screen_position(targets[0])
        pyautogui.moveTo(x = target[0], y=target[1])
        pyautogui.click()
        sleep(5)
    global is_bot_in_action
    is_bot_in_action = False

wincap.start()
detector.start()
loop_time = time()
while(True):
    # if we don't have a screenshot yet, don't run the code below
    if wincap.screenshot is None:
        continue

    # pre-process the image
    processed_image = vision.apply_hsv_filter(wincap.screenshot, hsv_filter)

    # cv.imshow('Computer Vision', screenshot)

    #do object detection
    detector.update(processed_image)

    
    if DEBUG:
        #rectange output image
        output_image = vision.draw_rectangles(wincap.screenshot, detector.rectangles)

        #display output_image
        cv.imshow('Processed', processed_image)
        cv.imshow('Matches', output_image)

    #take bot actions
    # if not is_bot_in_action:
    #     is_bot_in_action = True
    #     t = Thread(target=bot_actions, args=(detector.rectangles,))
    #     t.start()


    # print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()
    print(detector.stopped)


    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        detector.stop()
        wincap.stop()
        break
    

print('Done')
