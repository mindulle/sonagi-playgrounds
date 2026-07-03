/**
 * Get the immediate descendants of an element,
 * including text fragments and other non-element nodes.
 */

let wizards = document.querySelector("ul");

// returns all nodes, including the comments
let descendants = wizards.childNodes;

console.warn(descendants);
