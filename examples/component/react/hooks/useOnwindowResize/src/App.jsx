import React from 'react';
import useOnWindowResize from "../hook/useOnWindowResize";
import "./style.css";

export default function App() {
  useOnWindowResize(() =>
    console.log(`window size: (${window.innerWidth}, ${window.innerHeight})`)
  );
  return (
    <div className="App">
      <h1>React useOnWindowResize hook</h1>
      <p>Resize the window and check the console</p>
    </div>
  );
}
