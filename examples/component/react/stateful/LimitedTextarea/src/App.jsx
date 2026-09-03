import React from 'react';
import LimitedTextarea from "../component/LimitedTextarea.jsx";
import "./style.css";

export default function App() {
  return (
    <div className="App">
      <h1>Textarea with character limit</h1>
      <LimitedTextarea limit={32} value="Hello!" />
    </div>
  );
}
