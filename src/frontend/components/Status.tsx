type dadosClassificacao = {
    classificacao:string
}

function Status({classificacao}:dadosClassificacao){
    return(
        <h1>{classificacao}</h1>
    )
}

export default Status