import React from 'react';
import { useState } from "react";
import Modal from "../component/Modal.jsx";

import "./style.css";

export default function App() {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <div className="App">
      <h1>React useBodyScrollLock hook</h1>
      <div
        style={{
          height: "400vh",
          textAlign: "center",
          paddingTop: 100,
          background: "linear-gradient(to bottom, #1fa2ff, #12d8fa, #a6ffcb)"
        }}
      >
        <button onClick={() => setModalOpen(true)}>Open modal</button>
        {modalOpen && <Modal onClose={() => setModalOpen(false)} />}
      </div>
    </div>
  );
}
