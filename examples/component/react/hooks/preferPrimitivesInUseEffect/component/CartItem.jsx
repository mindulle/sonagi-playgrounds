import { useEffect } from "react";

const CartItem = ({ item }) => {
  const { name, quantity, price } = item;

  useEffect(() => {
    console.log(`${name} quantity has changed to ${quantity}.`);
  }, [name, quantity]);

  return (
    <>
      <h3>{name}</h3>
      <span>
        {price} x {quantity}
      </span>
    </>
  );
};

export default CartItem;
