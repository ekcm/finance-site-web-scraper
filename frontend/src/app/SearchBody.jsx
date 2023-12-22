'use client';
import React from 'react';

const SearchBar = ( {onButtonClick }) => {
  return (
    <div className="w-4/5 mx-auto">
      <h1 className="flex items-center justify-center text-white font-bold text-3xl">
        Query company financials
      </h1>

      <div className="flex justify-center p-2">
        <input className="searchInput pl-2" placeholder="Type company name"/>
        <button className="searchButton" onClick={onButtonClick}>Search</button>
      </div>
    </div>

  );
};

export default SearchBar;