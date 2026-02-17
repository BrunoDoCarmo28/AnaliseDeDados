# app.py

import pandas as pd
import streamlit as st
import plotly.express as px
import os

# -----------------------------
# Configuração da página
# -----------------------------
st.set_page_config(page_title="Análise de Cancelamentos", layout="wide")
st.title("📊 Análise de Cancelamentos")

# -----------------------------
# Carregar dados (Excel)
# -----------------------------
@st.cache_data
def carregar_dados():
    BASE_DIR = os.path.dirname(__file__)
    CAMINHO = os.path.join(BASE_DIR, "cancelamentos.xlsx")
    
    df = pd.read_excel(CAMINHO)
    df.columns = df.columns.str.strip()
    return df

tabela = carregar_dados()

# -----------------------------
# Tratamento dos dados
# -----------------------------

# Remover CustomerID se existir
tabela = tabela.drop(columns="CustomerID", errors="ignore")

# Padronizar texto da coluna plano
if "plano" in tabela.columns:
    tabela["plano"] = tabela["plano"].astype(str).str.strip().str.title()
    
    # Converter qualquer valor diferente para Mensal ou Anual
    tabela["plano"] = tabela["plano"].replace({
        "Basico": "Mensal",
        "Intermediario": "Mensal",
        "Premium": "Anual"
    })

# Converter cancelou para texto
tabela["cancelou"] = tabela["cancelou"].map({0: "Não", 1: "Sim"})

# -----------------------------
# Seleção de variável
# -----------------------------
st.subheader("🔎 Análise por variável")

coluna = st.selectbox(
    "Selecione a variável para análise:",
    options=[c for c in tabela.columns if c != "cancelou"]
)

# -----------------------------
# Gráfico de Quantidade
# -----------------------------
st.subheader("📊 Quantidade de Cancelamentos")

distribuicao = (
    tabela
    .groupby([coluna, "cancelou"])
    .size()
    .reset_index(name="quantidade")
)

grafico_qtd = px.bar(
    distribuicao,
    x=coluna,
    y="quantidade",
    color="cancelou",
    barmode="group",
    title=f"Cancelamentos por {coluna}"
)

st.plotly_chart(grafico_qtd, use_container_width=True)

# -----------------------------
# Gráfico de Percentual
# -----------------------------
st.subheader("📈 Percentual de Cancelamentos")

percentual = (
    tabela
    .groupby(coluna)["cancelou"]
    .value_counts(normalize=True)
    .mul(100)
    .rename("percentual")
    .reset_index()
)

grafico_pct = px.bar(
    percentual,
    x=coluna,
    y="percentual",
    color="cancelou",
    barmode="group",
    title=f"Percentual de Cancelamento por {coluna}"
)

st.plotly_chart(grafico_pct, use_container_width=True)
