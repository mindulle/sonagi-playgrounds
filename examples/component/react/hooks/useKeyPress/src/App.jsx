import React from 'react';
import useKeyPress from "../hook/useKeyPress";
import "./style.css";

export default function App() {
  const wPressed = useKeyPress("w");
  return (
    <div className="App">
      <h1>React useKeyPress hook</h1>
      <p>The "w" key is {!wPressed ? "not " : ""}pressed!</p>
    </div>
  );
}
