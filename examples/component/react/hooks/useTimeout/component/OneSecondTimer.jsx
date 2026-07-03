import { useState } from "react";
import useTimeout from "../hook/useTimeout";

const OneSecondTimer = (props) => {
  const [seconds, setSeconds] = useState(0);
  useTimeout(() => {
    setSeconds(seconds + 1);
  }, 1000);

  return <p>{seconds}</p>;
};

export default OneSecondTimer;
