from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form['text']
    try:
        response = openai.audio.speech.create(
            model="tts-1-hd",
            voice="onyx",
            input=text
        )
        audio_path = "static/voice.mp3"
        with open(audio_path, "wb") as f:
            f.write(response.read())
        return render_template('index.html', audio_file='static/voice.mp3')
    except Exception as e:
        return render_template('index.html', error=f"TTS Error: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
