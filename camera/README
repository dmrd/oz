An implementation based entirely on a camera.  No Leap necessary.  Relies on OpenCV and scikit-learn.

##Gather
###Usage:
```gather.py outputdir```:
Walks through gathering training images for several handmotions from the webcam (labels defined in the source).  Saves labelled images to outputdir.

```train.py traindir```:
Reads labelled images from traindir and trains an SVM.  Saves SVM to svmdata file that is used by classify.py

```classify.py traindir```:
Read in images from webcam and display a classification.  Loads trained classifier from svmdata.

Per computer tweaking probably necessary.
