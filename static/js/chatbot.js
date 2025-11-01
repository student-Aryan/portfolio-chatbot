const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');
const micBtn = document.getElementById('mic-btn');

sendBtn.addEventListener('click', sendMessage);
if(userInput) userInput.addEventListener('keypress', e => { if(e.key === 'Enter') sendMessage(); });

function appendMessage(cls, text){
  const d = document.createElement('div');
  d.className = cls;
  d.textContent = text;
  chatBox.appendChild(d);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(){
  const msg = userInput.value.trim();
  if(!msg) return;
  appendMessage('user', msg);
  userInput.value = '';
  try{
    const res = await fetch('/get_response', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({message: msg})
    });
    const data = await res.json();
    appendMessage('bot', data.reply);
    // speak reply
    speakText(data.reply);
  }catch(e){
    appendMessage('bot', 'Error: could not reach server.');
  }
}

// Text to Speech using Web Speech API
function speakText(text){
  if(!('speechSynthesis' in window)) return;
  const ut = new SpeechSynthesisUtterance(text);
  ut.lang = 'en-US';
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(ut);
}

// Speech to Text (microphone)
let recognition = null;
if('webkitSpeechRecognition' in window || 'SpeechRecognition' in window){
  const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new Rec();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  recognition.onresult = (e) => {
    const t = e.results[0][0].transcript;
    userInput.value = t;
    sendMessage();
  };
  recognition.onerror = (e) => { console.error('Speech error', e); };
} else {
  if(micBtn) micBtn.style.display = 'none';
}

if(micBtn){
  micBtn.addEventListener('click', ()=>{
    if(!recognition) return;
    recognition.start();
  });
}
