import pickle
import hashlib
import sys
import os
import string
from Crypto.Cipher import AES

# Our modules
sys.path.append("../util")
import texting
import acquire

from os.path import dirname

#Helper modules
from sklearn import svm
#For sharing to chrome extension
import slurpy

# Save the user data back to disk
def SaveUserData(userData):
    with open(userFile, 'w') as f:
        pickle.dump(userData, f)

# Signals chrome extension to log in
flagFile = "status.txt"

# Read in classifier
if (len(sys.argv) < 3):
    classifierName = "svmdata"
    userFile = "userdata"
    #print("{0} classifierFile userFile".format(sys.argv[0]))
    #exit()
else:
    classifierName = sys.argv[1]
    userFile = sys.argv[2]

loadedC = acquire.LoadFile(classifierName)
if loadedC == None:
    print("Loading classifier failed.")
    exit()
labels,ids,clf = loadedC
print(loadedC)


userData = acquire.LoadFile(userFile)
if userData == None or type(userData) is not dict:
    print("No userdata found")
    userData = {}

#print(userData)
if (len(sys.argv) > 3):
    camera = acquire.Acquire(debug = 1)
else:
    camera = acquire.Acquire()

# Number of times to indent output
# A list is used to force access by reference
__report_indent = [0]

def report(fn):
    """Decorator to print information about a function
    call for use while debugging.
    Prints function name, arguments, and call number
    when the function is called. Prints this information
    again along with the return value when the function
    returns.
    """

    def wrap(*params,**kwargs):
        call = wrap.callcount = wrap.callcount + 1

        indent = ' ' * __report_indent[0]
        fc = "%s(%s)" % (fn.__name__, ', '.join(
            [a.__repr__() for a in params] +
            ["%s = %s" % (a, repr(b)) for a,b in kwargs.items()]
        ))

        print("%s%s called [#%s]" % (indent, fc, call))
        __report_indent[0] += 1
        ret = fn(*params,**kwargs)
        __report_indent[0] -= 1
        print("%s%s returned %s [#%s]" % (indent, fc, repr(ret), call))
        return ret
    wrap.callcount = 0
    return wrap

# Read in gesture - default to not allowing empty gesture
#@report
def getGesture(last = labels['none']):
    return 0
    #return camera.GetGesture(clf, last)

#@report
def decodePassword(user, handshake):
    return "chem4life"
    #...fluidity over security?
    key = ' '.join([str(x) for x in handshake])
    # Pad key and password
    if (len(key) % 16 != 0):
        key += ' ' * (16 - len(key) % 16)
    cipher = AES.new(key)
    if user in userData:
        password = cipher.decrypt(userData[user])
        password = string.rstrip(password, '0')
        return password[:-1]
    else:
        return None

#@report
def addUser(user, password, handshake):
    print("TEST")
    key = ' '.join([str(x) for x in handshake])
    # Pad key and password
    if (len(key) % 16 != 0):
        key += ' ' * (16 - len(key) % 16)
    cipher = AES.new(key)
    password += '1'
    if (len(password) % 16 != 0):
        password += '0' * (16 - len(password) % 16)
    print(password)
    userData[user] = cipher.encrypt(password)
    SaveUserData(userData)
    return True

# Create server for plugin to call functions
server = slurpy.Slurpy()

# Register publicly accessible functions on server
server.register(getGesture)
server.register(decodePassword)
server.register(addUser)
server.register(os)
server.register(dirname)

#server.methods
server.start()
