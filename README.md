oz
==

*Oz* is a system for gesture-based authentication using a webcam.

The `camera` directory contains files for the acquisition of images from the 
webcam, processing those images, and the machine-learning algorithm files.

The `extension` directory contains files for the *Oz* Chrome extension.

The `util` directory contains scripts that allow *Oz* to text a user for the
password-reset functionality.


To use *Oz*, run `camera/oz.py` in the background and load the extension as
a Chrome plugin.  It is also necessary to first train the gesture classifier
using gather/trainer.py.  The Chrome plugin makes calls to a running instance of
`oz.py` to get current hand gestures.

The system relies on slurpy (a library to allow javascript-python communication),
scikit-learn for classification, and opencv for isolating the hand image.

Created for COS436 - Human Computer Interaction
