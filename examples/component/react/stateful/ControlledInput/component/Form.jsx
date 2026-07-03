import React, { useState } from "react";
import ControlledInput from "./ControlledInput";

const Form = () => {
  const [value, setValue] = useState("");

  return (
    <ControlledInput
      type="text"
      placeholder="Insert some text here..."
      value={value}
      onValueChange={setValue}
    />
  );
};

export default Form;
