# Portfolio Chatbot - Aryan Singh
This is a Flask-based personal portfolio + chatbot for **ARYAN SINGH**.

## Features
- Portfolio homepage with projects, skills, education
- Chatbot powered by OpenRouter (deepseek/deepseek-r1)
- Voice input (speech-to-text) and speech output (text-to-speech) in frontend
- Dark/Light theme toggle
- Resume download (static/Aryan.CV.pdf)
- Session-based short memory for chat


## Setup (local)
1. Create a virtualenv and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Set environment variables:
   - `OPENROUTER_API_KEY` - your OpenRouter API key
   - (optional) `FLASK_SECRET_KEY` - secret for Flask sessions
3. Run locally:
   ```bash
   python app.py
   ```
4. Visit http://localhost:5000


## Deploy to Render
1. Push repo to GitHub.
2. Create a new Web Service in Render and connect the repo.
3. Set the build command and start command as in `render.yaml`.
4. Add `OPENROUTER_API_KEY` as an environment variable in Render.
