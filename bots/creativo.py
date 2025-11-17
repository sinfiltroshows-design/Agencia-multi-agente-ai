from utils.logger import log

class BotCreativo:
    """Bot encargándose de escribir textos publicitarios e ideas creativas."""

    def generar_copy(self, plan):
        log("✍️ Generando texto publicitario...")
        copy = f"Descubre el futuro del sabor: {plan['objetivo']}"
        log(f"🗒️ Copy creado: {copy}")
        return copy