import useComponentDidMount from "../hook/useComponentDidMount";

const Mounter = () => {
  useComponentDidMount(() => console.log("Component did mount"));

  return <div>Check the console!</div>;
};

export default Mounter;
