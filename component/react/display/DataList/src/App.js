import React from 'react';
import DataList from "../component/DataList.jsx";
import './style.css';

export default function App() {
  return (
    <div className="App">
      <h1>Data list</h1>
      <DataList data={names} />
      <DataList data={names} isOrdered />
    </div>
  );
}
