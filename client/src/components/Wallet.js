import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const Wallet = ({ token }) => {
  const [prices, setPrices] = useState({});
  const [amount, setAmount] = useState('');
  const [coin, setCoin] = useState('bitcoin');
  const [toCard, setToCard] = useState(false);

  useEffect(() => {
    fetch('http://neuracoin.org/api/prices')
      .then(res => res.json())
      .then(data => setPrices(data));
  }, []);

  const topUp = async () => {
    await fetch('http://neuracoin.org/api/topup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ email: 'user@example.com', amount: parseFloat(amount), coin, to_card: toCard })
    });
    alert('Top-up successful!');
  };

  return (
    <motion.div
      className="p-4 max-w-md mx-auto"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <h2 className="text-xl mb-4">Wallet</h2>
      <div className="mb-4">
        {Object.keys(prices).map(c => (
          <p key={c}>{c}: ${prices[c].usd}</p>
        ))}
      </div>
      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        placeholder="Amount"
        className="w-full p-2 mb-2 bg-gray-800 rounded"
      />
      <select
        value={coin}
        onChange={(e) => setCoin(e.target.value)}
        className="w-full p-2 mb-2 bg-gray-800 rounded"
      >
        <option value="bitcoin">Bitcoin</option>
        <option value="ethereum">Ethereum</option>
        <option value="tether">USDT</option>
        <option value="solana">Solana</option>
        <option value="binancecoin">BNB</option>
        <option value="ripple">XRP</option>
      </select>
      <label className="flex items-center mb-2">
        <input
          type="checkbox"
          checked={toCard}
          onChange={() => setToCard(!toCard)}
          className="mr-2"
        />
        Move to Card
      </label>
      <button
        onClick={topUp}
        className="w-full p-2 bg-blue-600 rounded"
      >
        Top Up
      </button>
    </motion.div>
  );
};

export default Wallet;
