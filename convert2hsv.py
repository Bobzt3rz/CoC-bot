import cv2 as cv
import os
from vision import Vision
from hsvfilter import HsvFilter

vision = Vision()
hsv_filter = HsvFilter()
#apply desired hsv values
hsv_filter.set_troop_placement()

#For singular image
def single_image(img_path: str): 
    img = cv.imread(img_path, cv.IMREAD_UNCHANGED)
    out_img = vision.apply_hsv_filter(img, hsv_filter)
    img_name = img_path.split('/')[1]
    out_path = "hsv_image/" + img_name
    cv.imwrite(out_path, out_img)

# For multiple images
def multiple_image(filename: str):
    for entry in os.scandir(filename):
        path = entry.path.replace('\\', '/')
        img = cv.imread(path)
        out_img = vision.apply_hsv_filter(img, hsv_filter)
        img_name = path.split('/')[1]
        out_path = "hsv_image/" + img_name
        cv.imwrite(out_path, out_img)

single_image("images/base1.png")
# multiple_image("images")