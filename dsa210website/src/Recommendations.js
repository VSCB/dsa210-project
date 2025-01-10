import React from 'react';

function Recommendations({ data }) {
  if (!data || data.length === 0) {
    return <div>No recommendations found.</div>;
  }

  return (
    <div>
      <h3>Recommended Games:</h3>
      <ul>
        {data.slice(0, 5).map((game, index) => (
          <li key={index}>{game}</li>
        ))}
      </ul>
    </div>
  );
}

export default Recommendations;
