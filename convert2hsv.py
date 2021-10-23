import cv2 as cv
from vision import Vision
from hsvfilter import HsvFilter

pic_name = "testbase.jpg"

vision = Vision()
hsv_filter = HsvFilter(16, 136, 0, 28, 149, 255, 184, 116, 137, 20)

img_path = "source_image/" + pic_name
img = cv.imread(img_path, cv.IMREAD_UNCHANGED)

out_img = vision.apply_hsv_filter(img, hsv_filter)
out_path = "hsv_image/" + pic_name
cv.imwrite(out_path, out_img)