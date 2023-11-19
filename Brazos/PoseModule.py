import cv2
import mediapipe as mp
import time
import numpy as np
import math

class poseDetector():
    def __init__(self, mode=False, upBody=False, smooth=True):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        #self.detectionCon = 0.5
        #self.trackCon = 0.5

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth)
        #self.pose.setUseGpu(True)
        #self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)



    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        # muestro la deteccion de los puntos en la misma imagen
        ## Hace que se vean de manera cartesiana
        ##Basicamente que si ve resultados que ubique los puntos en las ubicaciones impresas
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
    def findPosition(self, img, draw=True):
        self.lmList = []
        #self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape  # le asigno valores de proporcion
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw = True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        #Calculo de angulo
        angle = abs(math.degrees( math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2,x1-x2)))

        #Draw
        if draw:
            cv2.line(img, (x1, y1),(x2,y2),(0,255,0,3),2)
            cv2.line(img, (x3, y3), (x2, y2), (0, 255, 0, 3),2)

            cv2.circle(img, (x1, y1), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 10, (255, 0, 0),2)
            cv2.circle(img, (x2, y2), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), 2)
            cv2.circle(img, (x3, y3), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), 2)

            cv2.putText(img, str(int(angle)), (x2-56,y2+58), cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        return angle

    def findDistance(self,img, p1, p2, draw = True):
        x1, y1, z1 = self.lmList[p1]
        x2, y2, z2 = self.lmList[p2]
        distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        if draw:
            cv2.line(img, (x1, y1),(x2,y2),(0,255,0,3),2)

            cv2.circle(img, (x1, y1), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 10, (255, 0, 0),2)
            cv2.circle(img, (x2, y2), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), 2)

            #cv2.putText(img, str(int(distancia)), ((x1+x2)*0.5-56,(y1+y2)*0.5+58), cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        return distancia

    def findAngle3D(self, img, p1, p2, p3, draw = True):
        z1, x1, y1 = self.lmList[p1]
        z2, x2, y2 = self.lmList[p2]
        z3, x3, y3 = self.lmList[p3]
        #print(x1," , ",y1, " , ",z1)
        # Calculo de angulo
        vector_a = np.array([x2-x1, y2-y1, z2-z1])
        vector_b = np.array([x2-x3, y2-y3, z2-z3])

        # Calcular el producto punto (producto escalar) de los vectores
        producto_punto = np.dot(vector_a, vector_b)

        # Modulo de cada vector
        magnitud_a = np.linalg.norm(vector_a)
        magnitud_b = np.linalg.norm(vector_b)

        angulo_radianes = np.arccos(producto_punto / (magnitud_a * magnitud_b))
        angulo_grados = np.degrees(angulo_radianes)

        #Logica para solo obtusos maximo
        #if angulo_grados>180
        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0, 3), 2)
            cv2.line(img, (x3, y3), (x2, y2), (0, 255, 0, 3), 2)

            cv2.circle(img, (x1, y1), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), 2)

            cv2.circle(img, (x2, y2), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), 2)

            cv2.circle(img, (x3, y3), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), 2)

            cv2.putText(img, str(int(angulo_grados)), (x2 - 56, y2 + 58), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angulo_grados

    def findAngle3DbyVectors(self, img, p1,p2,p3, draw = True):
        z1, x1, y1 = p1
        z2, x2, y2 = p2
        z3, x3, y3 = p3

        vector_a = np.array([x2 - x1, y2 - y1, z2 - z1])
        vector_b = np.array([x2 - x3, y2 - y3, z2 - z3])
        # Calcular el producto punto (producto escalar) de los vectores
        producto_punto = np.dot(vector_a, vector_b)

        # Modulo de cada vector
        magnitud_a = np.linalg.norm(vector_a)
        magnitud_b = np.linalg.norm(vector_b)

        angulo_radianes = np.arccos(producto_punto / (magnitud_a * magnitud_b))
        angulo_grados = np.degrees(angulo_radianes)

        producto_cruzado = np.cross(vector_a, vector_b)
        if producto_cruzado[2] < 0:  # Verificar el signo del producto cruzado para ajustar el ángulo
            angulo_grados = 360 - angulo_grados

            #Logica para solo obtusos maximo
        #if angulo_grados>180
        # Draw
        if draw:
            cv2.putText(img, str(int(angulo_grados)), (int(x2) - 56, int(y2) + 58), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angulo_grados

    def anteBrazoPuntuation(self, ang):
        # p para tener un codigo más limpio
        if ang > 60 and ang < 100:
            p = 1
        else:
            p = 2
        return p
    def brazoPuntuation(self, ang):
        # p para tener un codigo más limpio
        if (ang < 20):
            p = 1
        elif (ang < 45):
            p = 2
        elif (ang < 90):
            p = 3
        else:
            p = 4
        return p

    def cuelloPuntuation(self, ang):
        # p para tener un codigo más limpio
        if (ang <= 180 and ang>=170):
            p = 1
        elif (ang <= 170 and ang>=160):
            p = 2
        elif (ang <= 180 and ang>=170):
            p = 3
        else:
            p = 4
        return p

    def promDot(self,img, p1, p2,draw=True):
        z1, x1, y1 = self.lmList[p1]
        z2, x2, y2 = self.lmList[p2]

        # print(x1," , ",y1, " , ",z1)
        # Calculo de punto
        vector = [(x1+x2)/2, (y1+y2)/2, (z1+z2)/2]
        if draw:
            cv2.circle(img, (int(vector[0]), int(vector[1])), 7, (255, 0, 0), cv2.FILLED)
        return vector


    ## Funciones Johan
    def findVector(self, img, p1, p2, draw = True):
        x1, y1, z1 = self.lmList[p1]
        x2, y2, z2 = self.lmList[p2]
        vector = [x1-x2,y1-y2,z1-z2]
        if draw:
            cv2.line(img, (x1, y1),(x2,y2),(0,255,0,3),2)

            cv2.circle(img, (x1, y1), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 10, (255, 0, 0),2)
            cv2.circle(img, (x2, y2), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), 2)

        return vector

    def finddistance(self, img, p1,p2,p3,draw=True):
        x1, y1, z1 = self.lmList[p1]
        x2, y2, z2 = self.lmList[p2]
        x3, y3, z3 = self.lmList[p3]
        p1 = np.array(p1)
        p2 = np.array(p2)
        p3 = np.array(p3)
        v = p2 - p1
        vector_p1_p = p3 - p1
        u = np.cross(v, vector_p1_p)
        norma_u = np.linalg.norm(u)
        norma_v = np.linalg.norm(v)
        distancia = norma_u / norma_v

        if draw:
            cv2.line(img, (x1, y1),(x2,y2),(0,255,0,3),2)
            cv2.line(img, (x3, y3), (x2, y2), (0, 255, 0, 3),2)

            cv2.circle(img, (x1, y1), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 10, (255, 0, 0),2)
            cv2.circle(img, (x2, y2), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), 2)
            cv2.circle(img, (x3, y3), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), 2)

        return distancia
        

def main():
    cap = cv2.VideoCapture('PoseVideos/sporttik.mp4')
    pTime = 0
    detector = poseDetector()
    while True:
        # Comentario apra actualizar
        success, img = cap.read()
        img = detector.findPose(img)
        lmList=detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            print(lmList[14])
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

        # Configuro el tiempo
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        # Configuraciones para mostrar la imagen
        cv2.putText(img, str(int(fps)), (70, 100), cv2.FONT_HERSHEY_PLAIN,8, (0, 255, 0), 10)
        img = cv2.resize(img, (540, 960))
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()