from scipy import signal
import numpy as np
import pywt
import pandas as pd

# ---------- VARIÁVEIS IMPORTANTES ---------- #

# level -> Profundidade/Especificidade do corte do filtro
# fc -> Frequencia de corte
# fs -> Frequência na qual o sinal foi amostrado
# Q -> fator de qualidade do filtro notch, assim como level, diz respeito a sua profundidade/especifidade
# wavelet -> Tipo de transformada que vamos utilizar. Ex: "db4"(Daubichies 4),
# ------------------------------------------- #

# Funções para limpeza do sinal

def filtro_PA(df,fc,level,fs):
    
    sinal = df['Tensão']

    # signal.butter -> Constrói um filtro butterworth
    sos_PA = signal.butter(level,fc,'hp',fs=fs,output='sos') # SOS é um array com coeficientes númerico para o filtro
    
    # signal.sosfilt() -> Aplica o filtro sobre o sinal passado
    sinal_PA = signal.sosfiltfilt(sos_PA,sinal)
    return sinal_PA

def filtro_PB(df,fc,level,fs):
    sinal = df['Tensão']

    # signal.butter -> Constrói um filtro butterworth
    sos_PB = signal.butter(level,fc,fs=fs,output='sos') # SOS é um array com coeficientes númerico para o filtro
    
    # signal.sosfilt() -> Aplica o filtro sobre o sinal passado
    sinal_PB = signal.sosfiltfilt(sos_PB,sinal)
    return sinal_PB

def filtro_NOTCH(df,fc,Q,fs):
    
    #Função para projetar o filtro
    b,a = signal.iirnotch(fc, Q, fs) 

    # signal.filtfilt() -> Aplica o filtro no sinal 
    sinal_notch = signal.filtfilt(b,a,df['Tensão'])
    return sinal_notch

# Funções para análise

# Fourier será utilizado para observar a qualidade do sinal, avaliando interferências e ruídos
def fourier(df):
    sinal = df['Tensão'].values

    tempo = df['Tempo'].values

    # Passo
    passo = tempo[1] - tempo[0]

    # np.fft() -> Passa um Transformada de fourier discreta, retornando um array de números complexos
    array_fourier = np.fft.fft(sinal)

    n_pontos = sinal.size

    # Extraímos as frequências e pegamos a primeira metade.A segunda metade é composta pelos mesmos valores, porém negativos
    frequencias = np.fft.fftfreq(n_pontos,passo)[:n_pontos//2]

    # Extraímos as intensidade, ignorando os números complexos
    intensidade = np.abs(array_fourier[:n_pontos//2]) * 2/n_pontos

    return frequencias,intensidade

# Funções para mineração de dados

# Extração de coeficientes das bandas de frequência
def twd (df,wavelet,niveis):

    df = df.copy()

    df['Tempo'] = (df['Tempo'].astype(float))

    lista_estado = []

    # Lista para cada coeficiente gerado pelo nível Wavelet
    lista_CA4 = []
    lista_CD4 = []
    lista_CD3 = []
    lista_CD2 = []
    lista_CD1 = []
    
    tamanho_janela = 512

    for registro in range(0,len(df),tamanho_janela):

        janela = df.iloc[registro:registro + tamanho_janela] # Selecionando o trecho do tamanho da janela
        
        #Ignora a janela final imcompleta
        if len(janela) < tamanho_janela:
            break

        Ca4,Cd4,Cd3,Cd2,Cd1 = pywt.wavedec(janela["Tensão"].values.astype(float),wavelet,level=niveis) # Aplica a transformada
        
        lista_CA4.append(Ca4)
        lista_CD4.append(Cd4)
        lista_CD3.append(Cd3)
        lista_CD2.append(Cd2)
        lista_CD1.append(Cd1)
        lista_estado.append(janela["Estado"].values[0])


    df_wavelet = pd.DataFrame({
        "Ca4": lista_CA4,
        "Cd4": lista_CD4,
        "Cd3":lista_CD3,
        "Cd2":lista_CD2,
        "Cd1":lista_CD1,
        "Estado": lista_estado
    })

    return df_wavelet

# Funções para extração de features

# ----- FEATURES ----- #

# Desvio médio absoluto
# Zero Crossing
# RMS

# Média
# Desvio Padrão
# Máximo
# Mínimo

# ----- ----- ----- #

def extrair_features(df_wavelet):
    
    # Selecionando apenas os coeficientes das frequencias desejadas

    """O sinal foi amostrado em um taxa de amostragem (fs) 512Hz, devido ao teorema de nyquist, apenas as frequências < fs/2 são frequencias confiáveis, logo
    nossa decomposição se inicará em 256Hz
    """

    # Ordem dos coeficentes -> Ca4, Cd4, Cd3, Cd2, Cd1, desconsideraremos Ca4 pois a sua faixa de frequẽncias representa os ruídos de artefatos de movimentos e interferêcias
    coeficientes = ["Cd4","Cd3"]

    for i in coeficientes:

        # Extraíndo as features para cada coeficiente
        df_wavelet[f"Média {i}"] = df_wavelet[i].map(lambda x: np.mean(x)) # map aplica a operação
        df_wavelet[f"Potência {i}"] = df_wavelet[i].map(lambda x: np.mean(np.sum(np.array(x)**2)))
        df_wavelet[f"RMS {i}"] = df_wavelet[i].map(lambda x:np.sqrt(np.mean(np.array(x)**2)))
        df_wavelet[f"ZCR {i}"] = df_wavelet[i].map(lambda x: np.sum(np.diff(np.sign(x)) != 0))
        df_wavelet[f"Desvio padrão {i}"] = df_wavelet[i].map(lambda x: np.std(x))
        df_wavelet[f"Máximo {i}"] = df_wavelet[i].map(lambda x: np.max(x))
        df_wavelet[f"Mínimo {i}"] = df_wavelet[i].map(lambda x: np.min(x))



    # Excluíndo a coluna com coeficientes
    df_wavelet.drop(coeficientes,axis=1, inplace=True)

    #Excluindo Ca4
    df_wavelet.drop("Ca4",axis=1, inplace=True)
    df_wavelet.drop("Cd2",axis=1, inplace=True)
    df_wavelet.drop("Cd1",axis=1, inplace=True)

    return df_wavelet


    
"""

"""
