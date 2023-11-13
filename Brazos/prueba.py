import cv2
from mediapipe.python.solutions import hands

# Crear el detector de manos
hands = hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Capturar el video
cap = cv2.VideoCapture(0)

while True:
    # Capturar un fotograma
    ret, frame = cap.read()

    # Detectar las manos
    results = hands.process(frame)

    # Dibujar las manos
    hands.draw(frame, results)

    # Mostrar el video
    cv2.imshow("Video", frame)

    # Esperar a que se presione una tecla
    key = cv2.waitKey(1)

    # Cerrar el programa si se presiona la tecla `q`
    if key == ord("q"):
        break

# Cerrar la cámara
cap.release()

# Destruir todas las ventanas abiertas
cv2.destroyAllWindows()