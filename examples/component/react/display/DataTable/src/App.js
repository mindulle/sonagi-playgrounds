import React from 'react';
import DataTable from "../component/DataTable.jsx";
import './style.css';

export default function App() {
  const people = ["John", "Jesse"];

  return (
    <div className="App">
      <h1>Data table</h1>
      <DataTable data={people} />
    </div>
  );
}
