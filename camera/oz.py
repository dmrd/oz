import pickle
import sys
import string
from Crypto.Cipher import AES

# Our modules
sys.path.append("../util")
import texting
import acquire


#For sharing to chrome extension
import slurpy


# Save the user data back to disk
def SaveUserData(userData):
    with open(userFile, 'w') as f:
        pickle.dump(userData, f)

# Read in classifier and user data
if (len(sys.argv) < 3):
    classifierName = "svmdata"
    userFile = "userdata"
else:
    classifierName = sys.argv[1]
    userFile = sys.argv[2]

loadedC = acquire.LoadFile(classifierName)
if loadedC is None:
    print("Loading classifier failed.")
    exit()
labels, ids, clf = loadedC
print(loadedC)


userData = acquire.LoadFile(userFile)
if userData is None or type(userData) is not dict:
    print("No userdata found")
    userData = {}

print(userData)
if (len(sys.argv) > 3):
    camera = acquire.Acquire(debug=1)
else:
    camera = acquire.Acquire()


# Read in gesture - default to not allowing empty gesture
#@report
def getGesture(last=labels['none']):
    if last in labels:
        last = labels[last]
    if (last < 0):
        last = labels['none']
    print(last)
    gesture = ids[camera.GetGesture(clf, last)]
    return gesture


#@report
def decodePassword(user, handshake):
    #return "chem4life"  # Temporarily hardcoded for testing purposes
    #...fluidity over security?
    key = ' '.join([str(x) for x in handshake])
    # Pad key and password
    if (len(key) % 16 != 0):
        key += '-' * (16 - len(key) % 16)
    print(key)
    cipher = AES.new(key)
    if user in userData:
        password = cipher.decrypt(userData[user]['password'])
        password = string.rstrip(password, '0')
        return password[:-1]
    else:
        return None


#@report
def addUser(email, fullname, password, handshake):
    print("Adding user")
    print("User: " + email)
    print("Fullname: " + fullname)
    #print("Password: " + str(password))
    print("Handshake: " + str(handshake))
    key = ' '.join([str(x) for x in handshake])
    # Pad key and password
    if (len(key) % 16 != 0):
        key += '-' * (16 - len(key) % 16)
    print(key)
    cipher = AES.new(key)
    password += '1'
    if (len(password) % 16 != 0):
        password += '0' * (16 - len(password) % 16)
    #print("Pass: " + password)
    userData[email] = {'fullname': fullname,
                       'password': cipher.encrypt(password)}
    SaveUserData(userData)
    return True


# Return list of (username, fullname) tuples
def listUsers():
    tuples = [[key, userData[key]['fullname']] for key in userData.keys()]
    print(tuples)
    return tuples


def sendText(code):
    texting.send_text(code)

# Create server for plugin to call functions
server = slurpy.Slurpy()

# Register publicly accessible functions on server
server.register(getGesture)
server.register(decodePassword)
server.register(addUser)
server.register(listUsers)
server.register(sendText)

print(server.methods)
server.start()
