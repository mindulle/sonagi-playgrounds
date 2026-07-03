import useToggler from "../hook/useToggler";

const Switch = () => {
  const [val, toggleVal] = useToggler(false);
  return <button onClick={toggleVal}>{val ? "ON" : "OFF"}</button>;
};

export default Switch;
