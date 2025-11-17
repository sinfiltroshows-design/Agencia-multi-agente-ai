from bots.creativo import BotCreativo
from bots.disenador import BotDisenador
from bots.publicista import BotPublicista
from bots.analista import BotAnalista
from utils.logger import log

class BotEstratega:
    """Coordina a los bots creativos, de diseño, publicidad y análisis."""

    def __init__(self):
        self.creativo = BotCreativo()
        self.disenador = BotDisenador()
        self.publicista = BotPublicista()
        self.analista = BotAnalista()
        log("🎯 Estratega listo para orquestar a los bots")

    def crear_plan(self, objetivo):
        log(f"🧩 Diseñando plan para '{objetivo}'")
        return {"objetivo": objetivo, "plataformas": ["Meta", "TikTok", "Google Ads"]}

    def ejecutar_plan(self, plan):
        log("🤝 Coordinando bots...")
        copy = self.creativo.generar_copy(plan)
        media = self.disenador.crear_diseño(plan)
        self.publicista.publicar(copy, media, plan)
        reporte = self.analista.generar_reporte(plan)
        return reporte