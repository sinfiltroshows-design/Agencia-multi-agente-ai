# ==============================================================
#  dashboard.py  —  Agencia Multi‑Agente IA (versión Mistral)
# ==============================================================
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# --- Cargar configuración de entorno (.env) ---
load_dotenv()

# --- Bots principales (trabajan a través de common_ai) ---
from bots.common_ai import generar_texto, generar_imagen
from bots.analista import analizar_campañas

# --------------------------------------------------------------
# CONFIGURACIÓN BASE DEL DASHBOARD
# --------------------------------------------------------------
st.set_page_config(page_title="Agencia Multi‑Agente IA", page_icon="🤖")
st.title("🤖 Agencia de Marketing Autónoma")
st.caption("Estrategia · Creatividad · Diseño · Análisis  —  Motor: Mistral AI")

modo = st.sidebar.radio("Selecciona modo:", ["Crear Campaña", "Analizar Datos"])

# --------------------------------------------------------------
# MODO 1: CREAR CAMPAÑA
# --------------------------------------------------------------
if modo == "Crear Campaña":
    st.header("🚀 Creación de Campaña de Marketing")

    producto = st.text_input("📦 Nombre del producto o campaña:")

    if st.button("Lanzar nueva campaña"):
        if not producto.strip():
            st.warning("Por favor escribe el nombre del producto.")
        else:
            with st.spinner("🤖 Los agentes están elaborando el plan..."):

                # ----- Contexto de campañas previas -----
                base_informes = "informes_analista"
                contexto_prev = ""
                if os.path.exists(base_informes):
                    ultimos = sorted(os.listdir(base_informes))[-3:]
                    for archivo in ultimos:
                        with open(
                            os.path.join(base_informes, archivo), encoding="utf-8"
                        ) as f:
                            contexto_prev += f"\n\n{f.read()}"

                # ----- Estratega -----
                prompt_plan = f"""
                Eres un estratega de marketing.
                Desarrolla un plan de promoción para el producto {producto}.
                Incluye público objetivo, canales principales, tono y KPIs.
                Considera los aprendizajes previos: {contexto_prev}
                """
                plan = generar_texto(prompt_plan)

                # ----- Creativo -----
                prompt_copy = f"""
                Imagina que eres copywriter.
                Escribe tres textos publicitarios breves y memorables
                para una campaña llamada "{producto}".
                Adáptalos a Meta, TikTok y Google Ads.
                """
                copy = generar_texto(prompt_copy)

                resultado_total = f"=== PLAN DE MARKETING ===\n{plan}\n\n=== COPYS ===\n{copy}"

            # --------------------------------------------------
            # Mostrar resultados
            # --------------------------------------------------
            st.subheader("🎯 Resultados de la campaña")
            st.text_area("Texto generado:", resultado_total, height=250)
            st.success("✅ Campaña generada correctamente.")

            # ----- Generar imagen / diseño visual -----
            st.subheader("🎨 Diseño visual sugerido")
            if st.checkbox("Generar imagen representativa", value=True):
                with st.spinner("🎨 Creando imagen visual..."):
                    prompt_img = (
                        f"Anuncio publicitario para {producto}. "
                        "Estilo moderno, ecológico y profesional. "
                        "Tonos verdes y neutros, fondo limpio."
                    )
                    url_img = generar_imagen(prompt_img)
                    st.image(url_img, caption="Diseño generado")

            # ----- Crear plan de publicación -----
            st.subheader("📢 Plan de publicación sugerido")
            if st.checkbox("Crear plan de publicaciones", value=True):
                with st.spinner("🗓 El Publicista está organizando..."):
                    prompt_pub = f"""
                    Eres un publicista. 
                    Diseña un plan semanal de publicaciones para promocionar {producto}.
                    Indica plataformas, horarios, tipo de contenido y objetivo.
                    Basado en este copy: {copy}
                    """
                    plan_pub = generar_texto(prompt_pub)
                    st.text_area("Plan de Publicación", plan_pub, height=200)

            # ----- Guardar campaña -----
            datos = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "producto": producto,
                "resultado": resultado_total,
            }
            archivo = "campañas.csv"
            df = pd.DataFrame([datos])
            df.to_csv(
                archivo,
                mode="a" if os.path.exists(archivo) else "w",
                header=not os.path.exists(archivo),
                index=False,
                encoding="utf-8",
            )
            st.info("📁 Campaña guardada en campañas.csv")

    # ----- Historial de campañas -----
    st.subheader("📜 Historial de Campañas")
    if os.path.exists("campañas.csv"):
        data = pd.read_csv("campañas.csv")
        st.dataframe(data)
    else:
        st.caption("Aún no hay campañas registradas.")

# --------------------------------------------------------------
# MODO 2: ANALIZAR CAMPAÑAS
# --------------------------------------------------------------
if modo == "Analizar Datos":
    st.header("🔎 Análisis de Campañas")

    st.write(
        "El bot Analista leerá las campañas almacenadas y producirá un informe con tendencias y recomendaciones."
    )

    if st.button("📊 Generar informe analítico"):
        with st.spinner("Analizando..."):
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                informe = analizar_campañas()
            salida = buf.getvalue() or informe

        st.text_area("Informe Analítico:", salida, height=300)
        st.success("✅ Informe analítico generado.")
