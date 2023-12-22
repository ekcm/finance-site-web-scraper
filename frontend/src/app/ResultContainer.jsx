'use client';
import React, {useState} from 'react';

const ResultContainer = ( {buttonClicked}) => {

  return (
    <div className="w-3/5 mx-auto">
      <div className="glassmorphismContainer">
        <div>
          {buttonClicked ? (
            <h1>button is clicked</h1>
          ) : (
            <h1>button is not clicked</h1>
          )}
        </div>
      </div>
    </div>

  );
};

export default ResultContainer;