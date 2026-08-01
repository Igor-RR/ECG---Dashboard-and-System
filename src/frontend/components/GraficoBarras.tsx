import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js"

import { Bar } from 'react-chartjs-2'

type dadosGraficoLinha = {
  amplitudes: number[]
  frequencias: number[]
}
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const opcoes = {
  responsive: true,
  animation: false as const,
  maintainAspectRatio: false, // Gráfico deve respeitar o tamanho do container
  plugins: {
    legend: {
      position: 'top' as const
    },
    title: {
      display: true,
      text: "Frequências",
    },
  },
  scales: {
    x: {
      grid: {
        display: false
      }
    }
  }
};

function GraficoBarras({ amplitudes, frequencias }: dadosGraficoLinha) {
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

  return (
    <Bar data={dados} options={opcoes} />
  )
}

export default GraficoBarras