import React from 'react';
import { motion } from 'framer-motion';

const Card = () => (
  <motion.div
    className="p-4 max-w-md mx-auto"
    initial={{ scale: 0 }}
    animate={{ scale: 1 }}
  >
    <h2 className="text-xl mb-4">Your Card</h2>
    <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-4 rounded-lg">
      <p className="text-lg">NeuraCoin Card</p>
      <p>**** **** **** 1234</p>
      <p>Balance: $100.00</p>
    </div>
  </motion.div>
);

export default Card;
