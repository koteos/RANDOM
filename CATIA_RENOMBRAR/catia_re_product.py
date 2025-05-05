import win32com.client  

def renombrar_partes():  
    # Conectarse a Catia  
    catia = win32com.client.Dispatch("CATIA.Application")  
    documentos = catia.Documents  

    # Debug: Verificar cuántos documentos están abiertos  
    print(f"Número de documentos abiertos: {documentos.Count}")  
    
    # Comprobar que hay un documento activo  
    if documentos.Count == 0:  
        print("No hay documentos abiertos en Catia.")  
        return  

    # Obtener el documento activo  
    documento_activo = documentos.ActiveDocument  

    # Debug: Verificar el tipo del documento activo  
    print(f"Documento activo: {documento_activo.Name}, Tipo: {documento_activo.Type}")  

    # Verificar que el documento activo sea un producto  
    if documento_activo.Type != "Product":  
        print("El documento activo no es un producto.")  
        return  

    # Obtener el producto  
    producto = documento_activo.Product  

    # Iterar sobre las partes en el producto  
    for parte in producto.Products:  
        if parte.IsInstanceOf("Part"):  
            # Renombrar solo los primeros 12 caracteres del nombre  
            nuevo_nombre = parte.Name[:12]  # Toma los primeros 12 caracteres  
            parte.Name = nuevo_nombre  
            print(f"Renombrado: {parte.Name} a {nuevo_nombre}")  

    print("Renombramiento completado.")  

# Ejecutar la función  
renombrar_partes()  
