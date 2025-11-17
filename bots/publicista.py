# bots/publicista.py
# --------------------------------------------------------------
# BOT PUBLICISTA
# Genera un plan simple de publicaciones multilataforma
# usando el proveedor de IA configurado en .env (Mistral, etc.)
# --------------------------------------------------------------

from bots.common_ai import generar_texto

def plan_publicacion(producto, texto_copy):
    """
    Sugiere un calendario básico de publicaciones
    para promocionar el producto descrito.
    """
    prompt = f"""
    Crea un plan de publicaciones semanales para promover {producto}.
    Incluye plataformas recomendadas, tipo de contenido y frecuencia.
    Usa como referencia este copy base:
    {texto_copy}
    """

    plan = generar_texto(prompt)
    print("📢 Plan de publicación generado:")
    print(plan)
    return plan


# Permite probar el módulo si se ejecuta directamente
if __name__ == "__main__":
    ejemplo = plan_publicacion(
        "Café ecológico", 
        "Descubre el sabor natural en cada sorbo"
    )
    print(ejemplo)
