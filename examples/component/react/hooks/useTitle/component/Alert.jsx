import useTitle from "../hook/useTitle";

const Alert = () => {
  useTitle("Alert");
  return <p>Alert! Title has changed</p>;
};

export default Alert;
