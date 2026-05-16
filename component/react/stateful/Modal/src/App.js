import React from 'react';
import React, { useState } from "react";
import Modal from "../component/Modal.jsx";
import "./style.css";

export default function App() {
  const [isModal, setModal] = React.useState(false);
  return (
    <div className="App">
      <h1>Modal dialog</h1>
      <button onClick={() => setModal(true)}>Click Here</button>
      <Modal
        isVisible={isModal}
        title="Modal Title"
        content={<p>Add your content here</p>}
        footer={<button>Cancel</button>}
        onClose={() => setModal(false)}
      />
    </div>
  );
}
