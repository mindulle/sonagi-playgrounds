import React from 'react';
import useHash from "../hook/useHash";
import { useEffect } from "react";
import "./style.css";

export default function App() {
  const [hash, setHash] = useHash();

  useEffect(() => {
    setHash("#list");
  }, []);

  return (
    <div className="App">
      <h1>React useHash hook</h1>
      <p>window.location.href: {window.location.href}</p>
      <p>Edit hash: </p>
      <input value={hash} onChange={(e) => setHash(e.target.value)} />
    </div>
  );
}
