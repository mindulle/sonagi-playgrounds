import React from 'react';
import LazyLoad from "../component/LazyLoad.jsx"
import './style.css';

export default function App() {
  return (
    <div className="App">
      <h1>Lazy-loading image</h1>
      <LazyLoadImage
        src="https://picsum.photos/id/1080/600/600"
        alt="Strawberries"
      />
    </div>
  );
}
