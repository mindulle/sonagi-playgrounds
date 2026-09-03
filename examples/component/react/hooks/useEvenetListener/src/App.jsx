import React from 'react';
import useEventListener from "../hook/useEventListener";
import { useState, useCallback } from "react";
import "./style.css";

export default function App() {
  const [coords, setCoords] = useState({ x: 0, y: 0 });

  const updateCoords = useCallback(
    ({ clientX, clientY }) => {
      setCoords({ x: clientX, y: clientY });
    },
    [setCoords]
  );

  useEventListener("mousemove", updateCoords);
  return (
    <div className="App">
      <h1>React useEventListener hook</h1>
      <p>
        Mouse coordinates: {coords.x}, {coords.y}
      </p>
    </div>
  );
}
