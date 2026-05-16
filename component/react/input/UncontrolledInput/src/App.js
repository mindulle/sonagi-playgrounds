import React from 'react';
import UncontrolledInput from "../component/UncontrolledInput.jsx";
import "./style.css";

export default function App() {
  return (
    <div className="App">
      <h1>Uncontrolled input field</h1>
      <UncontrolledInput
        type="text"
        placeholder="Insert some text here..."
        onValueChange={alert}
      />
    </div>
  );
}
