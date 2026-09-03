import { useState, useDebugValue } from "react";

const useStateWithLabel = (initialValue, label) => {
  const [value, setValue] = useState(initialValue);
  useDebugValue(`${label}: ${value}`);
  return [value, setValue];
};

export default useStateWithLabel;
