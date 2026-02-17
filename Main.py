# app.py

import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# Configuração da página
# -----------------------------
st.set_page_config(page_title="Análise de Cancelamentos", layout="wide")
st.title("📊 Análise de Cancelamentos")

# -----------------------------
# Carregar dados
# -----------------------------
@st.cache_data
def carregar_dados():
    df = pd.read_csv("cancelamentos.csv")
    df.columns = df.columns.str.strip()
    return df

tabela = carregar_dados()

# Remover CustomerID se existir
tabela = tabela.drop(columns="CustomerID", errors="ignore")

# Transformar 0 e 1 em texto (mais profissional)
tabela["cancelou"] = tabela["cancelou"].map({0: "Não", 1: "Sim"})

# -----------------------------
# Seletor de variável
# -----------------------------
st.subheader("🔎 Análise por variável")

coluna = st.selectbox(
    "Selecione a variável para análise:",
    options=[c for c in tabela.columns if c != "cancelou"]
)

# -----------------------------
# Distribuição dinâmica
# -----------------------------
st.subheader("📊 Distribuição de Cancelamentos")

# Filtrando agrupamento dinâmico
distribuicao = (
    tabela
    .groupby([coluna, "cancelou"])
    .size()
    .reset_index(name="quantidade")
)

grafico = px.bar(
    distribuicao,
    x=coluna,
    y="quantidade",
    color="cancelou",
    barmode="group",
    title=f"Cancelamentos por {coluna}"
)

st.plotly_chart(grafico, use_container_width=True)

# -----------------------------
# Percentual dinâmico
# -----------------------------
st.subheader("📈 Percentual de Cancelamento")

percentual = (
    tabela
    .groupby(coluna)["cancelou"]
    .value_counts(normalize=True)
    .mul(100)
    .rename("percentual")
    .reset_index()
)

grafico_percentual = px.bar(
    percentual,
    x=coluna,
    y="percentual",
    color="cancelou",
    barmode="group",
    title=f"Percentual de Cancelamento por {coluna}"
)

st.plotly_chart(grafico_percentual, use_container_width=True)

