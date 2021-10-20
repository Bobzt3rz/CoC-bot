import cv2 as cv
import numpy as np
import pyautogui
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
from threading import Thread


WindowCapture.list_window_names()

wincap = WindowCapture("SM-G975F")
visionElixirlvl13 = Vision('elixirlvl13hsv.jpg')

#initialize trackbar window
visionElixirlvl13.init_control_gui()

#elxirlvl13 hsv filter
hsv_filter = HsvFilter(16, 136, 0, 28, 149, 255, 184, 116, 137, 20)

#global variable to detect if bot action is running
is_bot_in_action = False

#run function inside another thread
def bot_actions(rectangles):
    if len(rectangles) > 0:
        targets = visionElixirlvl13.get_click_points(rectangles)
        target = wincap.get_screen_position(targets[0])
        pyautogui.moveTo(x = target[0], y=target[1])
        pyautogui.click()
        sleep(5)
    global is_bot_in_action
    is_bot_in_action = False


loop_time = time()
while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # pre-process the image
    processed_image = visionElixirlvl13.apply_hsv_filter(screenshot, hsv_filter)

    # cv.imshow('Computer Vision', screenshot)

    #do object detection
    rectangles = visionElixirlvl13.find(processed_image, 0.5)

    #rectange output image
    output_image = visionElixirlvl13.draw_rectangles(screenshot, rectangles)

    #display output_image
    cv.imshow('Processed', processed_image)
    cv.imshow('Matches', output_image)

    #take bot actions
    if not is_bot_in_action:
        is_bot_in_action = True
        t = Thread(target=bot_actions, args=(rectangles,))
        t.start()


    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')
