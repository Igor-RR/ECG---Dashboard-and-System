from sklearn.preprocessing import StandardScaler # Padronização dos dados
import pandas as pd
import glob
from data.features.funcoes import twd,extrair_features,filtro_NOTCH,filtro_PA,filtro_PB
import numpy as np
# -------------- // -----------------> teste
from sklearn.model_selection import train_test_split # Divide o conjunto de dados de treimaneto.
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
import joblib as jbl
import os

fs = 512

# Padronizador
scaler = StandardScaler()

# Retorna um lista com os csv que tenham features em seu nome
arquivos = glob.glob("../data/raw/*.csv")

# Conveter cada arquivo csv presente na lista em dataframe e depois junta tudo
df = pd.concat([pd.read_csv(i) for i in arquivos])

#### Extraindo dados

df["Tensão"] = filtro_PB(df,40,4,fs)

df["Tensão"] = filtro_PA(df,20,4,fs)

df["Tensão"] = filtro_NOTCH(df,60,2,fs)

df = twd(df,"db4",4)

df = extrair_features(df)

# Treinando o modelo

# Seleção do modelo

kernel = "linear"

print(f"Kernel utilizado: {kernel}")

svm = SVC(kernel=kernel)

# Separar labels de features
X = df.copy()
X = df.drop("Estado",axis=1)

y = df["Estado"]

# Dividir os dados
x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

# Padronizando
x_train = scaler.fit_transform(x_train)
x_test = scaler.fit_transform(x_test)

param_grid = [
    {
        "C":[1],
        # "coef0":[6,8,10],
        # "degree":[2,3]
        # "gamma":[0.001,0.01,0.05]
        
    }
]

grid = GridSearchCV(svm,param_grid,cv=5,scoring="accuracy",return_train_score=True)
grid.fit(x_train,y_train)

print(f"melhores parâmetros: {grid.best_params_}")

svm = grid.best_estimator_

y_pred = svm.predict(x_train)

print("\nDesempenho do modelo sobre os dados de treinamento")

print(f"acurácia:{accuracy_score(y_true=y_train,y_pred=y_pred)}")

print(f"Sensibilidade: {recall_score(y_true=y_train,y_pred=y_pred)}")

print(f"f1-score:{f1_score(y_true=y_train,y_pred=y_pred)}")

print(f"precisão:{precision_score(y_train,y_pred)}")

# # Avalia o modelo com o método da validação cruzada
y_train_pred = cross_val_score(svm,x_train,y_train,cv=5,scoring="accuracy")

print("Validação cruzada: acurácia")

print(y_train_pred)

print(f"Média da validação cruzada: {np.mean(y_train_pred)}")

print(f"Desvio padrão das acurácias: {np.std(y_train_pred)}")

desempenho = svm.predict(x_test)

print("\nDesempenho do modelo sobre os dados de teste")

print(f"acurácia:{accuracy_score(y_true=y_test,y_pred=desempenho)}")

print(f"Sensibilidade: {recall_score(y_true=y_test,y_pred=desempenho)}")

print(f"f1-score:{f1_score(y_true=y_test,y_pred=desempenho)}")

print(f"precisão:{precision_score(y_test,desempenho)}")

# Define o caminho salvar o pkt
caminho_atual = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(caminho_atual, 'svm.pkt')

# Salvar modelo
modelo = jbl.dump(svm, arquivo)





