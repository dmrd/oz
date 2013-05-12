#Helper functions for Oz project
import cv2
import numpy as np
import pickle
import sys
from time import time

#Various defaults
THRESHOLD = 40
THRESH_METHOD = 1 #1 to target darker blobs, 0 to target lighter ones
CHANNEL = 1 #r, g, b = 0,1,2
sizeBound = 30000
KERNEL = (13,13)
background = None
CONSECUTIVE_FRAMES = 15
ATTEMPTS = 3

class Acquire:
    def __init__(self, cam = 0, debug = 0):
        self.c = cv2.VideoCapture(cam)
        self.background = self.GetBackground()
        self.threshold = THRESHOLD
        self.threshold_method = THRESH_METHOD
        self.sizeBound = sizeBound
        self.debug = debug

    def Setup(cam = 1):
        """Return webcam object. Takes camera number as optional arg"""
        c = cv2.VideoCapture(cam)
        return c

    def GetBackground(self):
        im = self.GetFrame()
        channels = cv2.split(im)
        try:
            background = channels[CHANNEL]
        except:
            print 'Try fuxing around with the webcam, bro.'
            return None
        #background = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        return cv2.blur(background, KERNEL)

    # Capture image
    def GetFrame(self):
        _,im = self.c.read()
        return im

    #Return tuple of image and hand
    def GetHand(self, threshold = None):
        """Take picture and return image and isolated hand """
        if threshold == None:
            threshold = self.threshold
        im = self.GetFrame()
        #imChannel = cv2.split(im)[CHANNEL]
        #imChannel = cv2.blur(imChannel, KERNEL)
        #diff = cv2.absdiff(imChannel,self.background)
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray, threshold, 256, self.threshold_method)

        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        large = GetLargestContour(contours)
        hand = np.zeros((len(im),len(im[0])), np.uint8) #Black image
        if (large != None):
            #Draw largest contour by itself and over image
            cv2.drawContours(im,[large[1]],-1,(255,0,0),-1)
            cv2.drawContours(hand,[large[1]],-1,(255,0,0),-1)

            #Crop hand only image down and resize
            x,y,w,h = large[2]
            hand = hand[y:y+h, x:x+w]
            hand = cv2.resize(hand, (256,512))

            #Draw rectangle around region on feed
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
        else:
            #No largest, so just an empty image
            hand = cv2.resize(hand, (256,512))

        if (self.debug):
            cv2.imshow('imgray', imgray)
            cv2.imshow('im', im)
            cv2.imshow('hand', hand)
        return im, hand

    # Read in current gesture - must hold for # consec frames
    def GetGesture(self, clf, lastGesture, consec = CONSECUTIVE_FRAMES):
        repeated = 0 # Number of times it has been repeated
        last = -1  # Gesture read in last frame
        while (repeated < consec):
            im, hand = self.GetHand()
            if (self.debug):
                cv2.imshow('hand',hand)

            #Predict hand shape
            fit = clf.predict(hand.flatten())[0]

            #How long have they held the current shape?
            if fit == last:
                repeated += 1
            else:
                repeated = 0
                last = fit
        return last

    #Delay while still showing hand.
    def CaptureDelay(self, seconds):
        """Continue video capture while delaying for # seconds.  Esc exits"""
        now = time()
        while (time() - now < seconds):
            im, hand = self.GetHand()
            #cv2.imshow('camera',im)
            #cv2.imshow('hand',hand)
            if cv2.waitKey(5) == 27:
                exit()

#Returns (size, contour, bbox) of largest contour
def GetLargestContour(contours):
    """Return (size,contour,bbox) of contour with largest bbox"""
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

def FinishCapture():
    cv2.destroyAllWindows()

def LoadFile(filename):
    """Load the pickled file from filename
    
        Return None if load fails
    """
    try:
        f = open(filename, 'r')
        loaded = pickle.load(f)
        f.close()
        return loaded
    except:
        return None 

