import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const MarketDetails = () => {
  const { id } = useParams();  // Get the market ID from the URL
  const [market, setMarket] = useState(null);

  useEffect(() => {
    const fetchMarketDetails = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://localhost:5000/markets/${id}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setMarket(response.data);
      } catch (error) {
        console.error('Failed to fetch market details');
      }
    };

    fetchMarketDetails();
  }, [id]);

  if (!market) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h2>{market.name}</h2>
      <p>City: {market.city}</p>
      <p>State: {market.state}</p>
      <p>Postal Code: {market.postal_code}</p>
    </div>
  );
};

export default MarketDetails;
