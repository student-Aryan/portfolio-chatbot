from flask import Flask, render_template, request, jsonify, session, send_file
import os, json

# -----------------------------
# Flask App Initialization
# -----------------------------
app = Flask(__name__)

# ✅ Secret Key for session management
# Uses Render environment variable if available, else fallback
app.secret_key = os.environ.get("SECRET_KEY", "aryan_super_secret_key_12345")

# -----------------------------
# Home Route - Portfolio Page
# -----------------------------
@app.route('/')
def home():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, 'data', 'aryan_data.json')

        # ✅ Load JSON data safely
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle accidental list wrapping
        if isinstance(data, list) and len(data) > 0:
            data = data[0]

        projects = data.get("projects", [])
        contact = {
            "linkedin": data.get("linkedin", ""),
            "github": data.get("github", ""),
            "leetcode": data.get("leetcode", ""),
            "resume": "/download_resume"
        }

        return render_template('index.html', data=data, projects=projects, contact=contact)

    except Exception as e:
        return f"Error loading portfolio data: {e}", 500


# -----------------------------
# Chatbot Page Route
# -----------------------------
@app.route('/chat')
def chat():
    try:
        # Initialize chat history session
        if 'chat_history' not in session:
            session['chat_history'] = []

        return render_template('chatbot.html')

    except Exception as e:
        return f"Error loading chatbot page: {e}", 500


# -----------------------------
# Chatbot API Endpoint
# -----------------------------
@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_message = request.json.get('message', '').strip()

        if not user_message:
            return jsonify({"reply": "Please type a message to start the chat 🤖"}), 400

        # Append to session chat history
        if 'chat_history' not in session:
            session['chat_history'] = []

        session['chat_history'].append({"user": user_message})

        # ✅ Temporary dummy chatbot reply
        reply = f"Hi, I'm Aryan's Chatbot 🤖 — you said: {user_message}"

        # Append bot response to chat history
        session['chat_history'].append({"bot": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500


# -----------------------------
# Resume Download Route
# -----------------------------
@app.route('/download_resume')
def download_resume():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        resume_path = os.path.join(base_dir, 'data', 'Aryan.CV.pdf')

        if not os.path.exists(resume_path):
            return "Resume file not found.", 404

        return send_file(resume_path, as_attachment=True)

    except Exception as e:
        return f"Error while downloading resume: {e}", 500


# -----------------------------
# Run App (for local testing)
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
