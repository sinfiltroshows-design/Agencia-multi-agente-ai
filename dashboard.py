# ==============================================================
#  dashboard.py  —  Agencia Multi‑Agente de Marketing Autónomo
# ==============================================================
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# Bots principales
from bots.creativo import *     # si aún los tienes separados
from bots.publicista import plan_publicacion
from bots.disenador import generar_imagen
from bots.analista import analizar_campañas
from bots.common_ai import generar_texto

# ---------------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# ---------------------------------------------------------------
load_dotenv()
st.set_page_config(page_title="Agencia Multi‑Agente", page_icon="🤖")
st.title("🤖 Agencia de Marketing Autónoma")
st.caption("Versión Mistral — Estrategia · Creatividad · Diseño · Análisis")

modo = st.sidebar.radio("Selecciona modo:", ["Crear Campaña", "Analizar Datos"])

# ---------------------------------------------------------------
# FUNCIONALIDAD PRINCIPAL — CREAR CAMPAÑAS
# ---------------------------------------------------------------
if modo == "Crear Campaña":
    producto = st.text_input("📦 Nombre del producto o campaña:")

    if st.button("🚀 Lanzar nueva campaña"):
        if not producto.strip():
            st.warning("Por favor escribe el nombre del producto.")
        else:
            with st.spinner("🤖 Los agentes están trabajando..."):

                # Aprendizaje previo: lee últimos informes
                contexto_prev = ""
                base_informes = "informes_analista"
                if os.path.exists(base_informes):
                    ultimos = sorted(os.listdir(base_informes))[-3:]
                    for archivo in ultimos:
                        with open(os.path.join(base_informes, archivo), encoding="utf-8") as f:
                            contexto_prev += f"\n\n{f.read()}"

                # Agentes principales
                estratega = Agent(
                    role="Estratega de Marketing",
                    goal=f"Diseñar un plan de marketing para el producto {producto}.",
                    backstory=(
                        "Especialista en estrategias digitales con visión de marca. "
                        f"Aprendizajes previos:\n{contexto_prev}"
                    ),
                )

                creativo = Agent(
                    role="Copywriter Creativo",
                    goal="Redactar textos publicitarios atractivos.",
                    backstory=(
                        "Apasionado del storytelling y la comunicación emocional."
                    ),
                )

                # Tareas
                plan = Task(
                    description=f"Elaborar estrategia para {producto}.",
                    expected_output="Documento breve con objetivos, público meta y KPIs.",
                    agent=estratega,
                )

                copy = Task(
                    description=f"Escribir tres variantes de anuncio para {producto}.",
                    expected_output="Tres textos breves para Meta, TikTok y Google Ads.",
                    agent=creativo,
                )

                agencia = Crew(agents=[estratega, creativo], tasks=[plan, copy])
                resultado = agencia.kickoff()

            # Mostrar resultado
            st.subheader("🎯 Resultados")
            st.text_area("Texto generado:", resultado, height=230)
            st.success("✅ Campaña creada con éxito.")

            # Diseño visual
            st.subheader("🎨 Diseño visual sugerido")
            if st.checkbox("Generar imagen representativa"):
                with st.spinner("🎨 Creando imagen..."):
                    prompt_img = (
                        f"Publicidad moderna y ecológica para {producto}, tonos verdes y marrones."
                    )
                    url_img = generar_imagen(prompt_img)
                    st.image(url_img, caption="Diseño sugerido")

            # Plan de publicación
            st.subheader("📢 Plan de publicación")
            if st.checkbox("Crear plan de publicaciones"):
                with st.spinner("📅 Planificando..."):
                    plan_pub = plan_publicacion(producto, resultado[:400])
                    st.text_area("Plan de Publicación", plan_pub, height=200)

            # Guardar resultados
            datos = {
                "fecha": datetime.now().strftime("%Y‑%m‑%d %H:%M:%S"),
                "producto": producto,
                "resultado": resultado,
            }
            archivo = "campañas.csv"
            df = pd.DataFrame([datos])
            df.to_csv(
                archivo,
                mode="a" if os.path.exists(archivo) else "w",
                header=not os.path.exists(archivo),
                index=False,
                encoding="utf‑8",
            )
            st.info("📁 Campaña guardada en campañas.csv")

    # Historial
    st.subheader("📜 Historial")
    if os.path.exists("campañas.csv"):
        st.dataframe(pd.read_csv("campañas.csv"))
    else:
        st.caption("Aún no hay campañas registradas.")

# ---------------------------------------------------------------
# MODO ANÁLISIS
# ---------------------------------------------------------------
if modo == "Analizar Datos":
    st.subheader("🔎 Análisis de Campañas Previas")
    st.write(
        "El Bot Analista examinará las campañas guardadas y producirá un informe resumen."
    )
    if st.button("📊 Generar Informe"):
        with st.spinner("Analizando..."):
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                informe = analizar_campañas()
            resultado = buf.getvalue() or informe