import React from 'react';
import useWindowSize from "../hooks/useWindowSize";
import "./style.css";

export default function App() {
  const { width, height } = useWindowSize();
  return (
    <div className="App">
      <h1>React useWindowSize hook</h1>
      <p>
        Window size: ({width} x {height})
      </p>
    </div>
  );
}
