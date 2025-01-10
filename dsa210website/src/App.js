import React, { useState } from 'react';
import OwnedGames from './OwnedGames';
import Recommendations from './Recommendations';
import PlaytimeAnalytics from './PlaytimeAnalytics';
import UnderplayedGames from './UnderPlayedGames';

function App() {
  const [steamId, setSteamId] = useState("");
  const [steamData, setSteamData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false); // New state for loading indicator

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSteamData(null);
    setLoading(true); // Show loading indicator
    if (!steamId) {
      setError("Please enter a SteamID");
      setLoading(false); // Stop loading
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/api/steam-data?steamid=${steamId}`);
      if (!response.ok) {
        const { error: apiError } = await response.json();
        setError(apiError || "Failed to fetch data.");
        setLoading(false); // Stop loading
        return;
      }
      const data = await response.json();
      setSteamData(data);
    } catch (err) {
      console.error(err);
      setError("Error fetching data.");
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div style={{ margin: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center', color: '#333' }}>Steam Data Viewer</h1>
      <form onSubmit={handleSubmit} style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <label style={{ fontSize: '1.2rem', color: '#555' }}>
          Enter SteamID: 
          <input
            type="text"
            value={steamId}
            onChange={(e) => setSteamId(e.target.value)}
            style={{
              marginLeft: '0.5rem',
              padding: '0.5rem',
              fontSize: '1rem',
              border: '1px solid #ccc',
              borderRadius: '4px',
            }}
          />
        </label>
        <button
          type="submit"
          style={{
            marginLeft: '1rem',
            padding: '0.5rem 1rem',
            fontSize: '1rem',
            backgroundColor: '#007BFF',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Fetch Data
        </button>
      </form>

      {loading && (
        <div style={{ textAlign: 'center', marginTop: '1rem' }}>
          <p style={{ color: '#555', fontSize: '1.2rem' }}>Fetching data, please wait...</p>
          <div className="spinner" style={{ margin: 'auto', width: '50px', height: '50px', border: '5px solid #ccc', borderTop: '5px solid #007BFF', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div>
        </div>
      )}

      {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

      {steamData && (
        <div style={{ marginTop: '2rem', padding: '1rem', backgroundColor: '#f9f9f9', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)' }}>
          <h2 style={{ color: '#007BFF', textAlign: 'center' }}>Data for SteamID: {steamId}</h2>
          <OwnedGames data={steamData.your_games} />
          <Recommendations data={steamData.recommendations} />
          <PlaytimeAnalytics
            totalPlaytime={steamData.total_playtime_hours}
            top5={steamData.top_5_games}
            genres={steamData.genres_distribution}
          />
          <UnderplayedGames data={steamData.underplayed_highly_rated_games} />
        </div>
      )}

      <style>
        {`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        `}
      </style>
    </div>
  );
}

export default App;
