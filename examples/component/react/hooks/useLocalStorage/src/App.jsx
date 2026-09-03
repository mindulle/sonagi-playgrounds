import React from 'react';
import useLocalStorage from "../hook/useLocalStorage";
import "./style.css";

export default function App() {
  const [name, setName] = useLocalStorage("name", "John");
  return (
    <div className="App">
      <h1>React useLocalStorage hook</h1>
      <input value={name} onChange={(e) => setName(e.target.value)} />
    </div>
  );
}
