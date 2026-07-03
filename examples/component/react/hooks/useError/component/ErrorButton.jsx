import useError from "../hook/useError";

const ErrorButton = () => {
  const dispatchError = useError();

  const clickHandler = () => {
    dispatchError(new Error("Error!"));
  };

  return <button onClick={clickHandler}>Throw error</button>;
};

export default ErrorButton;
