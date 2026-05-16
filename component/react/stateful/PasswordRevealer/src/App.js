import React from 'react';
import PasswordRevealer from "../component/PasswordRevealer.jsx";
import "./style.css";

export default function App() {
  return (
    <div className="App">
      <h1>Show/hide password toggle</h1>
      <PasswordRevealer />
    </div>
  );
}
