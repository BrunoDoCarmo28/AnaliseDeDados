import pandas as pd
import LabelEncoder #transforma textos em numeros, ele vem om a instalação scikit-learn

#Passo 1: importar base de dados 

tabela = pd.read_csv("clientes.csv")
display(tabela)  #lembrando que display só funciona em extensão .ipynb

#Passo 2: tratar e preparar a base de dados para a IA
#objetivo: prever a coluna score_credito

#todas as ias não trabalham com textos, somente números

display(tabela.info()) 

codificador_profissao = LabelEncoder() #recebendo a função pra codificar
tabela["profissao"] = codificador_profissao.fit_transform(tabela["profissao"]) #tabela recebe ela mesma com o codificador aplicando dentro da coluna

codificador_mix = LabelEncoder()
tabela["mix"] = codificador_mix.fit_transform(tabela["mix"]) #precisa aplicar um para cada, pois o 1 de uma coluna é diferente do 1 das outras


codificador_comportamento_pagamento = LabelEncoder()
tabela["comportamento_pagamento"] = codificador_comportamento_pagamento.fit_transform(tabela["comportamento_pagamento"])

#TERMOS COMUNS: X é o cara que vai ser usado para prever, o Y é quem é o cara que vai ser previsto. A partir dos dados de X, a IA vai descobrir como chegar # nos status contidos em Y

y = tabela["score_credito"]
x = tabela.drop(colums="score_credito", "id_cliente") #id sai pq é inutil, score sai para não virar numero e ser previsto

# O score sai justamente para que a ia PREVEJA, SEM TER A RESPOSTA

from sklearn.model_selection import train_test_split

x_treino, x_teste, y_treino, y_teste = train_test_split(x,y, test_size=0.3)#ficou 30% pra TESTE e 70% para treinar a IA


#Passo 3: criar modelo de previsão OU modelo de IA (ruim, ok bom)
#Modelos mais usados: RandomForest e KNN - Nearest neighbors

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

modelo_arvore = RandomForestClassifier()
modelo_knn = KNeighborsClassifier()

#PRECISA treinar os modelos antes

modelo_arvore.fit(x_treino, y_treino)
modelo_knn.fit(x_treino, y_treino)

#Passo 4 avaliar e escolher o melhor modelo

previsao_arvore = modelo_arvore.predict(x_teste)
previsao_knn = modelo_knn.predict(x_teste)


from sklearn.metrics import accuracy_score #calcular o score de acerto em %

print(accuracy_score(y_teste, previsao_arvore))	
print(accuracy_score(y_teste, previsao_knn))









