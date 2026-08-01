from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio

# Craindo o servidor
app = FastAPI()

# Middleware para conexão com react
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tipamos a variável conexão
conexao: WebSocket | None = None
 
#Dados esperados
class Dados(BaseModel):
    classificacao: str
    amplitudes: list[float]
    frequencias: list[float]
    tensao: list[float]
    tempo: list[float]


# Rota para o envio de dados
@app.post("/push")
async def push_dados(payload: Dados):
    # Busca os dados
    dados = payload.model_dump()

    #Verifica a conexão está aberta
    if conexao:
        await conexao.send_json(dados)

# Rota para conexão websocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global conexao
    await websocket.accept() # Aceita a conexão, iniciando a abertura do canal de comunicação
    conexao = websocket
    try:
        while True:
            await conexao.receive_text() # Mantém a escuta, evitando a desconexão
            asyncio.sleep(3)
    except WebSocketDisconnect:
        conexao = None
        print("Conexão encerrada")

#Mantém o servidor rodando      
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
 
 