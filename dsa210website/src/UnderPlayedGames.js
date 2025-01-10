import React from 'react';

function UnderplayedGames({ data }) {
  const getGameIconURL = (appid, iconHash) =>
    `http://media.steampowered.com/steamcommunity/public/images/apps/${appid}/${iconHash}.jpg`;

  if (!data || data.length === 0) {
    return <div>No underplayed highly-rated games found.</div>;
  }

  return (
    <div>
      <h3>Underplayed Highly-Rated Games</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, 120px)', gap: '1rem' }}>
        {data.map((game, index) => (
          <div
            key={index}
            style={{
              textAlign: 'center',
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '0.5rem',
              backgroundColor: '#f9f9f9',
            }}
          >
            {/* Display the game icon if available */}
            {game.img_icon_url && (
              <img
                src={getGameIconURL(game.appid, game.img_icon_url)}
                alt={game.name}
                style={{
                  width: '80px',
                  height: '80px',
                  borderRadius: '8px',
                  marginBottom: '0.5rem',
                }}
              />
            )}
            {/* Game Name */}
            <p style={{ fontSize: '0.85rem', fontWeight: 'bold', margin: '0' }}>{game.name}</p>
            {/* Playtime */}
            <p style={{ fontSize: '0.75rem', color: '#666', margin: '0.25rem 0' }}>
              Playtime: {game.playtime_hours.toFixed(2)} hours
            </p>
            {/* User Rating */}
            <p style={{ fontSize: '0.75rem', color: '#28a745', margin: '0' }}>
              Rating: {game.user_rating}/100
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default UnderplayedGames;
