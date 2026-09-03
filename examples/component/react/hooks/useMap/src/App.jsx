import React from 'react';
import useMap from "../hook/useMap";
import "./style.css";

export default function App() {
  const [map, { set, remove, clear }] = useMap([["apples", 10]]);
  return (
    <div className="App">
      <h1>React useMap hook</h1>
      <button onClick={() => set(Date.now(), new Date().toJSON())}>Add</button>
      <button onClick={() => clear()}>Reset</button>
      <button onClick={() => remove("apples")} disabled={!map.has("apples")}>
        Remove apples
      </button>
      <pre>
        {JSON.stringify(
          [...map.entries()].reduce(
            (acc, [key, value]) => ({ ...acc, [key]: value }),
            {}
          ),
          null,
          2
        )}
      </pre>
    </div>
  );
}
