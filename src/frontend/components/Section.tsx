import BotaoColeta from "./BotaoColeta"
import Card from "./Card"
import GraficoBarras from "./GraficoBarras"
import GraficoLinhas from "./GraficoLinhas"
import Status from "./Status"
import { useState,useEffect } from "react"

// useState -> Cuida do salvamento dos dados e propragação

// useEffect -> Cuida das chamdas de eventos e API

function Section(){

     const initial = {
        classificacao:"Contraído",
        tempo:[0,0,0,0],
        amplitudes:[0,0,0,0],
        tensao:[0,0,0,0],
        frequencias:[0,0,0,0]
    }

    const [dados,setDados] = useState(initial) 

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8000/ws") ; // Abre a conexão webSocket

        // Lê os eventos e atualiza o valor de dados
        ws.onmessage = (event) => {
        setDados(JSON.parse(event.data))
    }

    return() => { ws.close()} // Desfaz quando saímos a conexão pe encerrada

    })


    return(
    <>

        <div id="container-card">
            <Card>
                <GraficoLinhas tensao={dados.tensao} tempo={dados.tempo} />
            </Card>

            <Card>
                <GraficoBarras amplitudes={dados.amplitudes} frequencias={dados.frequencias}/>
            </Card>

            <Card className="card-status">
                <Status classificacao={dados.classificacao}/>
            </Card>
        </div>

        <div id="container-botoes">
            <BotaoColeta id="botao-ligar" buttonName="Iniciar"/>

            <BotaoColeta id="botao-desligar" buttonName="Desligar"/>
        </div>


    </>

    )
}

export default Section