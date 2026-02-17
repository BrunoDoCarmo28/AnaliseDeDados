# app.py

import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# Título da aplicação
# -----------------------------
st.set_page_config(page_title="Análise de Cancelamentos", layout="wide")
st.title("📊 Análise de Cancelamentos")

# -----------------------------
# Passo 1 - Importar dados
# -----------------------------
@st.cache_data
def carregar_dados():
    return pd.read_csv("cancelamentos.csv")

tabela = carregar_dados()

# -----------------------------
# Passo 2 - Visualizar dados
# -----------------------------
st.subheader("Base de dados")

tabela.columns = tabela.columns.str.strip()
tabela = tabela.drop(columns="CustomerID", errors="ignore")
st.dataframe(tabela)

# -----------------------------
# Passo 3 - Tratamento dos dados
# -----------------------------
st.subheader("Informações da base (antes do tratamento)")
st.text(tabela.info())

tabela = tabela.dropna()

st.subheader("Informações da base (após remover valores nulos)")
st.text(tabela.info())

# -----------------------------
# Passo 4 - Análise inicial
# -----------------------------
st.subheader("Distribuição de Cancelamentos")

col1, col2 = st.columns(2)

with col1:
    st.write("Quantidade")
    st.write(tabela["cancelou"].value_counts())

with col2:
    st.write("Percentual")
    st.write(tabela["cancelou"].value_counts(normalize=True).mul(100).round(2))

# -----------------------------
# Passo 5 - Análise das causas
# -----------------------------
st.subheader("Análise por variáveis")

# seletor de coluna (bem melhor do que gerar todos de uma vez)
coluna = st.selectbox(
    "Selecione a variável para análise:",
    options=[c for c in tabela.columns if c != "cancelou"]
)

grafico = px.histogram(
    tabela,
    x=coluna,
    color="cancelou",
    barmode="group",
    title=f"Cancelamentos por {coluna}"
)

st.plotly_chart(grafico, use_container_width=True)
