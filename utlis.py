import cv2
import numpy as np
writeList = []

def cannyEdge(img, cThr=[85,100]):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,cThr[0],cThr[1])
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=3)
    imgThre = cv2.erode(imgDial,kernel,iterations=2)
    return imgThre

def getContours(img,cThr=[100,100],showCanny=False,minArea=1000,filter=0,draw =True):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    writeList.append(imgGray)
    # cv2.imshow('test',imgGray)
    # if cv2.waitKey(0) == ord('w'):
    #     cv2.destroyAllWindows()
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    writeList.append(imgBlur)
    # cv2.imshow('test',imgBlur)
    # if cv2.waitKey(0) == ord('w'):
    #     cv2.destroyAllWindows()
    imgCanny = cv2.Canny(imgBlur,cThr[0],cThr[1])
    writeList.append(imgCanny)
    # cv2.imshow('test',imgCanny)
    # if cv2.waitKey(0) == ord('w'):
    #     cv2.destroyAllWindows()
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=3)
    writeList.append(imgDial)
    # cv2.imshow('test',imgDial)
    # if cv2.waitKey(0) == ord('w'):
    #     cv2.destroyAllWindows()
    imgThre = cv2.erode(imgDial,kernel,iterations=2)
    writeList.append(imgThre)
    # cv2.imshow('test',imgThre)
    # if cv2.waitKey(0) == ord('w'):
    #     cv2.destroyAllWindows()
    if showCanny:cv2.imshow('Canny',imgThre)
    contours, hierarchy= cv2.findContours(imgThre,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            print("area {}".format(area))

            #find perimeter of contour
            peri = cv2.arcLength(i,True)
            # print("peri {}".format(peri))

            #approximate array points of contour
            approx = cv2.approxPolyDP(i,0.02*peri,True)
            print("approx {}".format(approx))

            #returns rectangle values (x,y,w,h)
            bbox = cv2.boundingRect(approx)
            print("bbox {}".format(bbox))
            if filter > 0:
                if len(approx) == filter:
                    finalCountours.append([len(approx),area,approx,bbox,i])
            else:
                finalCountours.append([len(approx),area,approx,bbox,i])
    finalCountours = sorted(finalCountours,key = lambda x:x[1] ,reverse= True)
    if draw:
        for con in finalCountours:
            cv2.drawContours(img,con[4],-1,(0,0,255),3)
    return img, finalCountours

def reorder(myPoints):
    #print(myPoints.shape)
    myPointsNew = np.zeros_like(myPoints)
    myPoints = myPoints.reshape((4,2))
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1]= myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew

def warpImg (img,points,w,h,pad=20):
    # print(points)
    points =reorder(points)
    # print(points)
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(img,matrix,(w,h))
    imgWarp = imgWarp[pad:imgWarp.shape[0]-pad,pad:imgWarp.shape[1]-pad]
    
    return imgWarp

def findDis(pts1,pts2):
    return ((pts2[0]-pts1[0])**2 + (pts2[1]-pts1[1])**2)**0.5

