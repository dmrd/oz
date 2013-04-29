#Helper functions for Oz project
import cv2
import numpy as np
import pickle
from time import time

#Various defaults
THRESHOLD = 210
THRESH_METHOD = 0 #1 to target darker blobs, 0 to target lighter ones
sizeBound = 30000

def Setup(cam = 1):
    """Return webcam object. Takes camera number as optional arg"""
    return cv2.VideoCapture(cam)

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


#Return tuple of image and hand
def GetHand(c, threshold = THRESHOLD):
    """Take picture with camera c and return image and isolated hand """
    _,im = c.read()
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,threshold,256,THRESH_METHOD)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    large = GetLargestContour(contours)
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
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
    else:
        #No largest, so just an empty image
        hand = cv2.resize(hand, (256,512))
    return im, hand


#Delay while still showing hand.
def CaptureDelay(seconds, c):
    """Continue video capture while delaying for # seconds.  Esc exits"""
    now = time()
    while (time() - now < seconds):
        im, hand = GetHand(c)
        cv2.imshow('camera',im)
        cv2.imshow('hand',hand)
        if cv2.waitKey(5) == 27:
            exit()


#So secure... Trust me...

def ReadPassword(clf, c = None, ids = None):
    if (c == None):
        c = Setup()
    print("Press the spacebar to record a gesture, escape to end capture.")
    
    password = []
    while 1:
        im, hand = GetHand(c)
        cv2.imshow('hand',hand)
        k = cv2.waitKey(5)
        #Escape
        if k == 27:
            break
        #Space
        if k == 32:
            fit = clf.predict(hand.flatten())[0]
            if ids != None:
                print(ids[fit])
            password.append(fit)
    return password

def TrainPassword(clf, c = None, ids = None):
    while 1:
        print("Enter your desired password...")
        p1 = ReadPassword(clf, c, ids)
        print("\nEnter password again to confirm...")
        p2 = ReadPassword(clf, c, ids)
        if (p1 == p2):
            return p1
        else:
            print("Your password confirmation differed.  Please retry.")

def CheckPassword(clf, password, c = None, ids = None):
    enteredPass = ReadPassword(clf, c, ids)
    return (enteredPass == password)
