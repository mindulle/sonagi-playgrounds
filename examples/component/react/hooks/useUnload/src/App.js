import React from 'react';
import useUnload from "../hook/useUnload";
import "./style.css";

export default function App() {
  useUnload((e) => {
    e.preventDefault();
    const exit = confirm("Are you sure you want to leave?");
    if (exit) window.close();
  });
  return (
    <div className="App">
      <h1>React useUnload hook</h1>
      <div>Try closing the window.</div>
    </div>
  );
}
