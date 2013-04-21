#!/home/miles/cos436/py_virt_env/bin/python

import Leap, sys, time

class CustomHand:
    def __init__(self, visible):
        self.visible = visible

    def __str__(self):
        print visible

def main():
    controller = Leap.Controller()

    while True:
        frame = controller.frame()
        while frame.hands.empty or len(frame.hands[0].fingers) == 0:
            frame = controller.frame()

        hand = frame.hands[0]

        palmLoc = hand.palm_position
        palmDir = hand.direction
        palmNor = hand.palm_normal
        fingers = hand.fingers
        numFingers = len(fingers)

        print numFingers

        if len(fingers) == 5:
            customHand = CustomHand([True, True, True, True, True])
        else: 
            bases = []
            crosses = []
            totalWidth = 0
            for finger in fingers:
                totalWidth += finger.width
                fingerPos = finger.tip_position
                fingerLen = finger.length
                fingerDir = finger.direction
                fingerBase = fingerPos - fingerDir * fingerLen - palmLoc
                bases.append(fingerBase)
                resVec = fingerBase.cross(palmNor)
                crosses.append(resVec)

            avgWidth = totalWidth / numFingers

            guesses = [f.x/avgWidth for f in bases]

            sortedBases = sorted(bases, key=lambda f: f.x)
            sortedCrosses = sorted(crosses, key=lambda f: f.y)
            sortedYs = [f.y for f in sortedCrosses]
            sortedZs = [f.z for f in sortedCrosses]

            if sortedZs[0] > 0 or sortedZs[-1] > 0:
                hasThumb = True

            print sortedYs

        time.sleep(1)

if __name__ == "__main__":
    main()
