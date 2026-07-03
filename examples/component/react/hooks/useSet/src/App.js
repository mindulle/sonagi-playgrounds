import React from 'react';
import useSet from "../hook/useSet";
import "./style.css";

export default function App() {
  const [set, { add, remove, clear }] = useSet(new Set(["apples"]));

  return (
    <div className="App">
      <h1>React useSet hook</h1>
      <button onClick={() => add(String(Date.now()))}>Add</button>
      <button onClick={() => clear()}>Reset</button>
      <button onClick={() => remove("apples")} disabled={!set.has("apples")}>
        Remove apples
      </button>
      <pre>{JSON.stringify([...set], null, 2)}</pre>
    </div>
  );
}
