import Modal from "../component/Modal.jsx";
import { useState, useLayoutEffect } from "react";

const useBodyScrollLock = () => {
  useLayoutEffect(() => {
    const originalStyle = window.getComputedStyle(document.body).overflow;
    document.body.style.overflow = "hidden";
    return () => (document.body.style.overflow = originalStyle);
  }, []);
};

const MyApp = () => {
  const [modalOpen, setModalOpen] = useState(false);

  return (
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
  );
};

export default useBodyScrollLock;
