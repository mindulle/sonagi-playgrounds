/**
 * Insert elements and strings after another element.
 * Call the Node.after() method on the node you want to insert after,
 * and pass in one or more new elements or strings as arguments.
 */

// Create a new element
let p = document.createElement("p");
p.textContent = "Hello!";

// Get the target node
let app = document.querySelector("#app");

// Insert the new node after the target node
// <div id="app">Good morning</div><p>Hello!</p>
app.after(p);

// You can inject more than one item by passing in multiple arguments
// <div id="app">Good morning</div><p>Hello!</p>What's poppin'
app.after(p, `What's poppin?`);
