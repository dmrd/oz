#Gathers training data for hand shapes

import pickle
import sys
import cv2
import numpy as np
from sklearn import svm
import acquire

#labels = ["pinky", "index", "middle", "ring", "thumb", "five_fingers", "none", "fist", "peace", "rockOn", "bullhorns", "spock", "inverted_spock", "index_middle_ring", "cross_middle_index", "trigger"]
labels = ["pinky", "index", "middle", "ring", "thumb", "five_fingers", "none", "fist", "peace"]
framesPerLabel = 50

outputDirectory = "./" + sys.argv[1]

camera = acquire.Acquire()

for second in range(9,0,-1):
    print("Beginning captures in {0} seconds...".format(second))
    camera.CaptureDelay(1)
for label in labels:
    #Count down
    for second in range(3,0,-1):
        print("Reading {0} in {1} seconds...".format(label,second))
        camera.CaptureDelay(1)

    #Capture
    for frame in range(framesPerLabel):
        im, hand = camera.GetHand()
        cv2.imwrite(outputDirectory + "/" + label + "-" + str(frame) + ".png", hand)
        print("Frame {0} captures".format(frame))
        camera.CaptureDelay(0.2)

acquire.FinishCapture()
