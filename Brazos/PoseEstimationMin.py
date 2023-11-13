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
    ## Hace que se vean de manera cartesiana
    print(results.pose_landmarks)
    ##Basicamente que si ve resultados que ubique los puntos en las ubicaciones impresas
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        # Asigno un id a cada punto registrado
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape #le asigno valores de proporcion
            print(id, lm)
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx,cy), 5, (255,0,0),cv2.FILLED)

    #Configuro el tiempo
    cTime= time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    #Configuraciones para mostrar la imagen
    cv2.putText(img, str(int(fps)),(70,100), cv2.FONT_HERSHEY_PLAIN, 8,(0,255,0),10)
    img=cv2.resize(img,(540, 960))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
