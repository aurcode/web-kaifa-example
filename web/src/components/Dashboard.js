import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const MarketList = () => {
  const [markets, setMarkets] = useState([]);

  useEffect(() => {
    const fetchMarkets = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:5000/markets', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setMarkets(response.data);
      } catch (error) {
        console.error('Failed to fetch markets');
      }
    };

    fetchMarkets();
  }, []);

  return (
    <div>
      <h2>Markets List</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>City</th>
            <th>State</th>
            <th>Postal Code</th>
            <th>Details</th>
          </tr>
        </thead>
        <tbody>
          {markets.map((market) => (
            <tr key={market.id}>
              <td>{market.id}</td>
              <td>{market.name}</td>
              <td>{market.city}</td>
              <td>{market.state}</td>
              <td>{market.postal_code}</td>
              <td>
                <Link to={`/markets/${market.id}`}>View Details</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MarketList;
