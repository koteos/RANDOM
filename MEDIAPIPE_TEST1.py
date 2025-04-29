import cv2  
import mediapipe as mp  

# Inicializa mediapipe  
mp_pose = mp.solutions.pose  
mp_drawing = mp.solutions.drawing_utils  

# Configuración de la captura de video  
cap = cv2.VideoCapture(0)  

with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:  
    while cap.isOpened():  
        ret, image = cap.read()  
        if not ret:  
            break  

        # Convertir la imagen a RGB  
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
        results = pose.process(image_rgb)  

        # Dibujar la postura sobre la imagen si se detectan resultados  
        if results.pose_landmarks:  
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)  

        # Mostrar la imagen  
        cv2.imshow('Postura', image)  

        # Salir con la tecla 'q'  
        if cv2.waitKey(5) & 0xFF == ord('q'):  
            break  

cap.release()  
cv2.destroyAllWindows()  
