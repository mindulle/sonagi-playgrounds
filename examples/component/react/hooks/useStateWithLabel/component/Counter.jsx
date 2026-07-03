import useStateWithLabel from "../hook/useStateWithLabel";

const Counter = () => {
  const [value, setValue] = useStateWithLabel(0, "counter");
  return <p>{value}</p>;
};

export default Counter;
