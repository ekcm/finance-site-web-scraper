'use client'
import React, {useState} from "react";

const Navbar = ( {isSequential, onSequentialChange} ) => {

  const[sequential, setSequential] = useState(isSequential);

  const changeStrategyClick = async() => {
    const newSequentialState = !sequential;
    setSequential(newSequentialState);
    onSequentialChange(newSequentialState)
  }


  return (
    <div className="nav">
      <h1 className="flex items-center justify-center text-white font-bold">Web Scraping Strategy</h1>
      <div className="text-white flex justify-center space-x-4">
        <a
          href="#"
          onClick={changeStrategyClick}
          className={(isSequential === true 
            ? ' text-yellow-1 text-xs hover:text-yellow-2 duration-300'
            : 'text-grey-1 hover:text-white text-xs duration-300'
          )}
        >Sequential</a>

        <a
          href="#"
          onClick={changeStrategyClick}
          className={(isSequential === false 
            ? ' text-blue-1 text-xs hover:text-blue-2 duration-300'
            : 'text-grey-1 hover:text-white text-xs duration-300'
          )}
        >Concurrent</a>
      </div>
    </div>
  )

};

export default Navbar;