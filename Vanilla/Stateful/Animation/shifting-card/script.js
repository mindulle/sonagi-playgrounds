const card = document.querySelector('.shifting-card');
const { x, y, width, height } = card.getBoundingClientRect();
const cx = x + width / 2;
const cy = y + height / 2;

const handleMove = e => {
  const { pageX, pageY } = e;
  const dx = (cx - pageX) / (width / 2);
  const dy = (cy - pageY) / (height / 2);
  e.target.style.transform =
    `rotateX(${10 * dy * -1}deg) rotateY(${10 * dx}deg)`;
};

const handleOut = e => {
  e.target.style.transform = 'initial';
};

card.addEventListener('mousemove', handleMove);
card.addEventListener('mouseout', handleOut);
