import React from 'react';
import { useRef } from "react";
import useIntersectionObserver from "../hook/useIntersectionObserver";
import "./style.css";

export default function App() {
  const ref = useRef();
  const onScreen = useIntersectionObserver(ref, { threshold: 0.5 });

  return (
    <div className="App">
      <h1>React useIntersectionObserver hook</h1>
      <div style={{ height: "100vh" }}>Scroll down</div>
      <div style={{ height: "100vh" }} ref={ref}>
        <p>{onScreen ? "Element is on screen." : "Scroll more!"}</p>
      </div>
    </div>
  );
}
