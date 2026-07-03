import useMediaQuery from "../hook/useMediaQuery";

const ResponsiveText = () => {
  const text = useMediaQuery(
    "(max-width: 400px)",
    "Less than 400px wide",
    "More than 400px wide"
  );

  return <span>{text}</span>;
};

export default ResponsiveText;
