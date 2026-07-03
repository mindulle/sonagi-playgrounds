import React from 'react';
import SSRChecker from "../component/SSRChecker.jsx";
import "./style.css";

export default function App() {
  return (
    <div className="App">
      <h1>React useSSR hook</h1>
      <SSRChecker />
    </div>
  );
}
