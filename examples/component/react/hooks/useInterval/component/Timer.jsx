import { useState } from "react";
import useInterval from "../hook/useInterval";

const Timer = (props) => {
  const [seconds, setSeconds] = useState(0);
  useInterval(() => {
    setSeconds(seconds + 1);
  }, 1000);

  return <p>{seconds}</p>;
};

export default Timer;
