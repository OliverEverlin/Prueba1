import cv2
#import mediapipe as mp
import time
import PoseModule as pm
import numpy as np

cap = cv2.VideoCapture('PoseVideos/barra.mp4')
#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
pTime = 0
detector= pm.poseDetector()
count = 0
dir = 0 #1 para cuando sube, 0 para cuando baja

while True:
    #img = cv2.imread("PoseVideos/curls1.jpg")
    success, img = cap.read()
    img = detector.findPose(img,False)
    #success, img = cap.read()
    #img = detector.findPose(img)
    lmList = detector.findPosition(img,False)
    if len(lmList)!=0:
        #Derecha
        #angD = detector.findAngle(img,12,14,16)
        #Izquierda
        angI = detector.findAngle(img, 11, 13, 15)

        per = np.interp(angI,(30,160),(100,0))
        bar = np.interp(angI,(30,160),(100,650)) #el minimo y el maximo son diferentes para open cv
        #print(int(angI),per)


        # check numero de veces
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                #el siguiente de dir es para evitar que se sume innecesariamente
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)
        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)


    cTime= time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN,
                5, (255, 0, 0), 5)


    # Reajuste de tamaños
    escala = 0.8
    width, height, _ = img.shape
    alto = int(width * escala)
    ancho = int(height * escala)
    img = cv2.resize(img, (ancho, alto))

    cv2.imshow("Image", img)
    cv2.waitKey(1)