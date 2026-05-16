import React from 'react';
import FileDrop from "../component/FileDrop.jsx";
import "./style.css";

export default function App() {
  return (
    <div className="App">
      <h1>File drag and drop area</h1>
      <FileDrop onDrop={console.log} />
    </div>
  );
}
