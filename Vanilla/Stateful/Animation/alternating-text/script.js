const texts = ["Java", "Python", "C", "C++", "C#", "Javascript"];
const element = document.getElementById("alternating-text");

let i = 0;
const listener = (e) => {
  i = i < texts.length - 1 ? i + 1 : 0;
  element.innerHTML = texts[i];
};

element.innerHTML = texts[0];
element.addEventListener("animationiteration", listener, false);
