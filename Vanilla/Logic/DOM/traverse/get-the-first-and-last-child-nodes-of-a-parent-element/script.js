/**
 * Get the first and last child nodes of a parent element,
 * including nodes that aren’t elements (such as comments and text fragments).
 */

let wizards = document.querySelector("ul");

// returns the comment node <!-- The gray wizard -->
let firstDescendant = wizards.firstChild;

// returns <li>Neville</li>
let lastDescendant = wizards.lastChild;

console.warn(firstDescendant);
console.warn(lastDescendant);
