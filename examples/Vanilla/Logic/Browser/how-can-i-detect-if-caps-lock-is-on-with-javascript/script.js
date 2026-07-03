const el = document.getElementById("password");
const msg = document.getElementById("password-message");

el.addEventListener("keyup", (e) => {
  msg.style = e.getModifierState("CapsLock")
    ? "display: block"
    : "display: none";
});
