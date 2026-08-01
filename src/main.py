import consumer.consumer as consumer
import data.features.funcoes as funcoes
from scipy import stats # Importa o desvio padrão
import plotly.express as px
import joblib as jlb
import glob
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import requests as req

# tempo_inicio = time.perf_counter()

# Porta que hospeda o fastAPi, server devido ao container
url = "http://server:8000/push"

fs = 512 # taxa de amostragem EMG
svm = jlb.load("./models/svm.pkt") # Acoplando o modelo

scaler = StandardScaler()

# iniciando o fluxo de dados

# Coleta

# # Este trecho será adicionado somente no sistema em tempo real
# df = consumer.consumer()

# df = df.drop(df.index[-1])

# arquivo = glob.glob("../data/raw/*estendido*.csv")

arquivo = glob.glob("**.csv")

print(arquivo)

# print(arquivo)

while True:

    for i in arquivo:
        df = pd.read_csv(i)

        # O frontedn do sparkfun na configuração de monitor cardiáco, permite a passagem de 0,5 - 40hz de frequência
        # Os sinais de EMG possuem banda util de 10 - 450 hz
        # PA -> fc = 10hz
        # NOTCH -> 60 hz
        # PB -> 40hz

        # Dados para o gráfico de linha
        sinal_bruto = df['Tensão'].tolist()
        tempo = df['Tempo'].tolist()

        df['Tensão'] = funcoes.filtro_PA(df,20,4,fs)
        df["Tensão"] = funcoes.filtro_PB(df,40,2,fs)
        df['Tensão'] = funcoes.filtro_NOTCH(df,60,2,fs)

        # Dados para o gráfico de barras (Frequências contidas no sinal)
        frequencias,intensidade = funcoes.fourier(df)

        frequencias = np.round(frequencias,1)
        intensidade = np.round(intensidade,2)

        # Converte para lista para possibilitar a conversão para JSON
        frequencias = frequencias.tolist()
        intensidade = intensidade.tolist()

        data = funcoes.twd(df,"db4",4)

        data = funcoes.extrair_features(data)

        data = data.drop("Estado",axis=1)

        data = scaler.fit_transform(data)

        classificacoes = svm.predict(data)

        # Votação

        n_relaxado = np.count_nonzero(classificacoes == 0)
        n_contraido = np.count_nonzero(classificacoes == 1)

        if n_relaxado > n_contraido:
            print("Braço relaxado")
            classificacao = "Relaxado"

        elif n_contraido > n_relaxado:
            print("Braço contraído")
            classificacao = "Contraído"
        else:
            pass

        lista_frequencias = []

        lista_intensidade = []

        for i in range(len(frequencias)):

            if frequencias[i] < 20:
                pass
            elif (frequencias[i] < 40) and (frequencias[i] > 20):
                lista_frequencias.append(frequencias[i])
                lista_intensidade.append(intensidade[i])
            elif(frequencias[i] > 40):
                break

        # Json de resposta que será enviado à API
        dados = {
            "classificacao":classificacao,
            "amplitudes":lista_intensidade,
            "frequencias":lista_frequencias,
            "tensao":sinal_bruto,
            "tempo":tempo
        }

        # Envio de dados para API
        resposta = req.post(url,json=dados)



# tempo_final = time.perf_counter()

# print(f"Diferença de tempo: {tempo_final - tempo_inicio}")



