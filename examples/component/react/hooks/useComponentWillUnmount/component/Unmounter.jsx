import useComponentWillUnmount from "../hook/useComponentWillUnmount";

const Unmounter = () => {
  useComponentWillUnmount(() => console.log("Component will unmount"));

  return <div>Check the console!</div>;
};

export default Unmounter;
