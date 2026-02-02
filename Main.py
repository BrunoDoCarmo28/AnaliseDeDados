import streamlit as st
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


st.set_page_config(page_title="Previsão de Score de Crédito", layout="centered")

st.title("📊 Previsão de Score de Crédito")
st.write("App simples para treinar modelos de Machine Learning")

# Upload do arquivo
arquivo = st.file_uploader("📁 Envie o arquivo clientes.csv", type="csv")

if arquivo:
    tabela = pd.read_csv(arquivo)

    st.subheader("📋 Visualização da base de dados")
    st.dataframe(tabela)

    st.subheader("ℹ️ Informações da base")
    st.write(tabela.info())

    # ===============================
    # Tratamento dos dados
    # ===============================
    st.subheader("⚙️ Preparação dos dados")

    try:
        cod_profissao = LabelEncoder()
        tabela["profissao"] = cod_profissao.fit_transform(tabela["profissao"])

        cod_mix = LabelEncoder()
        tabela["mix"] = cod_mix.fit_transform(tabela["mix"])

        cod_comportamento = LabelEncoder()
        tabela["comportamento_pagamento"] = cod_comportamento.fit_transform(
            tabela["comportamento_pagamento"]
        )

        y = tabela["score_credito"]
        x = tabela.drop(columns=["score_credito", "id_cliente"])

        # Split
        x_treino, x_teste, y_treino, y_teste = train_test_split(
            x, y, test_size=0.3, random_state=42
        )

        # ===============================
        # Modelagem
        # ===============================
        st.subheader("🤖 Treinamento dos modelos")

        if st.button("Treinar modelos"):
            modelo_arvore = RandomForestClassifier(random_state=42)
            modelo_knn = KNeighborsClassifier()

            modelo_arvore.fit(x_treino, y_treino)
            modelo_knn.fit(x_treino, y_treino)

            previsao_arvore = modelo_arvore.predict(x_teste)
            previsao_knn = modelo_knn.predict(x_teste)

            acc_arvore = accuracy_score(y_teste, previsao_arvore)
            acc_knn = accuracy_score(y_teste, previsao_knn)

            st.success("Modelos treinados com sucesso!")

            st.metric("Acurácia - RandomForest", f"{acc_arvore:.2%}")
            st.metric("Acurácia - KNN", f"{acc_knn:.2%}")

            if acc_arvore > acc_knn:
                st.info("🏆 Melhor modelo: RandomForest")
            else:
                st.info("🏆 Melhor modelo: KNN")

    except Exception as e:
        st.error(f"Erro no processamento: {e}")
