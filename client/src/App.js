import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Wallet from './components/Wallet';
import Card from './components/Card';
import './App.css';

const App = () => {
  const [token, setToken] = useState(null);

  const register = async (email, plan) => {
    const res = await fetch('http://neuracoin.org/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, plan })
    });
    const data = await res.json();
    setToken(data.token);
  };

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-900 text-white">
        <nav className="p-4 bg-black">
          <h1 className="text-2xl">NeuraCoin</h1>
        </nav>
        <Routes>
          <Route path="/" element={<RegisterForm register={register} />} />
          <Route path="/wallet" element={<Wallet token={token} />} />
          <Route path="/card" element={<Card token={token} />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

const RegisterForm = ({ register }) => {
  const [email, setEmail] = useState('');
  const [plan, setPlan] = useState('free');

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl mb-4">Join NeuraCoin</h2>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        className="w-full p-2 mb-2 bg-gray-800 rounded"
      />
      <select
        value={plan}
        onChange={(e) => setPlan(e.target.value)}
        className="w-full p-2 mb-2 bg-gray-800 rounded"
      >
        <option value="free">Free ($0)</option>
        <option value="basic">Basic ($10/mo)</option>
        <option value="premium">Premium ($50/mo)</option>
      </select>
      <button
        onClick={() => register(email, plan)}
        className="w-full p-2 bg-blue-600 rounded"
      >
        Register
      </button>
    </div>
  );
};

export default App;
