import React from 'react';
import Unmounter from "../component/Unmounter.jsx";
import "./style.css";

export default function App() {
  return (
    <div className="App">
      <h1>React useComponentWillUnmount hook</h1>
      <Unmounter />
    </div>
  );
}
