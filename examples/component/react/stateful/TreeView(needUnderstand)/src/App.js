import React from 'react';
import TreeView from "../component/TreeView.jsx";
import "./style.css";

export default function App() {
  const data = {
    lorem: {
      ipsum: "dolor sit",
      amet: {
        consectetur: "adipiscing",
        elit: [
          "duis",
          "vitae",
          {
            semper: "orci",
          },
          {
            est: "sed ornare",
          },
          "etiam",
          ["laoreet", "tincidunt"],
          ["vestibulum", "ante"],
        ],
      },
      ipsum: "primis",
    },
  };

  return (
    <div className="App">
      <h1>Expandable Tree View</h1>
      <TreeView data={data} name="data" />
    </div>
  );
}
