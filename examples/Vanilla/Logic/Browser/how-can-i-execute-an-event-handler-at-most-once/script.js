/* original jquery api.
$("#my-btn").one("click", () => {
  console.log("Hello!"); // 'Hello!' will only be logged on the first click
});
*/

const listenOnce = (el, evt, fn) => {
  let fired = false;
  el.addEventListener(evt, (e) => {
    if (!fired) fn(e);
    fired = true;
  });
};

listenOnce(document.getElementById("my-btn"), "click", () =>
  console.log("Hello!")
); // 'Hello!' will only be logged on the first click

const newListenOnce = (el, evt, fn) =>
  el.addEventListener(evt, fn, { once: true });

newListenOnce(document.getElementById("my-btn"), "click", () =>
  console.log("Hello!")
); // 'Hello!' will only be logged on the first click
