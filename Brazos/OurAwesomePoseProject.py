import cv2
#import mediapipe as mp
import time
import PoseModule as pm

#cap = cv2.VideoCapture('PoseVideos/sporttik.mp4')
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
pTime = 0
detector= pm.poseDetector()

while True:
    #Comentario apra actualizar
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:
        print(lmList[14])
        cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

    # Configuro el tiempo
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Configuraciones para mostrar la imagen
    cv2.putText(img, str(int(fps)), (70, 100), cv2.FONT_HERSHEY_PLAIN, 8, (0, 255, 0), 10)

    escala=1
    ANCHO = int(img.shape[1] * escala)
    ALTO = int(img.shape[0] * ANCHO/img.shape[1])
    img = cv2.resize(img, (ANCHO, ALTO))
    cv2.imshow("Image", img)
    cv2.waitKey(1)

#cv2.detroyAllWindows()
