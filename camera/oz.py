import acquire
import pickle
from sklearn import svm

#Read in classifier
if (len(sys.argv) < 3):
    print("{0} classifierFile userFile".format(sys.argv[0]))
    exit()
else:
    classifierName = sys.argv[1]
    userFile = sys.argv[2]

loadedC = acquire.LoadClassifier(classifierName)
if loadedC == None:
    print("Loading classifier failed.")
    exit()
labels,ids,clf = loadedC


userData = acquire.LoadClassifier(userFile)
if userData == None or type(userData) is dict:
    print("Loading userdata failed.")
    exit()

c = acquire.Setup()

print("Please enter username:")
name = raw_input()
if name in userData:
    print("Please enter password:")
    if (acquire.CheckPassword(clf, userData[name], c, ids) == userData[name]):
        print("You successfully entered your password")
    else:
        print("Incorrect password")
else:
    print("You still need to set a password.")
    userData[name] = TrainPassword(clf, c, ids)
