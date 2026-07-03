import React from 'react';
import useSearchParam from "../hook/useSearchParam";
import "./style.css";

export default function App() {
  const post = useSearchParam("post");

  return (
    <div className="App">
      <h1>React useSearchParam hook</h1>
      <p>Post param value: {post || "null"}</p>
      <button
        onClick={() =>
          history.pushState({}, "", location.pathname + "?post=42")
        }
      >
        View post 42
      </button>
      <button onClick={() => history.pushState({}, "", location.pathname)}>
        Exit
      </button>
    </div>
  );
}
