from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
client = OpenAI()

def plan_publicacion(producto, texto_copy):
    """Sugiere un plan simple de publicaciones por plataforma."""
    prompt = f"""
Crea un plan básico de publicaciones semanales para promover {producto}.
Incluye plataforma, tipo de contenido y momento ideal de publicación.
Copy base:
{texto_copy}
"""
    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    plan = respuesta.choices[0].message.content
    print("📢 Plan de publicación generado:\n", plan)
    return plan