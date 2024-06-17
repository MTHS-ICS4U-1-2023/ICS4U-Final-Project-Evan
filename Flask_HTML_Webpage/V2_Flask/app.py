#!/usr/bin/env python3
"""
Created by: Evan Beaudoin
Created on: May 2024
This is the Record Audio module
"""

from flask import Flask, render_template, request, send_from_directory
import os
from datetime import datetime
import wave

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['POST'])
def record():
    if 'audio_data' in request.files:
        audio_data = request.files['audio_data']
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'recording_{timestamp}.wav'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with wave.open(filepath, 'wb') as f:
            f.setnchannels(1)  # Mono
            f.setsampwidth(2)  # Sample width in bytes
            f.setframerate(44100)  # Frame rate
            f.writeframes(audio_data.read())
        return {'filename': filename}
    return {'error': 'No audio data received'}, 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
