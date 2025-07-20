from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import speech_recognition as sr
from pydub import AudioSegment
from textblob import TextBlob
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400

    audio_file = request.files['audio']
    audio_path = "temp_audio.wav"
    audio_file.save(audio_path)

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            sentiment = TextBlob(text).sentiment.polarity
            return jsonify({'text': text, 'sentiment': sentiment})
        except sr.UnknownValueError:
            return jsonify({'error': 'Could not understand audio'}), 400
        except sr.RequestError:
            return jsonify({'error': 'API unavailable'}), 500

if __name__ == '__main__':
    app.run()
