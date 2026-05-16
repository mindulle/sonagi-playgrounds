/**
 * Get the closest parent up the DOM tree that matches against a selector.
 * The Element.closest() method starts with the element itself.
 * You can start with the first parent element by pairing it with the Node.parentNode property.
 */
let h1 = document.querySelector("h1");

// returns the .hero element
let hero = h1.closest(".hero");

// returns the h1 element itself
let sandwich = h1.closest("[data-sandwich]");

// Start with the element's parent
// returns null
let sandwich2 = h1.parentNode.closest("[data-sandwich]");

console.warn(hero);
console.warn(sandwich);
console.warn(sandwich2);
