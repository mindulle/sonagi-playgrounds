import React from 'react';
import MappedTable from "../component/MappedTable.jsx";
import './style.css';

export default function App() {
  const people = [
    { name: "John", surname: "Smith", age: 42 },
    { name: "Adam", surname: "Smith", gender: "male" }
  ];
  const propertyNames = ["name", "surname", "age"];

  return (
    <div className="App">
      <h1>Object table view</h1>
      <MappedTable data={people} propertyNames={propertyNames} />
    </div>
  );
}
