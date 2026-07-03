import React, { useState, useEffect, cloneElement } from "react";

const Carousel = ({ carouselItems, ...rest }) => {
  const [active, setActive] = useState(0);
  let scrollInterval = null;

  useEffect(() => {
    scrollInterval = setTimeout(() => {
      setActive((active + 1) % carouselItems.length);
    }, 2000);
    return () => clearTimeout(scrollInterval);
  });

  return (
    <div className="carousel">
      {carouselItems.map((item, index) => {
        const activeClass = active === index ? " visible" : "";
        return cloneElement(item, {
          ...rest,
          className: `carousel-item${activeClass}`
        });
      })}
    </div>
  );
};

export default Carousel;
