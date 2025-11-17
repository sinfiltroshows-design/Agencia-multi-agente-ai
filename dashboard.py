# ==============================================================
#  dashboard.py  —  Agencia Multi‑Agente IA (versión ampliada)
# ==============================================================
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
import plotly.express as px
import streamlit_authenticator as stauth
from crewai import Agent, Task, Crew

# ---- Cargar entorno -------------------------------------------------
load_dotenv()

# ---- Imports propios ------------------------------------------------
from bots.common_ai import generar_texto, generar_imagen
from bots.analista import analizar_campañas
from bots.estratega_social import plan_redes
from bots.seo import analisis_seo
from bots.ads_automatizado import ads_strategy

# ==============================================================
# CONFIGURACIÓN Y AUTENTICACIÓN
# ==============================================================
st.set_page_config(page_title="Agencia Multi‑Agente IA", page_icon="🤖")
st.title("🤖 Agencia de Marketing Autónoma v2")
st.caption("Estrategia · Creatividad · Diseño · Análisis · SEO · Ads")

usuarios = ['admin', 'equipo']
nombres = ['Administrador', 'Equipo Marketing']
contraseñas = ['12345', 'marketing']
hashed = stauth.Hasher(contraseñas).generate()

auth = stauth.Authenticate(
    nombres, usuarios, hashed,
    "cookie_agencia", "clave_cookie_secreta", cookie_expiry_days=1
)
nombre, auth_status, usuario = auth.login("Inicio de sesión", "main")

if not auth_status:
    st.warning("Por favor inicia sesión para usar la agencia.")
    st.stop()
st.success(f"✅ Sesión iniciada como {name}")

# ==============================================================
# MENÚ LATERAL (Planes)
# ==============================================================
st.sidebar.subheader("💼 Planes de Uso y Monetización
