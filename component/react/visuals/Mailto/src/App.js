import React from 'react';
import Mailto from "../component/Mailto.jsx";
import "./style.css";

export default function App() {
  return (
    <div className="App">
      <h1>Email link</h1>
      <Mailto email="foo@bar.baz" subject="Hello & Welcome" body="Hello world!">
        Mail me!
      </Mailto>
    </div>
  );
}
