import acquire
import pickle
import sys
sys.path.append("../util")
import texting
from sklearn import svm

#For sharing to chrome extension
import socket, sys
import SimpleHTTPServer
import SocketServer

# Shares directory - allows 1 reqest to be made
def ShareFolder():
    PORT = 1339
    url = socket.gethostbyname(socket.gethostname()) + ":" + str(PORT)
    print "Share this link: " + "http://" + url
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    httpd.handle_request()

def Login(name, userData):
    print("Logging you into Facebook...")
    # lulz lulz lulz
    # Do not do in real life.  Please.
    # Writes to file
    f = open(flagFile, 'wt')
    f.write("{0}\n{1}\n".format(name,userData[name]["password"]))
    f.close()

    #Shares directory for chrome plugin to access one time
    ShareFolder()

    #Clear file
    f = open(flagFile, 'wt')
    f.close()

# Signals chrome extension to log in
flagFile = "status.txt"

# Read in classifier
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
    if (camera.CheckPassword(clf, userData[name]["handshake"], ids)):
        print("You successfully entered your password")
        Login(name, userData)
        exit()
    else:
        print("You entered an incorrect password multiple times")
        resp = raw_input("Would you like to reset your password [y/n]?")
        
        if resp.lower() is "y" or resp.lower() is "yes":
            print("Sending verification code to registered phone number...")
            send_text("random")
            resp = raw_input("Please enter the verification code:")
            
            if resp is "31415":
                print("Verification code is correct!")
                print("Beginning password reset procedure.")

                password = camera.TrainPassword(clf, ids)
                if (len(password) == 0):
                    print("You did not enter a password.  Exiting")
                else:
                    userData[name] = {"handshake" : password, "password" : fb}
                    print("Successfully trained your password.  Logging you into Facebook now.")
                    Login(name, userData)

        else:
            print("Exiting...")
else:
    print("You still need to set a password.")
    #Testing purposes - does not claim to be secure
    print("Please enter Facebook password:")
    fb = raw_input()
    password = camera.TrainPassword(clf, ids)
    if (len(password) == 0):
        print("You did not enter a password.  Exiting")
    else:
        userData[name] = {"handshake" : password, "password" : fb}
        print("Successfully trained your password.  Logging you into Facebook now.")
        Login(name, userData)

# Save the user data back to disk
f = open(userFile, 'w')
pickle.dump(userData, f)
f.close()
