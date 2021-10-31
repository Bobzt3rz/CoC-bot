import cv2 as cv
import numpy as np
import imutils
from statistics import mean

# Load image, grayscale, Gaussian blur, threshold
image = cv.imread("hsv_image/base7.png")
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
    for points in contours:
        cv.circle(image, points[0], 1, (255, 50, 0), -1)
        
    for points in approx_edge_points:
        cv.circle(image, points[0], 1, (0, 50, 255), -1)




# draw contours
thresh_BGR = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
cv.drawContours(thresh_BGR, approx_edge_cnts, -1, (255,0,0), thickness= 2)
# cv.drawContours(image, approx_edge_cnts, -1, (255,0,0), thickness= 2)

x, y, w, h = cv.boundingRect(thresh)           #  Replaced code
                                                # 
left = (x, np.argmax(thresh[:, x]))             # 
right = (x+w-1, np.argmax(thresh[:, x+w-1]))    # 
top = (np.argmax(thresh[y, :]), y)              # 
bottom = (np.argmax(thresh[y+h-1, :]), y+h-1)   # 

cv.circle(image, left, 8, (0, 50, 255), -1)
cv.circle(image, right, 8, (0, 255, 255), -1)
cv.circle(image, top, 8, (255, 50, 0), -1)
cv.circle(image, bottom, 8, (255, 255, 0), -1)

print('left: {}'.format(left))
print('right: {}'.format(right))
print('top: {}'.format(top))
print('bottom: {}'.format(bottom))
cv.imshow('erode', erode)
cv.imshow('gray', gray)
cv.imshow('thresh', thresh)
cv.imshow('thresh bgr', thresh_BGR)
cv.imshow('image', image)
cv.waitKey()