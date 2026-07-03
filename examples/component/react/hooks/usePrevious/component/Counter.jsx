import { useState } from "react";
import usePrevious from "../hook/usePrevious";

const Counter = () => {
  const [value, setValue] = useState(0);
  const lastValue = usePrevious(value);

  return (
    <div>
      <p>
        Current: {value} - Previous: {lastValue}
      </p>
      <button onClick={() => setValue(value + 1)}>Increment</button>
    </div>
  );
};

export default Counter;
