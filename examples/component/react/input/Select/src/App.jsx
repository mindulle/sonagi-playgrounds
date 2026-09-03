import React from 'react';
import Select from "../component/Select.jsx";
import "./style.css";

export default function App() {
  const choices = [
    ["grapefruit", "Grapefruit"],
    ["lime", "Lime"],
    ["coconut", "Coconut"],
    ["mango", "Mango"]
  ];

  return (
    <div className="App">
      <h1>Select input value</h1>
      <Select
        values={choices}
        selectedValue="lime"
        onValueChange={(val) => console.log(val)}
      />
    </div>
  );
}
