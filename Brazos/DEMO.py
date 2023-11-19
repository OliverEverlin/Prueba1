# Proyecto de SIGA
# Grupo 3

##Desarrollado por:
## Oliver Rojas Pumaricra

## El siguiente codigo muestra la determinación de los angulos en tiempo real



import cv2
# import mediapipe as mp
import time
import PoseModule as pm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import csv

cap = cv2.VideoCapture('PoseVideos/curls.mp4')  # Poner el nombre de la carpeta del video que usarás
# cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
pTime = 0
detector = pm.poseDetector()
count = 0

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
    success, img = cap.read()

    # IF: Como filtro de valores atípicos
    if img is not None:
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        #SI se encontró un cuerpo se procesará y mostrará esa data
        if len(lmList) != 0:
            #CALCULO BRAZO--------------------------------------------------------
            # Angulo de brazo respecto al torso (puntuaciones)

            # DERECHA ---------------------------
            BRder = abs(detector.findAngle3D(img, 14, 12, 24))
            PBRder= detector.brazoPuntuation(BRder)

            # IZQUIERDA ---------------------------
            BRizq = abs(detector.findAngle3D(img, 13, 11, 23))
            PBRizq = detector.brazoPuntuation(BRizq)

            # CALCULO ANTEBRAZOS ---------------------------------------------------------------
            # DERECHA ---------------------------
            ABRder = abs(detector.findAngle3D(img, 12, 14, 16))
            PABRder = detector.anteBrazoPuntuation(BRder)

            # IZQUIERDA ---------------------------
            ABRizq = abs(detector.findAngle3D(img, 11, 13, 15))
            PABRizq = detector.anteBrazoPuntuation(BRizq)

            # CALCULO CUELLO ---------------------------------------------------------------
            #Promediacion
            head=[]
            budy=[]
            head = detector.promDot(img,7,8)
            budy = detector.promDot(img, 23, 24)
            cuello= detector.promDot(img,11,12)

            ANGcuello = (detector.findAngle3DbyVectors(img, head, cuello, budy, draw=True))
            PCuello = detector.cuelloPuntuation(ANGcuello)

            # PUNTAJE TOTAL
            TOTAL= PBRder + PBRizq + PABRder + PABRizq + PCuello
            #Todos estos valores impresos en el forms



        # Reajuste de tamaños: si la imagen sale muy grande o pequeña solo cambia el valor de la escala
        escala = 1
        width, height, _ = img.shape
        alto = int(width * escala)
        ancho = int(height * escala)
        img = cv2.resize(img, (ancho, alto))
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        count += 1

    else:
        ##En caso haya un error, se mantiene el valor anterior
        pass



