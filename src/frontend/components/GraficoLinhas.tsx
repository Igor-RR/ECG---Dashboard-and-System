import { Line } from "react-chartjs-2"

type dadosGraficoLinha = {
  tensao: number[]
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
  Decimation,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Decimation
)

const opcoes = {
  responsive: true,
  parsing: false as const,
  animation: false as const,
  maintainAspectRatio: false, // Gráfico deve respeitar a altugar do container
  plugins: {
    legend: { 
      position: 'top' as const
    },
    title: { display: true, text: 'Sinal' },
    decimation: {
      enabled: true,
      algorithm: 'lttb' as const,
      samples: 100,
    },
  },
  scales: {         
    x: {
      type: 'linear' as const,
      grid: {
        display: false
      }
    }
  }
};

function GraficosLinhas({ tensao, tempo }: dadosGraficoLinha) {

  const pontos = tempo.map((t, i) => ({ x: t, y: tensao[i] }))

  const data = {
    datasets: [{
      label: "Tensão",
      data: pontos,
      fill: false,
      backgroundColor: "rgba(54, 162, 235, 0.6)",
      borderColor: "rgba(54, 162, 235, 0.6)",
      pointRadius: 0
    }]
  }

  return (
    <Line data={data} options={opcoes} />
  )
}

export default GraficosLinhas