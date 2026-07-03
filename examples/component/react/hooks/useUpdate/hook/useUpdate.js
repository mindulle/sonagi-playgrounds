import { useReducer } from "react";

const useUpdate = () => {
  const [, update] = useReducer(() => ({}));
  return update;
};

export default useUpdate;
