import redis
import pandas as pd
from itertools import chain

def consumer():
    # Se conecta com o redis
    client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

    try:
        while True:
            # Busca as chaves
            estado = list(client.scan_iter(match='estado_[0-9]'))
            tensao = list(client.scan_iter(match='tensao_[0-9]'))
            tempo = list(client.scan_iter(match='tempo_[0-9]'))
            registro = list(client.scan_iter(match='registro_[0-9]'))

            lista_estados = []
            lista_tensoes = []
            lista_tempos = []
            lista_registros = []
                
            # Iterar sobre a lista de chaves que foi retornada
            for i in range(len(estado)):

                # No momento como estou armazendo dados para treinamento client.delete não será usado

                lista_estados.append(client.lrange(estado[i],0,-1))
                lista_tensoes.append(client.lrange(tensao[i],0,-1))
                lista_tempos.append(client.lrange(tempo[i],0,-1))
                lista_registros.append(client.lrange(registro[i],0,-1))

            # Funde as listas internas. Ex: l = [['A','B'],['C','D']] -> l = ['A','B','C','D']
            lista_estados = chain.from_iterable(lista_estados)
            lista_tensoes = chain.from_iterable(lista_tensoes)
            lista_tempos = chain.from_iterable(lista_tempos)
            lista_registros = chain.from_iterable(lista_registros)

            df = pd.DataFrame({

                "N° registro": lista_registros,
                "Tensão": list(map(float,lista_tensoes)),
                "Tempo": list(map(float,lista_tempos)),
                "Estado":lista_estados
                
                })
            
            df['N° registro'] = df['N° registro'].astype(int)
            df['Tempo'] = df['Tempo']/1000000

            # Apaga cada chave presente dentro da lista, liberando o banco
            #client.delete(lista_estados)
            #client.delete(lista_tensoes)
            #client.delete(lista_tempos)
            #client.delete(lista_registros)

            return df

    except (ConnectionError, TimeoutError):
        print("Erro: Não foi possível conectar ao Redis!")
        return None

