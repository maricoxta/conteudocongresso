import streamlit as st
import pandas as pd
from pipeline.Agenda import carregar_dataframe

# Palavras-chave por tema
temas = {
    'Meio Ambiente': ['meio ambiente', 'ambiental', 'floresta', 'biodiversidade', 'ecologia'],
    'Saneamento Básico': ['saneamento', 'água', 'esgoto', 'abastecimento', 'resíduos'],
    'Defesa Civil': ['defesa civil', 'chuvas', 'alagamentos', 'desastres', 'emergência', 'inundações']
}

# Função para classificar eventos por tema
def classificar_evento(texto):
    texto = texto.lower()
    for tema, palavras in temas.items():
        if any(palavra in texto for palavra in palavras):
            return tema
    return 'Outros'

# Título do dashboard
st.set_page_config(page_title="Agenda do Congresso - Temas Ambientais", layout="wide")
st.title("📅 Acompanhamento de Reuniões - Congresso Nacional")

# Carregando os dados da Agenda.py
st.info("🔄 Carregando dados mais recentes da Câmara dos Deputados...")
df = carregar_dataframe()  # A função deve retornar um DataFrame

# Classificando eventos por tema
df['Tema'] = df['nomeResumido'].apply(classificar_evento)

# Filtros
temas_opcao = st.multiselect("Filtrar por tema:", options=list(temas.keys()), default=list(temas.keys()))
datas = st.date_input("Filtrar por data:", [])

# Filtrando os dados
if temas_opcao:
    df = df[df['Tema'].isin(temas_opcao)]

if datas:
    if isinstance(datas, list) and len(datas) == 2:
        start_date, end_date = datas
        df = df[(df['Data e Hora Início'].dt.date >= start_date) & (df['Data e Hora Início'].dt.date <= end_date)]

# Exibindo dados
if df.empty:
    st.warning("Nenhum evento encontrado com os filtros selecionados.")
else:
    for tema in temas_opcao:
        df_tema = df[df['Tema'] == tema]
        if not df_tema.empty:
            st.subheader(f"📌 {tema}")
            st.dataframe(df_tema[['Data e Hora Início', 'Título', 'Local', 'Link']].sort_values('Data e Hora Início'))

# Rodapé
st.markdown("---")
st.caption("Atualizado automaticamente com dados da API da Câmara dos Deputados.")