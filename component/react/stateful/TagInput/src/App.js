import React from 'react';
import TagInput from "../component/TagInput.jsx";
import "./style.css";

export default function App() {
  return (
    <div className="App">
      <h1>Hello CodeSandbox</h1>
      <TagInput tags={["Nodejs", "MongoDB"]} />
    </div>
  );
}
