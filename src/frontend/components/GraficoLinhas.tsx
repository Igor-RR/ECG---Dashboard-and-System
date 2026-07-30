import { Line } from "react-chartjs-2"

type dadosGraficoLinha = {
  tensao:number[]
  tempo: number[]
}

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
)



const opcoes = {
responsive: true,
  plugins: {
    legend: { position: 'top' as const },
    title: { display: true, text: 'Sinal' },
  },
  scales:{
    x:{
      grid:{
        display: false
            }
        }
    }
};

function GraficosLinhas({tensao,tempo}:dadosGraficoLinha){

  const data = {
    labels:tempo,
    datasets:[{
        label:"Tensão",
        data:tensao,
        fill: false,
        backgroundColor: "rgba(54, 162, 235, 0.6)",
        borderColor:"rgba(54, 162, 235, 0.6)"
    }]
}
  
    return( 
        <Line data={data} options={opcoes}/>
    )
}

export default GraficosLinhas