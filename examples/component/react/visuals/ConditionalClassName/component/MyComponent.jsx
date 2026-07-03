const MyComponent = ({ enabled }) => {
  return <div className={enabled ? "enabled" : ""}> Hi </div>;
};

export default MyComponent;
