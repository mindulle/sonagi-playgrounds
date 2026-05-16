import React from 'react';
import OneSecondTimer from "../component/OneSecondTimer.jsx";
import "./style.css";

export default function App() {
  return (
    <div className="App">
      <h1>React useTimeout hook</h1>
      <OneSecondTimer />
    </div>
  );
}
