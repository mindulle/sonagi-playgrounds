const Callto = ({ phone, children }) => {
  return <a href={`tel:${phone}`}>{children}</a>;
};

export default Callto;
