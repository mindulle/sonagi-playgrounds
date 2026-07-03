const DataList = ({ isOrdered = false, data }) => {
  const list = data.map((val, i) => <li key={`${i}_${val}`}>{val}</li>);
  return isOrdered ? <ol>{list}</ol> : <ul>{list}</ul>;
};

export default DataList;
