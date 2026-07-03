/**
 * Insert one or more elements or strings at the beginning of a set elements inside a shared parent.
 *  Call the Element.prepend() method on the target node,
 * and pass in one or more new elements or strings as arguments.
 */

// Create a new element
let li = document.createElement("li");
li.textContent = "I am new here.";

// Create another new element
let liToo = document.createElement("li");
liToo.textContent = `I'm new, too!`;

// Get the parent node
let list = document.querySelector("#list");

// Insert the new node before the first element in the parent node
// <li>I am new here.</li><li>Item 1</li>...
list.prepend(li);

// You can inject more than one item by passing in multiple arguments
// <li>I am new here.</li><li>I'm new, too!</li><li>Item 1</li>...
list.prepend(li, liToo);
