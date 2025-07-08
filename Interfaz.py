import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

st.set_page_config(page_title="SmartAgro - Gestión de Riego", layout="wide")

st.title("🌾 SmartAgro - Panel de Control Agrícola")
st.markdown("Sistema inteligente de riego autónomo basado en sensores y predicción climática.")

# Configuración personalizada
st.sidebar.header("🔧 Configuración del Sistema")
bateria_minima = st.sidebar.slider("🔋 Nivel mínimo de batería para permitir riego", 0, 100, 40)
humedad_umbral = st.sidebar.slider("💧 Umbral de humedad para riego (%)", 0, 100, 30)
temp_maxima = st.sidebar.slider("🌡️ Temperatura máxima tolerada antes de alerta", 20, 50, 38)
tolerancia_sequia = st.sidebar.selectbox("🧠 Tolerancia del cultivo a la sequía", ["Alta", "Media", "Baja"])

# Simulación de sensores y clima
hora_actual = datetime.now()
humedad_suelo = np.random.randint(15, 60)
temperatura = np.random.randint(20, 45)
bateria_actual = np.random.randint(20, 90)
lluvia_predicha = np.random.choice(["Alta", "Baja", "Nula"], p=[0.2, 0.4, 0.4])
parcelas = ["Parcela Norte", "Parcela Centro", "Parcela Sur"]
parcela_seleccionada = st.selectbox("🌱 Selecciona una parcela", parcelas)

# Métricas principales
top_col1, top_col2, top_col3, top_col4, top_col5 = st.columns(5)
top_col1.metric("💧 Humedad del Suelo", str(humedad_suelo) + "%")
top_col2.metric("🌡️ Temperatura Ambiente", str(temperatura) + " °C")
top_col3.metric("🔋 Batería Disponible", str(bateria_actual) + "%")
top_col4.metric("🌧️ Lluvia Predicha", lluvia_predicha)
top_col5.metric("🧠 Tolerancia", tolerancia_sequia)

st.markdown("---")

# Recomendación del sistema
st.subheader("🤖 Recomendación Inteligente para " + parcela_seleccionada)
regar = False
razon = ""

if humedad_suelo < humedad_umbral:
    if bateria_actual >= bateria_minima:
        if lluvia_predicha == "Nula":
            regar = True
            razon = "Humedad baja, batería suficiente y no se espera lluvia."
        else:
            razon = "Humedad baja, pero se espera lluvia próximamente."
    else:
        razon = "Humedad baja, pero batería insuficiente."
else:
    razon = "Humedad suficiente, no es necesario regar."

if regar:
    st.success("✅ Activar riego recomendado. " + razon)
else:
    st.info("⏳ Esperar antes de regar. " + razon)

# Botón para activar riego manual
if st.button("🚿 Activar riego manual en " + parcela_seleccionada):
    st.warning("🔄 Riego manual ACTIVADO para " + parcela_seleccionada)

# Alerta de temperatura
if temperatura >= temp_maxima:
    st.warning("⚠️ Alerta: Temperatura elevada. Riesgo de estrés térmico en los cultivos.")

# Historial de humedad y temperatura
st.markdown("---")
st.subheader("📊 Historial de Sensores (Últimas 24 horas) - " + parcela_seleccionada)
fechas = pd.date_range(end=hora_actual, periods=24, freq="H")
humedades = np.clip(np.random.normal(loc=40, scale=10, size=24), 10, 70)
temperaturas = np.clip(np.random.normal(loc=30, scale=5, size=24), 20, 45)
df_hist = pd.DataFrame({"Hora": fechas, "Humedad (%)": humedades, "Temperatura (°C)": temperaturas})

# Gráfico 1: Humedad
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(df_hist["Hora"], df_hist["Humedad (%)"], label="Humedad", color="blue", marker="o")
ax1.axhline(y=humedad_umbral, color='gray', linestyle='--', label="Umbral Riego")
ax1.set_xlabel("Hora")
ax1.set_ylabel("Humedad (%)")
ax1.set_title("Evolución de la Humedad del Suelo")
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.legend()
ax1.grid(True)
fig1.autofmt_xdate()
st.pyplot(fig1)

# Gráfico 2: Temperatura
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(df_hist["Hora"], df_hist["Temperatura (°C)"], label="Temperatura", color="orange", marker="s")
ax2.axhline(y=temp_maxima, color='red', linestyle='--', label="Alerta Máxima")
ax2.set_xlabel("Hora")
ax2.set_ylabel("Temperatura (°C)")
ax2.set_title("Evolución de la Temperatura Ambiente")
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax2.legend()
ax2.grid(True)
fig2.autofmt_xdate()
st.pyplot(fig2)

# Exportar configuración personalizada
configuracion = "parcela=" + parcela_seleccionada + "\n" + \
                "bateria_minima=" + str(bateria_minima) + "\n" + \
                "humedad_umbral=" + str(humedad_umbral) + "\n" + \
                "temperatura_maxima=" + str(temp_maxima) + "\n" + \
                "tolerancia_sequia=" + tolerancia_sequia

st.markdown("---")
st.download_button("📁 Exportar configuración actual", data=configuracion, file_name="configuracion_riego.txt")


import webbrowser
webbrowser.open("http://localhost:8501")