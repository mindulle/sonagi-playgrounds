import React from 'react';
import AutoLink from "../component/AutoLink.jsx";
import "./style.css";

export default function App() {
  return (
    <div className="App">
      <h1>Automatic text linking</h1>
      <AutoLink text="foo bar baz http://example.org bar" />
    </div>
  );
}
