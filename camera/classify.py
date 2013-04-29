#Hand classifier
#Author: David Dohan

import cv2
import sys
import numpy as np
import pickle
import acquire
from sklearn import svm

imageID = 0 #Save images as image{id}.png

#Font stuff
font = cv2.FONT_HERSHEY_PLAIN
text_color = (255,255,255)

#Read in classifier
if (len(sys.argv) > 1):
    classifierName = sys.argv[1]
else:
    classifierName = "svmdata"

loaded = acquire.LoadFile(classifierName)
if loaded == None:
    print("Loading classifier failed.")
    exit()
labels,ids,clf = loaded


#Get camera
c = acquire.Setup()

while(1):
    im, hand = acquire.GetHand(c)

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


acquire.FinishCapture()
