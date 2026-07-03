import { useState } from "react";

const useMergeState = (initialState = {}) => {
  const [value, setValue] = useState(initialState);

  const mergeState = (newState) => {
    if (typeof newState === "function") newState = newState(value);
    setValue({ ...value, ...newState });
  };

  return [value, mergeState];
};

const MyApp = () => {
  const [data, setData] = useMergeState({ name: "John", age: 20 });

  return (
    <>
      <input
        value={data.name}
        onChange={(e) => setData({ name: e.target.value })}
      />
      <button onClick={() => setData(({ age }) => ({ age: age - 1 }))}>
        -
      </button>
      {data.age}
      <button onClick={() => setData(({ age }) => ({ age: age + 1 }))}>
        +
      </button>
    </>
  );
};

export default useMergeState;
