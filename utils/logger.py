from datetime import datetime

def log(mensaje: str):
    hora = datetime.now().strftime("%H:%M:%S")
    print(f"[{hora}] {mensaje}")