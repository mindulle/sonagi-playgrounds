import useScript from "../hook/useScript";

const script =
  "data:text/plain;charset=utf-8;base64,KGZ1bmN0aW9uKCl7IGNvbnNvbGUubG9nKCdIZWxsbycpIH0pKCk7";

const Child = () => {
  const status = useScript(script);
  return <p>Child status: {status}</p>;
};

export default Child;
