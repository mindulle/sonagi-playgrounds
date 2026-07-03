const Select = ({ disabled, readonly, values, callback, selected }) => {
  return (
    <select
      disabled={disabled}
      readOnly={readonly}
      defaultValue={selected}
      onChange={({ target: { value } }) => alert(value)}
    >
      {values.map(([value, text]) => (
        <option value={value}>{text}</option>
      ))}
    </select>
  );
};

export default Select;
