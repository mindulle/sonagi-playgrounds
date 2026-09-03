import React from 'react';
import TextArea from "../component/TextArea.jsx";
import "./style.css";

export default function App() {
  return (
    <div className="App">
      <h1>Uncontrolled textarea element</h1>
      <TextArea
        placeholder="Insert some text here..."
        onValueChange={(val) => alert(val)}
      />
    </div>
  );
}
