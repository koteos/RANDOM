import win32com.client  

def renombrar_partes(nuevos_nombres):  
    # Conectarse a Catia  
    catia = win32com.client.Dispatch("CATIA.Application")  
    documentos = catia.Documents  

    print(f"Número de documentos abiertos: {documentos.Count}")  
    
    # Comprobar que hay documentos abiertos  
    if documentos.Count == 0:  
        print("No hay documentos abiertos en Catia.")  
        return  

    # Iterar sobre los documentos y renombrar los CATPart  
    for i in range(1, documentos.Count + 1):  
        doc = documentos.Item(i)  
        
        # Comprobar si el documento es una parte (CATPart)  
        if doc.IsInstanceOf("Part"):  # Verificar si el objeto es un CATPart  
            indice = i - 1  # Ajustar el índice para la lista de nuevos nombres  
            if indice < len(nuevos_nombres):  
                nuevo_nombre = nuevos_nombres[indice]  
                doc.Name = nuevo_nombre  
                print(f"Renombrado: {doc.Name} a {nuevo_nombre}")  
            else:  
                print(f"No hay nuevo nombre disponible para: {doc.Name}")  

    print("Renombramiento completado.")  

# Lista de nuevos nombres para las partes  
nuevos_nombres = ["Parte1", "Parte2", "Parte3"]  # Ajusta según sea necesario  
renombrar_partes(nuevos_nombres)  
