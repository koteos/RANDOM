import cv2  
import numpy as np  
import ezdxf  

# Cargar la imagen  
imagen = cv2.imread(r'C:\Users\Pc\Documents\GitHub\RANDOM\sign1.jpg')  

# Convertir la imagen a escala de grises  
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)  

# Aplicar un desenfoque gaussiano  
desenfocada = cv2.GaussianBlur(gris, (5, 5), 0)  

# Usar Canny para detectar bordes  
bordes = cv2.Canny(desenfocada, 50, 150)  

# Encontrar contornos  
contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  

# Crear un nuevo archivo DXF  
doc = ezdxf.new()  
msp = doc.modelspace()  

# Iterar a través de los contornos y agregar líneas al DXF  
for contorno in contornos:  
    for i in range(len(contorno)):  
        start_point = tuple(contorno[i][0])  
        end_point = tuple(contorno[(i + 1) % len(contorno)][0])  # Conectar al primer punto  
        msp.add_line(start_point, end_point)  

# Guardar el archivo DXF  
doc.saveas(r'C:\Users\Pc\Documents\GitHub\RANDOM\contornos.dxf')  

# Mostrar la imagen original y la imagen con contornos  
cv2.imshow('Imagen Original', imagen)  
cv2.imshow('Contornos', bordes)  

# Esperar a que se presione una tecla y cerrar ventanas  
cv2.waitKey(0)  
cv2.destroyAllWindows()  
