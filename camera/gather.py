#Gathers training data for hand shapes

import pickle, sys
from time import time
import cv2
import numpy as np
from sklearn import svm


labels = ["pinky", "index", "middle", "ring", "thumb", "five_fingers", "none", "fist", "peace", "rockOn", "bullhorns", "spock", "inverted_spock", "index_middle_ring", "cross_middle_index", "trigger"]
framesPerLabel = 30

outputDirectory = "./" + sys.argv[1]

sizeBound = 30000 #Smallest bounding box accepted

threshold = 65

#Returns (size, contour, bbox) of largest contour
def getLargestContour(contours):
    sContours = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if (w*h < sizeBound):
            continue
        sContours.append((w*h,contour,(x,y,w,h)))
    sContours.sort(key=lambda e: e[0])
    if (len(sContours) > 0):
        return sContours[-1]
    else:
        return None

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
    ret,thresh = cv2.threshold(imgray,threshold,256,1)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    large = getLargestContour(contours)
    hand = np.zeros((len(thresh),len(thresh[0])), np.uint8) #Black image
    if (large != None):
        #Draw largest contour by itself and over image
        cv2.drawContours(imgray,[large[1]],-1,(255,0,0),-1)
        cv2.drawContours(hand,[large[1]],-1,(255,0,0),-1)


        #Crop hand only image down and resize
        x,y,w,h = large[2]
        hand = hand[y:y+h, x:x+w]
        hand = cv2.resize(hand, (256,512))

        #Draw rectangle around region on feed
        cv2.rectangle(imgray,(x,y),(x+w,y+h),(0,255,0),2)
    else:
        #No largest, so just an empty image
        hand = cv2.resize(hand, (256,512))

    cv2.imshow('e2',imgray)
    cv2.imshow('e1',hand)
    return imgray, hand

#Delay while still showing hand.
def captureDelay(seconds):
    now = time()
    while (time() - now < seconds):
        getHand(c)
        if cv2.waitKey(5) == 27:
            exit()


c = cv2.VideoCapture(1)
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
