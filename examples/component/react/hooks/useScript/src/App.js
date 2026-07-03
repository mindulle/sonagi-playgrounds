import React from 'react';
import useScript from "../hook/useScript";
import Child from "../component/Child.jsx";
import "./style.css";

const script =
  "data:text/plain;charset=utf-8;base64,KGZ1bmN0aW9uKCl7IGNvbnNvbGUubG9nKCdIZWxsbycpIH0pKCk7";

export default function App() {
  const status = useScript(script);
  return (
    <div className="App">
      <h1>React useScript hook</h1>
      <p>Parent status: {status}</p>
      <Child />
    </div>
  );
}
