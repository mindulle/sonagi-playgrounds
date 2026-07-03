const ancestors = [
  window,
  document,
  document.documentElement,
  document.body,
  document.getElementById("btn-container")
];

// Target phase
document.querySelector(".btn").addEventListener("click", (e) => {
  console.log(`Hello from ${e.target}`);
});

/* Bubble phase */
ancestors.forEach((a) => {
  a.addEventListener("click", (e) => {
    console.log(`Hello from ${e.currentTarget}`);
  });
});

// Capture phase
ancestors.forEach((a) => {
  a.addEventListener(
    "click",
    (e) => {
      console.log(`Hello from ${e.currentTarget}`);
    },
    true
  );
});

window.addEventListener("click", (e) => {
  if (e.target.className === "btn") console.log("Hello there!");
});
