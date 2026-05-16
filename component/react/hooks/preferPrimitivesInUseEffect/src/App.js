import React from 'react';
import CartItem from "../component/CartItem.jsx";
import "./style.css";

export default function App() {
  const firstItem = {
    name: "carrot",
    quantity: 1,
    price: 1000,
  };

  return (
    <div className="App">
      <h1>Prefer primitives in useEffect dependencies</h1>
      <CartItem item={firstItem} />
    </div>
  );
}
