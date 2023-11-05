import cv2
import numpy as np
import time
import PoseModule as pm

cap= cv2.VideoCapture("AITrainer/barra.mp4")
img = cv2.imread("AITrainer/curls1.jpg")
while True:
    # success, img= cap.read()
    # img = cv2.resize(img,(1288,728))
    
    cv2.imshow("Image",img)
    cv2.waitKey(1)