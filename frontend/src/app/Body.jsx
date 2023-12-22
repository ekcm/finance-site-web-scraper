'use client';
import SearchBody from "./SearchBody.jsx"
import ResultContainer from "./ResultContainer.jsx";
import { useState } from "react";

const Body = () => {
  const [buttonClicked, setButtonClicked] = useState(false);

  const handleButtonClick = () => {
    setButtonClicked((prevValue) => !prevValue);
    console.log("button is clicked");
  }

  return (
    <div>
      <SearchBody onButtonClick = {handleButtonClick} />
      <ResultContainer buttonClicked = {buttonClicked} />

    </div>

  );
};

export default Body;