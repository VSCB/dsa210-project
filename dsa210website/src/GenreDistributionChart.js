import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';

function GenreDistributionChart({ genres }) {
  if (!genres || Object.keys(genres).length === 0) {
    return <p>No genre data available.</p>;
  }

  // Convert genres to an array and sort by count
  const sortedGenres = Object.entries(genres).sort(([, countA], [, countB]) => countB - countA);

  // Get Top 5 and Others
  const top5Genres = sortedGenres.slice(0, 5);
  const otherGenres = sortedGenres.slice(5);

  const labels = top5Genres.map(([genre]) => genre);
  const genreCounts = top5Genres.map(([, count]) => count);

  if (otherGenres.length > 0) {
    labels.push('Others'); // Add "Others" label
    const otherCount = otherGenres.reduce((sum, [, count]) => sum + count, 0);
    genreCounts.push(otherCount);
  }

  // Define chart data
  const data = {
    labels,
    datasets: [
      {
        label: 'Number of Games',
        data: genreCounts,
        backgroundColor: [
          '#36a2eb',
          '#ff6384',
          '#ffce56',
          '#4bc0c0',
          '#9966ff',
          '#c9cbcf', // Color for "Others"
        ],
        hoverOffset: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Top 5 Game Genres + Others',
      },
      legend: {
        position: 'right',
      },
    },
  };

  return (
    <div style={{ maxWidth: '300px', margin: '0 auto' }}> 
      <Pie data={data} options={options} />
    </div>
  );
}

export default GenreDistributionChart;
