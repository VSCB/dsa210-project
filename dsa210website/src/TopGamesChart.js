import React from 'react';
import { Bar } from 'react-chartjs-2';
// The next import automatically registers Chart.js components
import { Chart as ChartJS } from 'chart.js/auto';

function TopGamesChart({ top5 }) {
  if (!top5 || top5.length === 0) {
    return <p>No top games data available.</p>;
  }

  // Extract labels (game names) and data (playtime in hours)
  const labels = top5.map((game) => game.name);
  const playtimeData = top5.map((game) => Math.floor(game.playtime_forever / 60));

  // Define chart data
  const data = {
    labels,
    datasets: [
      {
        label: 'Playtime (Hours)',
        data: playtimeData,
        backgroundColor: 'rgba(75, 192, 192, 0.6)', // Light teal color
        borderColor: 'rgba(75, 192, 192, 1)',       // Dark teal border
        borderWidth: 1,
      },
    ],
  };

  // Optional chart configuration
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Top 5 Games by Playtime',
      },
    },
  };

  return (
    <div style={{ margin: '1rem 0' }}>
      <Bar data={data} options={options} />
    </div>
  );
}

export default TopGamesChart;
