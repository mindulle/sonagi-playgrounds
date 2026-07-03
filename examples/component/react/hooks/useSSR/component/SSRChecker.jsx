import useSSR from "../hook/useSsr";
const SSRChecker = (props) => {
  let { isBrowser, isServer } = useSSR();

  return <p>{isBrowser ? "Running on browser" : "Running on server"}</p>;
};

export default SSRChecker;
