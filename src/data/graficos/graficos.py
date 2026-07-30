import data.features.funcoes as funcoes
import plotly.express as px
import pandas as pd
import glob

fs = 512

arquivo = glob.glob("../data/raw/*estendido*.csv")

df = pd.read_csv(arquivo[1])

df["Tensão"] = funcoes.filtro_PB(df,40,4,fs)

df["Tensão"] = funcoes.filtro_PA(df,20,4,fs)

df["Tensão"] = funcoes.filtro_NOTCH(df,60,2,fs)

# # Análise de ruídos e interferências
frequencias,intensidade = funcoes.fourier(df)

fig = px.line(x=frequencias, y=intensidade, title="Frequências presentes no sinal - Braço estendido",labels={"x": "Frequência (Hz)", "y": "Intensidade"})
fig.show()
