type CardProps = {
    buttonName:string
    id:string
}

function BotaoColeta({buttonName,id}:CardProps){
    return(
        <button id={id}>{buttonName}</button>
    )
}

export default BotaoColeta