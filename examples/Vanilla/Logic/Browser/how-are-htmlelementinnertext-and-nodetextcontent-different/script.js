const greeting = document.getElementById('greeting');

greeting.innerText; // "Hi there! My name is Bubbles."
greeting.textContent; // "Hi there! My name is Bubbles."

greeting.innerText = 'Hello!'; // <p id="greeting">Hello!</p>
greeting.textContent = 'Hi!'; // <p id="greeting">Hi!</p>

const card = document.querySelector('.card');

card.innerText;
/*
"Hi there!
My name is BUBBLES."
*/

card.textContent;
/*
"

    p { color: red; }
    strong { text-transform: uppercase; }
    small { display: none; }

  Hi   there!My name is Bubbles.
  And I'm a dog.
"
*/
