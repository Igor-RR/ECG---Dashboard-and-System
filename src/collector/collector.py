import serial 
import redis
import time
import struct

# Se conecta com o redis
client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
print(client.ping())

porta = serial.Serial("/dev/ttyACM0", 921600, timeout=5)

TIPOS_NA_STRUCT = "<IBfI"
TAMANHO_STRUCT = struct.calcsize(TIPOS_NA_STRUCT)

porta.reset_input_buffer()

lista_tensao = []
lista_tempo = []
lista_registro = []
lista_estado = []

with porta:

    # Força reset do ESP32 via DTR/RTS
    porta.setDTR(False)
    time.sleep(0.1)
    porta.setDTR(True)
    time.sleep(2)  # espera o ESP32 reiniciar e inicializar
    porta.reset_input_buffer()

    # Validação da instrução
    while True:
        print("\n--- SISTEMA INICIALIZADO --- \n")
        print("Para Braço estendido, digite 0")
        print("Para o Braço flexionado, dite 1")
        status_serial = input("Digite o estado do braço: ")
        if status_serial in ["0", "1"]:
            porta.write(f"{status_serial}\n".encode())  # ← estava aqui
            break
        print("Digite apenas 0 ou 1!")

    # Coleta dos dados
    registro = 0

    while True: 
        leitura = porta.read(TAMANHO_STRUCT)
        if len(leitura) == TAMANHO_STRUCT and registro!= 0xFFFFFFFF:

            registro,estado,tensao,tempo = struct.unpack(TIPOS_NA_STRUCT,leitura)

            # Faz a conversão para os valores reais
            tensao = tensao*3.3/4095

            # Salva  cada item na lista
            lista_estado.append(estado)
            lista_tensao.append(tensao) 
            lista_tempo.append(tempo)
            lista_registro.append(registro)

            print(f"Registro:{registro},Estado:{estado},Tempo:{tempo},Tensao:{tensao:.3f}")
        
        elif registro == 0xFFFFFFFF:
            print("Todos os registros coletados!")
            break

# Envio para o redis como lista
print("Enviando para o Redis...")
if len(lista_estado) != 0:
    client.rpush(f'estado_{lista_estado[0]}', *lista_estado)
    client.rpush(f'tensao_{lista_estado[0]}', *lista_tensao)
    client.rpush(f'tempo_{lista_estado[0]}', *lista_tempo)
    client.rpush(f'registro_{lista_estado[0]}', *lista_registro)
    print("Ok!")