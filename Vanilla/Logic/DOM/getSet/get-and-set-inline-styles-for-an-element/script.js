/**
 * Get and set inline styles for an element.
 */

let sandwich = document.querySelector("#sandwich");

// Get a style
// If this style is not set as an inline style directly on the element, it returns an empty string
let bgColor = sandwich.style.backgroundColor; // this will return "green"
let fontWeight = sandwich.style.fontWeight; // this will return ""

// Set the background-color style property
sandwich.style.backgroundColor = "purple";

/**
 * You can also get and set a string representation of the entire inline style property
 * on the element itself with the Element.style.cssText property.
 */

// Get the styles on an element
// returns "background-color: green; color: white;"
let styles = sandwich.style.cssText;

// Completely replace the inline styles on an element
sandwich.style.cssText = "font-size: 2em; font-weight: bold;";

// Add additional styles
sandwich.style.cssText += "color: purple;";
