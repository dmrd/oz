#!/home/miles/cos436/py_virt_env/bin/python

import Leap, time

def getFingerBase(hand, finger):
    palmPos = hand.palm_position
    palmDir = hand.direction
    fingerDir = finger.direction
    fingerLen = finger.length
    fingerPos = finger.tip_position

    fingerBase = fingerPos - fingerDir * fingerLen - palmPos
    fingerBase = fingerBase.cross(palmDir)
    return fingerBase

def main():
    controller = Leap.Controller()
    
    while True:
        time.sleep(0.1)
        frame = controller.frame()
        if frame.hands.empty:
            continue
        hand = frame.hands[0]
        if hand.fingers.empty:
            continue
        
        for finger in hand.fingers:
            print getFingerBase(hand, finger)

if __name__ == "__main__":
    main()
