import cv2  
import numpy as np  
import ezdxf  

while True:  
    # Solicitar el nombre del archivo de entrada  
    archivo_entrada = input("Ingresa el nombre del archivo de entrada (incluye la extensión, e.g., 'sign1.jpg'): ")  

    # Solicitar el nombre del archivo de salida  
    archivo_salida = input("Ingresa el nombre del archivo de salida (sin extensión, por ejemplo 'contornos'): ") + ".dxf"  

    # Cargar la imagen  
    imagen = cv2.imread(archivo_entrada)  

    # Verificar si la imagen se cargó correctamente  
    if imagen is None:  
        print("Error: No se pudo cargar la imagen. Verifica la ruta y el nombre.")  
        continue  # Preguntar de nuevo por el archivo de entrada  

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
    doc.saveas(archivo_salida)  
    print(f"Archivo guardado como: {archivo_salida}")  

    # Mostrar la imagen original y la imagen con contornos  
    cv2.imshow('Imagen Original', imagen)  
    cv2.imshow('Contornos', bordes)  

    # Esperar a que se presione una tecla  
    cv2.waitKey(0)  # Esto permitirá que se cierren las ventanas cuando se presione una tecla  
    cv2.destroyAllWindows()  

    # Preguntar si desea generar otro contorno  
    otra_vez = input("¿Deseas generar otro contorno? (s/n): ").strip().lower()  
    if otra_vez != 's':  
        print("Saliendo del programa.")  
        break  
