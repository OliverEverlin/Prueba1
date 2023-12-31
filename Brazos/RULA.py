#Proyecto de SIGA
#Grupo 3

##Desarrollado por:
## Oliver Rojas Pumaricra
## Johan Palomino Delgado


import cv2
#import mediapipe as mp
import time
import PoseModule as pm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import csv

cap = cv2.VideoCapture('PoseVideos/curls.mp4') #Poner el nombre de la carpeta del video que usarás
#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
pTime = 0
detector= pm.poseDetector()
count = 0
dir = 0 #1 para cuando sube, 0 para cuando baja

#Definicion de listas -----------------------------------------------
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

    #IF: Como filtro de valores atípicos
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
            #print(LargeD)
            if LargeD > LargeBrazo*1.05:
                pp = pp + 1
            # +1 brazo rotado
            vector_cuerpo = detector.findVector(img, 12, 11)
            vector_plano_mano = np.cross(detector.findVector(img, 16, 20),detector.findVector(img, 18, 16))
            dif = abs(vector_cuerpo[2] - vector_plano_mano[2])
            if dif > 50:
                pp = pp + 1
            # +1 brazos abducidos
            #d = detector.finddistance(img,24,12,14)
            #if d > 300:
            #    pp = pp + 1
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

        #Estimación de FPS
        cTime= time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN,
                    5, (0, 255, 255), 5)


        # Reajuste de tamaños: si la imagen sale muy grande o pequeña solo cambia el valor de la escala
        escala = 0.3
        width, height, _ = img.shape
        alto = int(width * escala)
        ancho = int(height * escala)
        img = cv2.resize(img, (ancho, alto))
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        count+=1

        #Almacenamiento de datos: Se alamacena all en una lista
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
        ##Se filtrará este valor después
        pandasl.append(-10)
        break

#Termina el bucle ----------------------------------


##Post procesado
#Analizo los estiramientos
print("POST")

#+1 Hombro elevado, brazo rotado, brazos abducidos
#for i in range(len(estiramiento)):
#    print(estiramiento[i])
# Almacenamiento para analizis de datos
# with open("2.csv", "w", newline="") as archivo:
#     writer = csv.writer(archivo)
#     writer.writerow([filas, pandasl,estiramiento])

# Crear un objeto DataFrame

##Impresión de numero de valores tomados
print("Se crea el DF")
# print(len(filas))
# #print(len(pandasl))
# print(len(angulos))
# print(len(punto_angulos))
# print(len(estiramiento))
# print(len(punto_estiramiento))
# print(len(antebrazoD))
# print(len(punto_antebrazoD))
# print(len(antebrazoI))
# print(len(punto_antebrazoI))
#Se almacenan las listas en el DF
df = pd.DataFrame({
    "Columna_1": filas,
    #"Columna 2": pandasl,
    "Columna_3": angulos,
    "Columna_4": punto_angulos,
    "Columna_5": estiramiento,
    "columna_6": punto_estiramiento,
    "Columna_7": antebrazoD,
    "Columna_8": punto_antebrazoD,
    "Columna_9": antebrazoI,
    "Columna_10": punto_antebrazoI
})

# Guardar el DataFrame en un archivo CSV
df.to_csv("4.csv")
print(df)
# - apoyo en el punto

#graficas puntos angulos
print("Debería comenzar a graficar")
puntos_a = df["Columna_4"].value_counts()
puntos_a.plot.pie()
df.plot(kind = "scatter", x = 'Columna_1', y = 'Columna_4')
plt.show()

#graficas puntos estiramiento
#puntos_b=df["Columna_6"].value_counts()
#puntos_b.plot.pie()
#df.plot(kind = "scatter", x = 'Columna 1', y = 'Columna 6')

#graficas puntos antebrazo D e I
puntos_c=df["Columna_8"].value_counts()
puntos_c.plot.pie()
df.plot(kind = "scatter", x = 'Columna_1', y = 'Columna_8')
plt.show()


puntos_d=df["Columna_10"].value_counts()
puntos_d.plot.pie()
df.plot(kind = "scatter", x = 'Columna_1', y = 'Columna_10')
plt.show()
