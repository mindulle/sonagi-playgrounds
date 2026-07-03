import React from 'react';
import { useState, useEffect } from "react";
import useDelayedState from "../hook/useDelayedState";
import "./style.css";

export default function App() {
  const [branches, setBranches] = useState([]);
  const [selectedBranch, setSelectedBranch] = useDelayedState(
    branches[0],
    branches.length
  );

  useEffect(() => {
    const handle = setTimeout(() => {
      setBranches(["master", "staging", "test", "dev"]);
    }, 2000);
    return () => {
      handle && clearTimeout(handle);
    };
  }, []);

  return (
    <div className="App">
      <h1>React useDelayedState hook</h1>
      <p>Selected branch: {selectedBranch}</p>
      <select onChange={(e) => setSelectedBranch(e.target.value)}>
        {branches.map((branch) => (
          <option key={branch} value={branch}>
            {branch}
          </option>
        ))}
      </select>
    </div>
  );
}
