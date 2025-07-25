from PIL import Image, ImageEnhance
from rembg import remove
import os

# Carpetas de entrada y salida
input_folder = 'fotos_originales'
output_folder = 'fotos_editadas'
os.makedirs(output_folder, exist_ok=True)

# Opciones de mejora
MEJORAR_CONTRASTE = True
FACTOR_CONTRASTE = 1.2  # 1.0 = sin cambio

# Procesar cada archivo de imagen
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Abrir imagen
        with open(input_path, 'rb') as f:
            input_image = f.read()

        # Quitar fondo
        output_image = remove(input_image)

        # Convertir a imagen PIL
        img = Image.open(io.BytesIO(output_image)).convert("RGBA")

        # Crear fondo blanco
        fondo_blanco = Image.new("RGBA", img.size, (255, 255, 255, 255))
        resultado = Image.alpha_composite(fondo_blanco, img).convert("RGB")

        # Opcional: mejorar el contraste
        if MEJORAR_CONTRASTE:
            enhancer = ImageEnhance.Contrast(resultado)
            resultado = enhancer.enhance(FACTOR_CONTRASTE)

        # Guardar imagen resultante
        resultado.save(output_path)

        print(f"Procesada: {filename}")
