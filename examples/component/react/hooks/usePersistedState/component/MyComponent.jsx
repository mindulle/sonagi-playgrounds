import usePersistedState from "../hook/usePersistedState";

const MyComponent = ({ name }) => {
  const [val, setVal] = usePersistedState(name, 10);
  return (
    <input
      value={val}
      onChange={(e) => {
        setVal(e.target.value);
      }}
    />
  );
};

export default MyComponent;
