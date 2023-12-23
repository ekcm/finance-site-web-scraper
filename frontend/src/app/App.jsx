'use client'
import React, { useState } from 'react';
import Navbar from './Navbar';
import CompanyBody from './CompanyBody';


export default function App() {
  const [isSequential, setSequential] = useState(true);

  const onSequentialChange = (newSequentialState) => {
    setSequential(newSequentialState);
  };

  return (
    <div>
      <Navbar isSequential={isSequential} onSequentialChange = {onSequentialChange} />
      <CompanyBody isSequential={isSequential} />
    </div>
  );
}
