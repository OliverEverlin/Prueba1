import cv2
#import mediapipe as mp
import time
import PoseModule as pm
import numpy as np
import pandas as pd
import csv

cap = cv2.VideoCapture('Johan/curls.mp4')
#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
pTime = 0
detector= pm.poseDetector()
count = 0
dir = 0 #1 para cuando sube, 0 para cuando baja
pandasl = []
filas = []
angulos = []
punto_angulos = []
# Determinare el grupo A
## Puntuación del brazo
estiramiento=[]
punto_estiramiento = []
antebrazoD = []
punto_antebrazoD = []
antebrazoI = []
punto_antebrazoI = []
while True:
    #img = cv2.imread("PoseVideos/curls1.jpg")
    success, img = cap.read()
    if img is not None:
        img = detector.findPose(img,False)
        #success, img = cap.read()
        #img = detector.findPose(img)
        lmList = detector.findPosition(img,False)
        if len(lmList)!=0:

            #Angulo de brazo respecto al torso (puntuaciones)
            angBDT=detector.findAngle(img, 14, 12, 24)

            pBDT = 0  # Puntuacion del brazo
            if(angBDT<20):
                pBDT=1
            elif(angBDT<45):
                pBDT=2
            elif (angBDT < 90):
                pBDT = 3
            else:
                pBDT = 4
            
            pp = 0
            #+1 Hombro elevado,
            LargeD= detector.findDistance(img, 12,24)
            LargeBrazo = detector.findDistance(img,12,14)
            print(LargeD)
            if LargeD > LargeBrazo*1.05:
                pp = pp + 1
            # +1 brazo rotado
            vector_cuerpo = detector.findVector(img, 12, 11)
            vector_plano_mano = np.cross(detector.findVector(img, 16, 20),detector.findVector(img, 18, 16))
            dif = abs(vector_cuerpo[2] - vector_plano_mano[2])
            if dif > 50:
                pp = pp + 1
            # +1 brazos abducidos
            d = detector.finddistance(img,24,12,14)
            if d > 300:
                pp = pp + 1
            # - 1 apoyo en el punto


            #Angulo de antebrazos (puntuaciones)
            #Derecha
            angD = detector.findAngle(img,12,14,16)
            #Izquierda
            angI = detector.findAngle(img, 11, 13, 15)
            if angD>60 and angD<100:
                pAntebrazoD = 1
            else:
                pAntebrazoD = 2

            if angI>60 and angI<100:
                pAntebrazoI = 1
            else:
                pAntebrazoI = 2

            

            per = np.interp(angI,(30,160),(100,0))
            bar = np.interp(angI,(30,160),(100,650)) #el minimo y el maximo son diferentes para open cv
            #print(int(angI),per)


        cTime= time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN,
                    5, (0, 255, 255), 5)


        # Reajuste de tamaños
        escala = 0.3
        width, height, _ = img.shape
        alto = int(width * escala)
        ancho = int(height * escala)
        img = cv2.resize(img, (ancho, alto))

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        count+=1

        #Almacenamiento de datos
        filas.append(count)
        pandasl.append(1)
        estiramiento.append(int(LargeD))
        punto_estiramiento.append(int(pp))
        angulos.append(int(angBDT))
        punto_angulos.append(int(pBDT))
        antebrazoD.append(int(angD))
        antebrazoI.append(int(angI))
        punto_antebrazoD.append(int(pAntebrazoD))
        punto_antebrazoI.append(int(pAntebrazoI))
        #time.sleep(0.5)
    else:
        pandasl.append(-10)
        break

##Post procesado
#Analizo los estiramientos
print("POST")

#+1 Hombro elevado, brazo rotado, brazos abducidos
for i in range(len(estiramiento)):
    print(estiramiento[i])
# Almacenamiento para analizis de datos
# with open("2.csv", "w", newline="") as archivo:
#     writer = csv.writer(archivo)
#     writer.writerow([filas, pandasl,estiramiento])

# Crear un objeto DataFrame
print("a")
print(len(filas))
#print(len(pandasl))
print(len(angulos))
print(len(punto_angulos))
print(len(estiramiento))
print(len(punto_estiramiento))
print(len(antebrazoD))
print(len(punto_antebrazoD))
print(len(antebrazoI))
print(len(punto_antebrazoI))
df = pd.DataFrame({
    "Columna 1": filas,
    #"Columna 2": pandasl,
    "Columna 3": angulos,
    "Columna 4": punto_angulos,
    "Columna 5": estiramiento,
    "columna 6": punto_estiramiento,
    "Columna 7": antebrazoD,
    "Columna 8": punto_antebrazoD,
    "Columna 9": antebrazoI,
    "Columna 10": punto_antebrazoI
})

# Guardar el DataFrame en un archivo CSV
df.to_csv("3.csv")

# - apoyo en el punto