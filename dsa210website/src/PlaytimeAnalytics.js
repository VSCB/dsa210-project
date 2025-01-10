import React from 'react';
import TopGamesChart from './TopGamesChart';
import GenreDistributionChart from './GenreDistributionChart';

function PlaytimeAnalytics({ totalPlaytime, top5, genres }) {
  // Steam game icon URL helper function
  const getGameIconURL = (appid, iconHash) =>
    `http://media.steampowered.com/steamcommunity/public/images/apps/${appid}/${iconHash}.jpg`;

  // Prepare Top 5 Genres + Others for textual display
  const sortedGenres = Object.entries(genres)
    .sort(([, countA], [, countB]) => countB - countA);
  const top5Genres = sortedGenres.slice(0, 5);
  const otherGenres = sortedGenres.slice(5);
  const otherCount = otherGenres.reduce((sum, [, count]) => sum + count, 0);

  return (
    <div style={{ padding: '1rem', fontFamily: 'Arial, sans-serif' }}>
      <h3>Total Playtime: {totalPlaytime.toFixed(2)} hours</h3>
      
      {/* Top 5 Games by Playtime */}
      <h4>Top 5 Games by Playtime:</h4>
      <ul style={{ display: 'flex', flexWrap: 'wrap', listStyleType: 'none', padding: 0 }}>
        {top5.map((game) => (
          <li
            key={game.appid}
            style={{
              margin: '0.5rem',
              padding: '0.5rem',
              border: '1px solid #ddd',
              borderRadius: '8px',
              textAlign: 'center',
              width: '120px',
              backgroundColor: '#f9f9f9',
            }}
          >
            {/* Game Icon */}
            <img
              src={getGameIconURL(game.appid, game.img_icon_url)}
              alt={game.name}
              style={{
                width: '80px', // Adjusted width for smaller icons
                height: '80px', // Adjusted height for smaller icons
                borderRadius: '4px',
                marginBottom: '0.5rem',
              }}
            />
            {/* Game Name and Playtime */}
            <span style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>{game.name}</span>
            <br />
            <span style={{ fontSize: '0.8rem', color: '#666' }}>
              {Math.floor(game.playtime_forever / 60)} hours
            </span>
          </li>
        ))}
      </ul>
      <TopGamesChart top5={top5} />

      {/* Game Genres Distribution */}
      <h4>Game Genres Distribution:</h4>
      <ul>
        {top5Genres.map(([genre, count]) => (
          <li key={genre}>
            {genre}: {count} games
          </li>
        ))}
        {otherGenres.length > 0 && (
          <li>Others: {otherCount} games</li>
        )}
      </ul>
      <GenreDistributionChart genres={genres} />
    </div>
  );
}

export default PlaytimeAnalytics;
