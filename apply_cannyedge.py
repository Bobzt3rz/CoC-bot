import cv2 as cv
import utlis
import os

imgs = []
try:
    for entry in os.scandir("images"):
        path = entry.path.replace('\\', '/')
        img = cv.imread(path)
        cannyimg = utlis.cannyEdge(img)
        cv.imshow("out",cannyimg)
        cv.imshow("original", img)
        cv.waitKey(0)
        imgs.append(cannyimg)
except KeyboardInterrupt:
    cv.destroyAllWindows()


    
