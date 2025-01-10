import React from 'react';

function OwnedGames({ data }) {
  const getGameIconURL = (appid, iconHash) =>
    `http://media.steampowered.com/steamcommunity/public/images/apps/${appid}/${iconHash}.jpg`;

  if (!data || data.length === 0) {
    return <p>No games found.</p>;
  }

  return (
    <div>
      <h3>Your Owned Games</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, 80px)', gap: '1rem' }}>
        {data.map((game) => (
          <div
            key={game.appid}
            style={{
              textAlign: 'center',
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '0.5rem',
              backgroundColor: '#f9f9f9',
            }}
          >
            <img
              src={getGameIconURL(game.appid, game.img_icon_url)}
              alt={game.name}
              style={{ width: '60px', height: '60px', borderRadius: '8px', marginBottom: '0.5rem' }}
            />
            <p style={{ fontSize: '0.75rem', margin: '0.5rem 0', fontWeight: 'bold' }}>
              {game.name}
            </p>
            <p style={{ fontSize: '0.7rem', color: '#666', margin: '0' }}>
              {Math.floor(game.playtime_forever / 60)} hours
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default OwnedGames;
