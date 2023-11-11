import cv2
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils #para dibujar puntos
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture('PoseVideos/sporttik.mp4')
pTime = 0
while True:
    #Comentario apra actualizar
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    #muestro la deteccion de los puntos en la misma imagen
    print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

    #Configuro el tiempo
    cTime= time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    #Configuraciones para mostrar la imagen
    cv2.putText(img, str(int(fps)),(70,100), cv2.FONT_HERSHEY_PLAIN, 8,(0,255,0),10)
    img=cv2.resize(img,(540, 960))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
