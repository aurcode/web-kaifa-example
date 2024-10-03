import './Dashboard.css';

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [markets, setMarkets] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMarkets = async () => {
      try {
        // Get the access token from localStorage
        const token = localStorage.getItem('access_token');
        
        if (!token) {
          navigate('/login');  // Redirect to login if no token
          return;
        }

        // Fetch markets from the Flask backend
        const response = await axios.get('http://localhost:5000/markets', {
          headers: {
            Authorization: `Bearer ${token}`  // Send the JWT token in the headers
          }
        });
        
        setMarkets(response.data);
      } catch (error) {
        setErrorMessage('Failed to fetch markets. Please try again.');
      }
    };

    fetchMarkets();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');  // Remove token from storage
    navigate('/login');  // Redirect to login page
  };

  return (
    <div className="dashboard">
      <h2>Market Dashboard</h2>

      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}

      <button onClick={handleLogout}>Logout</button>

      <div className="market-list">
        {markets.length > 0 ? (
          <ul>
            {markets.map((market) => (
              <li key={market.id}>
                <strong>{market.name}</strong> - {market.city}, {market.state}
              </li>
            ))}
          </ul>
        ) : (
          <p>No markets found.</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
