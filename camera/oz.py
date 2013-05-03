import acquire
import pickle
import sys
from sklearn import svm

#For sharing to chrome extension
import socket, sys
import SimpleHTTPServer
import SocketServer

#Shares directory - allows 1 reqest to be made
def ShareFolder():
    PORT = 1339
    url = socket.gethostbyname(socket.gethostname()) + ":" + str(PORT)
    print "Share this link: " + "http://" + url
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    httpd.handle_request()

flagFile = "status.txt"

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

print(userData)
camera = acquire.Acquire()

print("Please enter username:")
name = raw_input()
if name in userData:
    print("Please enter password:")
    if (camera.CheckPassword(clf, userData[name]["handshake"], ids)):
        print("You successfully entered your password")
        # lulz lulz lulz
        # Do not do in real life.  Please.
        # Writes to file
        f = open(flagFile, 'wt')
        f.write("{0}\n{1}\n".format(name,userData[name]["password"]))
        f.close()
        #Shares directory for chrome plugin to access
        ShareFolder()
        #Clear file
        f = open(flagFile, 'wt')
        f.close()
    else:
        print("Incorrect password")
else:
    print("You still need to set a password.")
    #Testing purposes - does not claim to be secure
    print("Please enter Facebook password:")
    fb = raw_input()
    userData[name] = {"handshake" : camera.TrainPassword(clf, ids), "password" : fb}

f = open(userFile, 'w')
pickle.dump(userData, f)
f.close()
