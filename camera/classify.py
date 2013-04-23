#Hand classifier
#Author: David Dohan

import cv2
import numpy as np
import pickle
from sklearn import svm
imageID = 0 #Save images as image{id}.png

#Font stuff
font = cv2.FONT_HERSHEY_PLAIN
text_color = (255,255,255)

threshold = 65
THRESH_METHOD = 1 #1 to target darker blobs, 0 to target lighter ones
sizeBound = 30000 #Smallest bounding box accepted

#Returns (size, contour, bbox) of largest contour
def getLargestContour(contours):
    sContours = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if (w*h < sizeBound):
            continue
        #print(w*h)
        sContours.append((w*h,contour,(x,y,w,h)))
    sContours.sort(key=lambda e: e[0])
    if (len(sContours) > 0):
        return sContours[-1]
    else:
        return None

with open('svmdata', 'r') as f:
    print("Loading saved SVM")
    labels,ids,clf = pickle.load(f)

c = cv2.VideoCapture(1)

while(1):
    _,im = c.read()
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,threshold,256,THRESH_METHOD)
    #thresh = cv2.adaptiveThreshold(imgray, 256, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    large = getLargestContour(contours)
    hand = np.zeros((len(thresh),len(thresh[0])), np.uint8) #Black image
    if (large != None):
        #Draw largest contour by itself and over image
        cv2.drawContours(im,[large[1]],-1,(255,0,0),-1)
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

    if (clf != None):
        handClass = ids[clf.predict(hand.flatten())[0]]
        #print(handClass)
        cv2.putText(im, handClass, (30,440), font, 4.0, text_color,thickness=5)

    cv2.imshow('e2',im)
    cv2.imshow('e1',hand)
    k = cv2.waitKey(5)
    #print(k)
    if k == 27:
        break
    if k == 115:
        cv2.imwrite("./images/image{0}.png".format(imageID), hand)
        print("Saving image")
        imageID+= 1
    if k == 65362:
        threshold = min(255, threshold + 5)
        print("Threshold: {0}".format(threshold))
    if k == 65364:
        threshold = max(0, threshold - 5)
        print("Threshold: {0}".format(threshold))

    #if k == 99:
        #if clf == None:
            #print("Must train SVM first...")
        #else:
            #print(ids[clf.predict(hand.flatten())[0]])

cv2.destroyAllWindows()
