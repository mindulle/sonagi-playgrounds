import React from 'react';
import CountDown from "../component/CountDown.jsx";
import './style.css';

export default function App() {
  return (
    <div>
      <h1>Countdown timer</h1>
      <CountDown hours={1} minutes={45} />
    </div>
  );
}
