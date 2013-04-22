import cv2
import numpy as np
import pickle
from sklearn import svm
c = cv2.VideoCapture(0)
imageID = 0

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

#try:
with open('svmdata', 'r') as f:
    print("Loading saved SVM")
    labels,ids,clf = pickle.load(f)
#except:
        #print("No saved SVM found.  Please rebuild")
        #clf = None

while(1):
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
    #cv2.imshow('e2',thresh)
    k = cv2.waitKey(5)
    if k == 27:
        break
    if k == 115:
        cv2.imwrite("./images/image{0}.png".format(imageID), im)
        print("Saving image")
        imageID+= 1
    if k == 99:
        if clf == None:
            print("Must train SVM first...")
        else:
            print(ids[clf.predict(im.flatten())[0]])
            #print(idsclf.predict(im.flatten())[0])

cv2.destroyAllWindows()
