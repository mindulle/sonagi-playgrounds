/**
 * Returns a live HTMLCollection,
 * which means if items are added to it later,
 * the collection updates as well.
 */

let wizards = document.querySelector(".wizards");
let wizardsList = document.querySelector(".wizards ul");

// returns an HTMLCollection with the ul element
let wizardDescendants = wizards.children;

// returns an HTMLCollection with the list items
let wizardListDescendants = wizardsList.children;

// Add a new item
let li = document.createElement("li");
li.textContent = "Merlin";
wizardsList.append(li);

// wizardListDescendants now automatically contains the new li
