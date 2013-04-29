import acquire
import pickle
import sys
from sklearn import svm

#Read in classifier
if (len(sys.argv) < 3):
    print("{0} classifierFile userFile".format(sys.argv[0]))
    exit()
else:
    classifierName = sys.argv[1]
    userFile = sys.argv[2]

loadedC = acquire.LoadFile(classifierName)
if loadedC == None:
    print("Loading classifier failed.")
    exit()
labels,ids,clf = loadedC


userData = acquire.LoadFile(userFile)
if userData == None or type(userData) is not dict:
    print("No userdata found")
    userData = {}

c = acquire.Setup()

print("Please enter username:")
name = raw_input()
if name in userData:
    print("Please enter password:")
    if (acquire.CheckPassword(clf, userData[name]["handshake"], c, ids)):
        print("You successfully entered your password")
    else:
        print("Incorrect password")
else:
    print("You still need to set a password.")
    #Testing purposes - does not claim to be secure
    print("Please enter Facebook password:")
    fb = raw_input()

    userData[name] = {"handshake" : acquire.TrainPassword(clf, c, ids), "password" : fb}

f = open(userFile, 'w')
pickle.dump(userData, f)
f.close()
