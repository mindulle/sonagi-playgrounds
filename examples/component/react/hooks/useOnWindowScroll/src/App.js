import React from 'react';
import useOnWindowScroll from "../hook/useOnWindowScroll";
import "./style.css";

export default function App() {
  useOnWindowScroll(() => console.log(`scroll Y: ${window.pageYOffset}`));
  return (
    <div className="App">
      <h1>React useOnWindowScroll hook</h1>
      <p style={{ height: "300vh" }}>Scroll and check the console</p>
    </div>
  );
}
