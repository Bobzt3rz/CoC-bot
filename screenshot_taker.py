from windowcapture import WindowCapture
from time import time
import cv2 as cv

wincap = WindowCapture("SM-G975F")
wincap.start()
#change count num
count = 6

while True:
    if wincap.screenshot is None:
        continue
    cv.imshow('out', wincap.screenshot)

    if cv.waitKey(1) == ord('s'):
        count += 1
        out_path = "images/pic" + str(count) + ".png"
        cv.imwrite(out_path, wincap.screenshot)
        print("Image saved")

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        wincap.stop()
        break
