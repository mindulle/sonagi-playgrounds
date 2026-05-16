/**
 * Create a copy of a node. Call on the node to clone.
 * If you want all of a node’s child nodes to also be copied,
 * pass in true as an argument.
 */

// returns <div id="app" class="background" data-app>
let app = document.querySelector("#app");

// Create a shallow clone
// returns <div id="app" class="background" data-app></div> as an empty node
let clone = app.cloneNode();

// Create a deep clone
// returns <div id="app" class="background" data-app></div> with the h1, p, and text nodes
let deepClone = app.cloneNode(true);
