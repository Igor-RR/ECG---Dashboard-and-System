import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    scales,
} from "chart.js"

import {Bar} from 'react-chartjs-2'

type dadosGraficoLinha = {
  amplitudes: number[]
  frequencias: number[]
}

// Passa para o chartJS o modo como o gráfico deve ser montado
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend,scales);



// Configurações adicionais do gráfico
const opcoes = {
  responsive: true,
  plugins: {
    legend: {
      position: "top" as const,
    },
    title: {
      display: true,
      text: "Frequências por mês",
    },
  },

  scales:{
    x:{
      grid:{
        display: false
      }
    }
  }
};


function GraficoBarras({amplitudes,frequencias}:dadosGraficoLinha){




  // Dados para a construção do protótipo do gráfico
  const dados = {
    labels: frequencias,
    datasets: [
      {
        label: "Frequência",
        data: amplitudes,
        backgroundColor: "rgba(54, 162, 235, 0.6)",
      },
    ],
  };

  return(
    <Bar data={dados} options={opcoes}/>
    )
}

export default GraficoBarras