import React from 'react';
import useSessionStorage from "../hook/useSessionStorage";
import "./style.css";

export default function App() {
  const [name, setName] = useSessionStorage("name", "John");

  return (
    <div className="App">
      <h1>React useSessionStorage hook</h1>
      <input value={name} onChange={(e) => setName(e.target.value)} />
    </div>
  );
}
