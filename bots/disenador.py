# bots/disenador.py
# --------------------------------------------------------------
# BOT DISEÑADOR
# Genera una imagen descriptiva o un prompt para el producto
# usando el proveedor de IA configurado (Mistral, OpenRouter, etc.)
# --------------------------------------------------------------

from bots.common_ai import generar_imagen

def crear_diseño(producto, descripcion_extra=""):
    """
    Genera una imagen o propuesta visual para el producto.
    """
    prompt = (
        f"Diseño publicitario atractivo para {producto}. "
        f"{descripcion_extra}. "
        "Estilo moderno, profesional y ecológico si aplica."
    )

    url_o_prompt = generar_imagen(prompt)
    print("🎨 Diseño generado → ", url_o_prompt)
    return url_o_prompt


# --- Prueba directa (solo si se ejecuta este archivo solo) ---
if __name__ == "__main__":
    resultado = crear_diseño("Café ecológico", "Tonos verdes y marrones, fondo limpio")
    print(resultado)
