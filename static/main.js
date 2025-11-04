// === Typing Animation for Hero Section ===
document.addEventListener("DOMContentLoaded", () => {
  const typingText = document.getElementById("typing-text");
  const textToType = "Aspiring AI Engineer | Machine Learning Developer | Python Enthusiast";
  let index = 0;

  function typeEffect() {
    if (index < textToType.length) {
      typingText.textContent += textToType.charAt(index);
      index++;
      setTimeout(typeEffect, 80);
    }
  }

  if (typingText) {
    typeEffect();
  }
});
