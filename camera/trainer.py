import cv2
from sklearn import svm
import os, pickle

directory = "./train"

images = []
labels = []

labelIDs = {}
idLabels = {}

def getLabel(name):
    if name in labelIDs:
        return labelIDs[name]
    else:
        labelIDs[name] = len(labelIDs)
        idLabels[len(labelIDs)-1] = name
        return labelIDs[name]

#Read in training data
for name in os.listdir(directory):
    path = directory + "/" + name
    #Load image
    img = cv2.imread(path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    #Convert entirely to b&w
    img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    images.append(img.flatten())
    label = name.split("-")[0]
    print(name + " : " + label)
    labels.append(getLabel(label))
    #print(img)
    #cv2.imshow('img', img)
    #if cv2.waitKey(-1) == 27:
        #break
#cv2.destroyAllWindows()


#Train
clf = svm.LinearSVC()
print("Training SVM...")
clf.fit(images, labels)
print("Training complete")
trained = (labelIDs, idLabels, clf)

#Save data
f = open('svmdata', 'w')
pickle.dump(trained, f)
