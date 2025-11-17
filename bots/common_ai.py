# bots/common_ai.py
# ================================================================
# Capa común para conectar distintos proveedores de IA
# (Mistral, OpenRouter, Groq, Ollama, OpenAI si aún se requiere)
# ================================================================

import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# ---------------------------------------------------------------
# Determinar proveedor por defecto (AI_PROVIDER en .env)
# ---------------------------------------------------------------
PROVEEDOR_DEFAULT = os.getenv("AI_PROVIDER", "mistral").lower()

# ================================================================
# Generar TEXTO (chat/completions)
# ================================================================
def generar_texto(prompt: str, proveedor: str = PROVEEDOR_DEFAULT) -> str:
    """
    Envía un prompt de texto al proveedor indicado y devuelve la respuesta.
    Soporta: mistral, openrouter, groq, ollama (local) y openai.
    """

    try:
        # --------------------- Mistral -------------------------
        if proveedor == "mistral":
            headers = {
                "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "mistral-small",
                "messages": [{"role": "user", "content": prompt}]
            }
            r = requests.post("https://api.mistral.ai/v1/chat/completions",
                              headers=headers, json=data)
            return r.json()["choices"][0]["message"]["content"]

        # --------------------- OpenRouter -----------------------
        elif proveedor == "openrouter":
            from openai import OpenAI
            client = OpenAI(
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1"
            )
            res = client.chat.completions.create(
                model="mistralai/mixtral-8x7b",
                messages=[{"role": "user", "content": prompt}]
            )
            return res.choices[0].message.content

        # --------------------- Groq ------------------------------
        elif proveedor == "groq":
            headers = {
                "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "mixtral-8x7b",
                "messages": [{"role": "user", "content": prompt}]
            }
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                              headers=headers, json=data)
            return r.json()["choices"][0]["message"]["content"]

        # --------------------- Ollama Local ----------------------
        elif proveedor == "ollama":
            r = requests.post("http://localhost:11434/api/generate",
                              json={"model": "llama3", "prompt": prompt})
            texto = []
            for line in r.iter_lines():
                if line:
                    texto.append(line.decode(errors="ignore"))
            return "".join(texto)

        # --------------------- OpenAI (opcional) -----------------
        elif proveedor == "openai":
            from openai import OpenAI
            client = OpenAI()
            res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return res.choices[0].message.content

        else:
            return f"⚠️ Proveedor desconocido: {proveedor}"

    except Exception as e:
        return f"⚠️ Error con {proveedor}: {e}"


# ================================================================
# Generar IMAGEN (solo si el proveedor lo soporta)
# ================================================================
def generar_imagen(prompt: str, proveedor: str = PROVEEDOR_DEFAULT):
    """
    Devuelve una URL o texto con el resultado de generar una imagen.
    Compatible con OpenAI/OpenRouter que usan gpt-image-1 o DALL·E.
    Para otros proveedores, devuelve el prompt como sugerencia visual.
    """
    try:
        if proveedor in ("openai", "openrouter"):
            from openai import OpenAI
            client = OpenAI()
            result = client.images.generate(
                model="gpt-image-1", prompt=prompt, size="512x512"
            )
            return result.data[0].url
        elif proveedor == "ollama":
            return f"[Prompt local para generar imagen]: {prompt}"
        else:
            return f"[Descripción visual sugerida]: {prompt}"
    except Exception as e:
        return f"⚠️ Error generando imagen: {e}"