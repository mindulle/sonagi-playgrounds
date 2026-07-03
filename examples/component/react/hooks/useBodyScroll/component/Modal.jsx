import useBodyScrollLock from "../hook/useBodyScrollLock";

const Modal = ({ onClose }) => {
  useBodyScrollLock();

  return (
    <div
      style={{
        zIndex: 100,
        background: "rgba(0,0,0,0.25)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
      }}
    >
      <p
        style={{ padding: 8, borderRadius: 8, background: "#fff" }}
        onClick={onClose}
      >
        Scroll locked! <br /> Click me to unlock
      </p>
    </div>
  );
};

export default Modal;
