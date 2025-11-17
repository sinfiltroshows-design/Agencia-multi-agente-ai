# bots/disenador.py
# ------------------------------------------------------------
# Bot Diseñador: genera o sugiere imágenes usando DALL·E
# ------------------------------------------------------------
from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar variable de entorno con la API key
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_path, ".env"))

client = OpenAI()

def generar_imagen(prompt, nombre="imagen_generada"):
    """
    Genera una imagen a partir de un texto descriptivo (prompt).
    Retorna la URL de la imagen creada por el modelo gpt-image-1 (DALL·E).
    """
    try:
        respuesta = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="512x512"
        )
        url = respuesta.data[0].url
        print(f"🎨 Imagen generada para '{prompt}': {url}")
        return url
    except Exception as e:
        print("⚠️ Error generando imagen:", e)
        return "Error al generar imagen"

# Prueba directa (solo si ejecutas este archivo manualmente)
if __name__ == "__main__":
    prueba = generar_imagen("Anuncio con una taza de café ecológico, fondo verde claro")
    print(prueba)