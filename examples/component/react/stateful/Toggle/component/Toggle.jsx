import React, { useState } from "react";

const Toggle = ({ defaultToggled = false }) => {
  const [isToggleOn, setIsToggleOn] = useState(defaultToggled);

  return (
    <label className={isToggleOn ? "toggle on" : "toggle off"}>
      <input
        type="checkbox"
        checked={isToggleOn}
        onChange={() => setIsToggleOn(!isToggleOn)}
      />
      {isToggleOn ? "ON" : "OFF"}
    </label>
  );
};

export default Toggle;
