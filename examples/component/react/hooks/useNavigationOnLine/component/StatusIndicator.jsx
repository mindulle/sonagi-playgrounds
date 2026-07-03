import useNavigatorOnLine from "../hook/useNavigatorOnLine";

const StatusIndicator = () => {
  const isOnline = useNavigatorOnLine();

  return <span>You are {isOnline ? "online" : "offline"}.</span>;
};

export default StatusIndicator;
