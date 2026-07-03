import React from 'react';
import { useState, useRef } from "react";
import useMutationObserver from "../hook/useMutationObserver";
import "./style.css";

export default function App() {
  const mutationRef = useRef();
  const [mutationCount, setMutationCount] = useState(0);
  const incrementMutationCount = () => {
    return setMutationCount(mutationCount + 1);
  };
  useMutationObserver(mutationRef, incrementMutationCount);
  const [content, setContent] = useState("Hello world");

  return (
    <div className="App">
      <h1>React useMutationObserver hook</h1>
      <label for="content-input">Edit this to update the text:</label>
      <textarea
        id="content-input"
        style={{ width: "100%" }}
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <div style={{ width: "100%" }} ref={mutationRef}>
        <div
          style={{
            resize: "both",
            overflow: "auto",
            maxWidth: "100%",
            border: "1px solid black"
          }}
        >
          <h2>Resize or change the content:</h2>
          <p>{content}</p>
        </div>
      </div>
      <div>
        <h3>Mutation count {mutationCount}</h3>
      </div>
    </div>
  );
}
