const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');
const micBtn = document.getElementById('mic-btn');

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });

// Function to append messages with animation
function appendMessage(role, text) {
  const msgDiv = document.createElement('div');
  msgDiv.classList.add(role);
  msgDiv.textContent = text;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Add typing animation
function showTyping() {
  const typingDiv = document.createElement('div');
  typingDiv.classList.add('bot');
  typingDiv.innerHTML = `<div class="typing"><span></span><span></span><span></span></div>`;
  chatBox.appendChild(typingDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
  return typingDiv;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage('user', message);
  userInput.value = '';

  const typingDiv = showTyping();

  try {
    const response = await fetch('/get_response', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    typingDiv.remove();
    appendMessage('bot', data.reply);
    speakText(data.reply);
  } catch (err) {
    typingDiv.remove();
    appendMessage('bot', '⚠️ Error connecting to server.');
  }
}

// Text to speech
function speakText(text) {
  if (!('speechSynthesis' in window)) return;
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = 'en-US';
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utter);
}

// Optional: glowing mic visual pulse
if (micBtn) {
  micBtn.addEventListener('click', () => {
    micBtn.classList.add('pulse');
    setTimeout(() => micBtn.classList.remove('pulse'), 1000);
  });
}
