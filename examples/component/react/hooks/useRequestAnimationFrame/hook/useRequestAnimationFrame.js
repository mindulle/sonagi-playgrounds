import { useEffect, useRef } from "react";

const useRequestAnimationFrame = (callback) => {
  const requestRef = useRef();
  const previousTimeRef = useRef();

  const animate = (time) => {
    if (previousTimeRef.current) callback(time - previousTimeRef.current);
    previousTimeRef.current = time;
    requestRef.current = requestAnimationFrame(animate);
  };

  useEffect(() => {
    requestRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(requestRef.current);
  }, []);
};

export default useRequestAnimationFrame;
