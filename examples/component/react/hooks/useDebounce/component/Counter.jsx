import { useState } from "react";
import useDebounce from "../hook/useDebounce";

const Counter = () => {
  const [value, setValue] = useState(0);
  const lastValue = useDebounce(value, 500);

  return (
    <div>
      <p>
        Current: {value} - Debounced: {lastValue}
      </p>
      <button onClick={() => setValue(value + 1)}>Increment</button>
    </div>
  );
};

export default Counter;
