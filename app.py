from flask import Flask, render_template, request, jsonify, send_from_directory, session
import json, os, requests
from pathlib import Path

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'change_this_to_secure_random_value')

BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / 'data' / 'aryan_data.json', 'r', encoding='utf-8') as f:
        aryan_data = json.load(f)

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', 'YOUR_API_KEY_HERE')
MODEL = "deepseek/deepseek-r1"

@app.route('/')
def home():
        return render_template('index.html', data=aryan_data)

@app.route('/chat')
def chat():
        # initialize session chat cache (last 10 messages)
        if 'chat_history' not in session:
            session['chat_history'] = []
        return render_template('chatbot.html', data=aryan_data)

@app.route('/get_response', methods=['POST'])
def get_response():
        user_msg = request.json.get('message', '')
        # keep session-based short memory
        history = session.get('chat_history', [])
        history.append({'role': 'user', 'content': user_msg})
        # keep only last 8
        history = history[-8:]
        # Build system prompt with data context
        system_prompt = f"""You are Aryan Singh's personal portfolio assistant. Use the structured data provided to answer questions about Aryan's skills, education, experience, projects, and certifications. Be concise, professional, and helpful.
Data: {json.dumps(aryan_data)}"""

        messages = [{'role': 'system', 'content': system_prompt}]
        # add short memory
        for item in history:
            messages.append(item)
        # last user message is included already
        messages.append({'role': 'user', 'content': user_msg})

        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': MODEL,
            'messages': messages,
            'temperature': 0.2
        }

        # call OpenRouter Chat Completions
        try:
            r = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=payload, timeout=20)
            r.raise_for_status()
            j = r.json()
            reply = j['choices'][0]['message']['content']
        except Exception as e:
            reply = 'Sorry — I could not reach the AI service. ' + str(e)

        # update session history
        history.append({'role': 'assistant', 'content': reply})
        session['chat_history'] = history[-20:]
        return jsonify({'reply': reply})

@app.route('/download_resume')
def download_resume():
        return send_from_directory('static', 'Aryan.CV.pdf', as_attachment=True)

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)
