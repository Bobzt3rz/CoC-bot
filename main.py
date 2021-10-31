import cv2 as cv
import numpy as np
import pyautogui
import threading
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
from detection import Detection

DEBUG = True
# make a threadlock
threadLock = threading.Lock()
# list window names
WindowCapture.list_window_names()
# initialize the WindowCapture class
wincap = WindowCapture("SM-G975F")
# initialize detection class for elixir collector
detector = Detection('hsv_image/Elixir_Collector13.png', cv.TM_CCOEFF_NORMED, threshold = 0.5, max_results = 10)
# initialize an empty Vision class
vision = Vision()
# initialize bot


#initialize trackbar window
vision.init_control_gui()

#elxirlvl13 hsv filter
hsv_filter = HsvFilter(16, 136, 0, 28, 149, 255, 184, 116, 137, 20)

#global variable to detect if bot action is running
is_bot_in_action = False

#run function inside another thread
def bot_actions(rectangles):
    if len(rectangles) > 0:
        targets = vision.get_rect_centers(rectangles)
        target = wincap.get_screen_position(targets[0])
        pyautogui.moveTo(x = target[0], y=target[1])
        sleep(3)
        pyautogui.click()
        sleep(3)
    global is_bot_in_action
    is_bot_in_action = False


wincap.start()
detector.start()

loop_time = time()
# This loop is to resize the needle image before going into main loop
while(True):
    # if we don't have a screenshot yet, loop infinitely
    if wincap.screenshot is None:
        continue
    else:
        # pre-process the image
        processed_image = vision.apply_hsv_filter(wincap.screenshot, hsv_filter)
        # pre-process the needle image
        needle = cv.imread("hsv_image/Elixir_Collector13.png", cv.IMREAD_UNCHANGED)
        processed_needle = vision.apply_hsv_filter(needle, hsv_filter)
        scaled_needle = vision.resize_needle(processed_needle, processed_image)
        detector.update_needle(scaled_needle)
        break    

while(True):

    # pre-process the image
    processed_image = vision.apply_hsv_filter(wincap.screenshot)

    # cv.imshow('Computer Vision', screenshot)

    #do object detection
    detector.update_screenshot(processed_image)

    
    if DEBUG:
        #rectange output image
        output_image = vision.draw_rectangles(wincap.screenshot, detector.rectangles)

        #display output_image
        cv.imshow('Processed', processed_image)
        cv.imshow('Matches', output_image)

    #take bot actions
    # if not is_bot_in_action:
    #     is_bot_in_action = True
    #     t = threading.Thread(target=bot_actions, args=(detector.rectangles,))
    #     t.start()

    #print FPS of 1 loop of code
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()


    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        detector.stop()
        wincap.stop()
        break
    

print('Done')
