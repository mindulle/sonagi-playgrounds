import { useRef, useEffect } from "react";

const useOnWindowScroll = (callback) => {
  const listener = useRef(null);

  useEffect(() => {
    if (listener.current)
      window.removeEventListener("scroll", listener.current);
    listener.current = window.addEventListener("scroll", callback);
    return () => {
      window.removeEventListener("scroll", listener.current);
    };
  }, [callback]);
};

const App = () => {
  useOnWindowScroll(() => console.log(`scroll Y: ${window.pageYOffset}`));
  return <p style={{ height: "300vh" }}>Scroll and check the console</p>;
};

export default useOnWindowScroll;
