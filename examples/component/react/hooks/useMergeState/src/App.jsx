import React from 'react';
import useMergeState from "../hook/useMergeState";
import "./style.css";

export default function App() {
  const [data, setData] = useMergeState({ name: "John", age: 20 });

  return (
    <div className="App">
      <h1>React useMergeState hook</h1>
      <input
        value={data.name}
        onChange={(e) => setData({ name: e.target.value })}
      />
      <button onClick={() => setData(({ age }) => ({ age: age - 1 }))}>
        -
      </button>
      {data.age}
      <button onClick={() => setData(({ age }) => ({ age: age + 1 }))}>
        +
      </button>
    </div>
  );
}
