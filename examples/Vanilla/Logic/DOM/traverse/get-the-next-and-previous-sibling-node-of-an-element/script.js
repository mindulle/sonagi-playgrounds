/**
 * Get the next and previous sibling node of an element,
 * including nodes that aren’t elements (such as comments and text fragments).
 */

let hermione = document.querySelector("#hermione");

// returns <!-- The surprise hero -->
let next = hermione.nextSibling;

// returns <li>Radagast</li>
let previous = hermione.previousSibling;

console.warn(next);
console.warn(previous);
