import { useEffect, useRef } from "react";

const useOnGlobalEvent = (type, callback, options) => {
  const listener = useRef(null);
  const previousProps = useRef({ type, options });

  useEffect(() => {
    const { type: previousType, options: previousOptions } = previousProps;

    if (listener.current) {
      window.removeEventListener(
        previousType,
        listener.current,
        previousOptions
      );
    }

    listener.current = window.addEventListener(type, callback, options);
    previousProps.current = { type, options };

    return () => {
      window.removeEventListener(type, listener.current, options);
    };
  }, [callback, type, options]);
};

const App = () => {
  useOnGlobalEvent("mousemove", (e) => {
    console.log(`(${e.x}, ${e.y})`);
  });

  return <p>Move your mouse around</p>;
};

export default useOnGlobalEvent;
