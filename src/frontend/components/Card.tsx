// Aqui passamos os atributos que o card espera receber
type CardProps = {
    children: React.ReactNode // Habilitamos este componente para reenderizar tudo oq for passado para ele
    className?: string
}


function Card({children,className}: CardProps){
    return(
        <div className={`card ${className || ''}`}>
            <div className="Conteudo-card">
                {children}
            </div>
        </div>
    )
}

export default Card
