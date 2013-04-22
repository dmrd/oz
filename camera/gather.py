#Gathers training data for hand shapes

import pickle, sys
from time import time
import cv2
import numpy as np
from sklearn import svm


labels = ["pinky", "index", "middle", "ring", "thumb", "five_fingers", "none", "fist"]
framesPerLabel = 10

outputDirectory = "./" + sys.argv[1]

#Returns (size, contour, bbox) of largest contour
def getLargestContour(contours):
    sContours = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        sContours.append((w*h,contour,(x,y,w,h)))
    sContours.sort(key=lambda e: e[0])
    return sContours[-1]

def getFeatures(img):
    detector = cv2.FeatureDetector_create('SIFT')
    descriptor = cv2.DescriptorExtractor_create('SIFT')
    #grid_detector = cv2.GridAdaptedFeatureDetector(detector, 100)
    key = detector.detect(img)
    key, desc = descriptor.compute(img, key)
    #print(desc)
    return (key,desc)

#Return tuple of greyscale image and hand
def getHand(c):
    _,im = c.read()
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,75,256,1)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if (len(contours) > 0):
        large = getLargestContour(contours)
        cv2.drawContours(imgray,[large[1]],-1,(255,0,0),-1)
        cv2.drawContours(thresh,[large[1]],-1,(255,0,0),-1)

        #keys, desc = getFeatures(imgray)
        #cv2.drawKeypoints(imgray,keys)

        x,y,w,h = large[2]
        cropped = thresh[y:y+h, x:x+w]
        cv2.rectangle(imgray,(x,y),(x+w,y+h),(0,255,0),2)

        #im = cv2.resize(cropped, (512,256))
        im = cv2.resize(cropped, (256,512))
    else:
        im = cv2.resize(thresh, (256,512))

    cv2.imshow('e2',imgray)
    cv2.imshow('e1',im)
    return imgray, im

#Delay while still showing hand.
def captureDelay(seconds):
    now = time()
    while (time() - now < seconds):
        getHand(c)
        if cv2.waitKey(5) == 27:
            exit()


c = cv2.VideoCapture(0)
for second in range(9,0,-1):
    print("Beginning captures in {0} seconds...".format(second))
    captureDelay(1)
for label in labels:
    #Count down
    for second in range(3,0,-1):
        print("Reading {0} in {1} seconds...".format(label,second))
        captureDelay(1)

    #Capture
    for frame in range(framesPerLabel):
        imgray, im = getHand(c)
        cv2.imwrite(outputDirectory + "/" + label + "-" + str(frame) + ".png", im)
        print("Frame {0} captures".format(frame))
        captureDelay(0.2)

cv2.destroyAllWindows()
