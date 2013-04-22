#!/home/miles/cos436/py_virt_env/bin/python

import Leap, time, pickle, sys
from sklearn import svm

fingerNames = ['thumb', 'pointer', 'middle finger', 'ring finger', 'pinky']

class CustomHand:
    def __init__(self, **kwargs):
        self.names = []

    def addFinger(self, *kwargs):
        for f in kwargs:
            self.names.append(f)
    
    def hasFinger(self, *args):
        for finger in args:
            try:
                self.names.index(args)
            except ValueError:
                return False
        return True

    def __str__(self):
        name = ""
        for f in self.names:
            name += f + " "
        return name

def getFingerBase(hand, fingerIndex=0):
    palmPos = hand.palm_position
    palmDir = hand.direction
    finger = hand.fingers[fingerIndex]
    fingerDir = finger.direction
    fingerLen = finger.length
    fingerPos = finger.tip_position

    fingerBase = fingerPos - fingerDir * fingerLen - palmPos
    fingerBase = fingerBase.cross(palmDir)
    print fingerBase
    return fingerBase

def trainSVM(controller):
    clf = svm.LinearSVC()
    fingerSet = []
    labelSet = []

    for j, name in enumerate(fingerNames):
        print "Training " + name + " as " + str(j) + " in 2"
        time.sleep(1)
        print "Training " + name + " as " + str(j) + " in 1"
        time.sleep(1)
        print "Training " + name + " now!"

        for i in range(300):
            frame = controller.frame()
            while frame.hands.empty or len(frame.hands[0].fingers) != 1:
                print "Please use one finger with the " + name
                time.sleep(0.2)
                frame = controller.frame()

            # Get the hand data
            fingerBase = getFingerBase(frame.hands[0])
            fingerSet.append(fingerBase.to_float_array())
            labelSet.append(j)
            time.sleep(0.01)
        print "Ok, you're done training the " + name + " now."
        time.sleep(1)

    clf.fit(fingerSet, labelSet)
    return clf

def predictNextFinger(clf, controller):
    frame = controller.frame()
    while frame.hands.empty or len(frame.hands[0].fingers) == 0:
        print "Please use one hand"
        time.sleep(1)
        frame = controller.frame()

    # Get the hand data
    hand = frame.hands[0]
    tempfingers = hand.fingers
    hand.fingers = sorted(tempfingers, key=lambda f: f.tip_position.y)

    print "Predicted fingers:",
    customhand = CustomHand()

    for i in range(len(hand.fingers)):
        fingerBase = getFingerBase(hand, i)
        prediction = clf.predict(fingerBase.to_float_array())[0]
        
        if prediction == 0:
            customhand.addFinger('thumb')
        if prediction == 1:
            customhand.addFinger('pointer')
        if prediction == 2:
            customhand.addFinger('middle')
        if prediction == 3:
            customhand.addFinger('ring')
        if prediction == 4:
            customhand.addFinger('pinky')

    return customhand

def main():
    controller = Leap.Controller()
    #if not controller.is_connected:
        #print "Need to have Leap connected."
        #return

    if len(sys.argv) > 1 and sys.argv[1] == "--rebuild-svm":
        print "About to train the SVM..."
        clf = trainSVM(controller)
        f = open('.svmdata', 'w')
        pickle.dump(clf, f)
    else:
        try:
            with open('.svmdata', 'r') as f:
                print "Found saved SVM"
                clf = pickle.load(f)
        except IOError:
            print "Couldn't find SVM, rebuilding..."
            clf = trainSVM(controller)
            f = open('.svmdata', 'w')
            pickle.dump(clf, f)

    print "Now will predict your fingers:"

    while True:
        print predictNextFinger(clf, controller)
        time.sleep(1)

if __name__ == "__main__":
    main()
