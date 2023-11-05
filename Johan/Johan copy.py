import cv2 as cv
import cv2
from matplotlib import pyplot as plt
import numpy as np
import argparse


img =  cv.imread("Johan/image.jpg")
plt.imshow(img)


# Sorry for being late in replying, please follow the video, when we are performing predictions 
# and drawing points and joining them , so actually it contains coordinates that is how it is drawing 
# the points and line on image, but all cordinates are based on image size,you have to subtract or 
# check total image size accrodingly. I hope I have answered your question, please print the values you 
# will get like x,y,w,h we are alreay using in video, please follow the instructions. Stay blessed