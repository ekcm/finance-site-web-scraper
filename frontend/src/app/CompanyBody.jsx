'use client';
import React, { useState } from "react";

const CompanyBody = () => {

  const [buttonClicked, setButtonClicked] = useState(false);
  const [searchProgress, setSearchProgress] = useState(false);
  const [searchInputValue, setSearchInputValue] = useState('');
  const [fetchedData, setFetchedData] = useState(null);

  const onButtonClick = async() => {
    const inputValue = document.querySelector('.searchInput').value
    console.log("button is clicked");
    setButtonClicked(true);
    setSearchProgress(true);
    setSearchInputValue(inputValue);

    // make fetch request to FastAPI backend
    try{
      const url = 'http://127.0.0.1:5001/api/webscrape/' + inputValue;
      console.log(url)
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok){
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log('Response from backend:', data);
      setFetchedData(data);
      setSearchProgress(false);

    }catch(error){
      console.log("error");
    }

  };

  return(
    <div>
      {/* Search Bar */}

      <div id="searchBar">
        <div className="w-4/5 mx-auto">
          <h1 className="flex items-center justify-center text-white font-bold text-3xl">
            Query company financials
          </h1>
          <div className="flex justify-center p-2">
            <input className="searchInput pl-2" placeholder="Type company name"/>
            <button className="searchButton" onClick={onButtonClick}>Search</button>
          </div>
        </div>
      </div>

      {/* results container */}
      <div>
        <div className="w-3/5 mx-auto">
          <div className="glassmorphismContainer flex items-center justify-center">
            {buttonClicked ? (
              searchProgress ? (
                <div className="grid place-items-center">
                  <h1>searching for {searchInputValue}</h1>
                  <div className="inline-block animate-spin rounded-full border-current border-r-transparent text-neutral-400 w-12 h-12 border-[6px]" role="status">
                  </div>
                </div>
                  ):fetchedData ? (
                    <div className="text-xs">
                      <h1>completed</h1>
                      <table>
                        <thead>
                          <tr>
                            <th>Attribute</th>
                            <th>Value</th>
                          </tr>
                        </thead>
                        <tbody>
                          {Object.entries(fetchedData).map(([source, values]) =>
                            Object.entries(values).map(([company, attributes]) =>
                              Object.entries(attributes).map(([attribute, value]) => (
                                <tr key={attribute}>
                                  <td>{`${source} - ${company} - ${attribute}`}</td>
                                  <td>{value}</td>
                                </tr>
                              ))
                            )
                          )}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <h1>No data found</h1>
                  )
                
            ) : (
              <h1>button is not clicked</h1>
            )}
          </div>
        </div>
      </div>

    </div>
  )
};

export default CompanyBody;