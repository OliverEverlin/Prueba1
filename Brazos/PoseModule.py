import cv2
import mediapipe as mp
import time
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

    def findAngle(self, img, p1, p2, p3, draw= True):
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