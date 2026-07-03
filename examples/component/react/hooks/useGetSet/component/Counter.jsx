import useGetSet from "../hook/useGetSet";

const Counter = () => {
  const [getCount, setCount] = useGetSet(0);
  const onClick = () => {
    setTimeout(() => {
      setCount(getCount() + 1);
    }, 1_000);
  };

  return <button onClick={onClick}>Count: {getCount()}</button>;
};

export default Counter;
