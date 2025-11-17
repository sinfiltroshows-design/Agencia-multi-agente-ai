# bots/analista.py
# ===============================================================
# BOT ANALISTA
# Lee las campañas guardadas en campañas.csv y crea un informe
# usando el proveedor de IA activo (Mistral, OpenRouter, etc.)
# ===============================================================

import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from bots.common_ai import generar_texto

# Cargar las variables de entorno (.env)
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# ---------------------------------------------------------------
def analizar_campañas():
    """Analiza campañas pasadas y genera un informe textual."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    archivo = os.path.join(base_dir, "campañas.csv")

    if not os.path.exists(archivo):
        print("❗ No hay campañas registradas todavía.")
        return "❗ No hay campañas registradas todavía."

    # Leer archivo CSV de campañas
    try:
        df = pd.read_csv(archivo)
    except Exception as e:
        print("⚠️ Error leyendo campañas.csv:", e)
        return f"⚠️ Error leyendo campañas.csv: {e}"

    if df.empty:
        print("⚠️ El archivo campañas.csv está vacío.")
        return "⚠️ El archivo campañas.csv está vacío."

    print(f"📊 Analizando {len(df)} campañas...\n")

    # Concatenar todos los textos de campaña
    contenido = "\n\n".join(df["resultado"].astype(str))

    # Crear el prompt para el modelo
    prompt = f"""
Analiza los siguientes resultados de campañas publicitarias y redacta un informe
breve pero profesional que incluya:

• Temas o ideas que se repiten.
• Qué estilos parecen más persuasivos.
• Recomendaciones para mejorar próximas campañas.

Campañas:
{contenido}
"""

    # Llamar al generador de texto usando el proveedor configurado (.env)
    informe = generar_texto(prompt)

    # Mostrar en consola
    print("=== INFORME DE ANÁLISIS ===\n")
    print(informe)

    # Guardar informe TXT en carpeta informes_analista/
    salida = os.path.join(base_dir, "informes_analista")
    os.makedirs(salida, exist_ok=True)
    nombre = f"informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    ruta_completa = os.path.join(salida, nombre)
    try:
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write(informe)
        print(f"\n📝 Informe guardado en: {ruta_completa}")
    except Exception as e:
        print("⚠️ Error guardando informe:", e)

    return informe


# ---------------------------------------------------------------
# Permite ejecutar el analista directamente desde la terminal
# ---------------------------------------------------------------
if __name__ == "__main__":
    analizar_campañas() 