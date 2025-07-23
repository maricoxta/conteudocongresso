# dashboard_app.py

import streamlit as st
from Agenda import carregar_dataframe
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta 

st.set_page_config(page_title="CNM Agenda", layout="wide")
st.title("📅 Agenda Legislativa CNM")

df = carregar_dataframe()

# 🔔 Alertas de proposições (Pop-up)
avisos = df[df['Título'].str.contains('PL', case=False, na=False)]
if not avisos.empty:
    st.warning(f"🔔 Atenção: {len(avisos)} proposição(ões) com 'PL' nesta semana.")

# 📆 Calendário — simplificado por dia
df["dia"] = df["Data e Hora Início"].dt.date
cal_count = df.groupby("dia").size().reset_index(name="eventos")
fig = px.bar(cal_count, x="dia", y="eventos", title="Eventos por Dia")
st.plotly_chart(fig)

# 📋 Lista por área técnica
for area in df["Tema"].unique():
    st.subheader(area)
    st.table(df[df["Tema"] == area][[
        "Data e Hora Início", "Título", "Assunto", "Local", "Link"
    ]])

# 📊 Indicador semanal
hoje = datetime.now().date()
sem = df[df["Data e Hora Início"].dt.date >= hoje - timedelta(days=7)]
ant = df[df["Data e Hora Início"].dt.date.between(hoje - timedelta(days=14), hoje - timedelta(days=7))]
res = sem.groupby("Tema").size().reset_index(name="atual")
ant = ant.groupby("Tema").size().reset_index(name="anterior")
comp = pd.merge(res, ant, on="Tema", how="left").fillna(0)
comp["var%"] = ((comp["atual"]-comp["anterior"])/comp["anterior"].replace(0,1))*100
st.subheader("📊 Indicadores Semanais")
st.table(comp)
