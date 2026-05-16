import React from 'react';
import Callto from "../component/Callto.jsx";
import "./style.css";

export default function App() {
  return (
    <div className="App">
      <h1>Callable telephone link</h1>
      <Callto phone="+302101234567">Call me!</Callto>
    </div>
  );
}
