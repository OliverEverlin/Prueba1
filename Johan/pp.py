import cv2
import numpy as np
import time
import PoseModule as pm

#cap = cv2.VideoCapture()

detector = pm.poseDetector()

while True:
    #success, img = cap.read()
    #img = cv2.resize(img, (1280,720))
    img = cv2.imread("Johan/image.jpg")
    img = detector.findPose(img)
    cv2.imshow("Image",img)
    cv2.waitKey(1)