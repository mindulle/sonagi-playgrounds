import React from 'react';
import MyComponent from "../component/MyComponent.jsx";
import { useState } from "react";
import "./style.css";

export default function App() {
  const [name, setName] = useState("my-value");
  return (
    <div className="App">
      <h1>React usePersistedState hook</h1>
      <MyComponent name={name} />
      <input
        value={name}
        onChange={(e) => {
          setName(e.target.value);
        }}
      />
    </div>
  );
}
