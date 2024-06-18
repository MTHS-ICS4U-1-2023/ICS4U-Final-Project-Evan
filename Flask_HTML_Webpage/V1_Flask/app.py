#!/usr/bin/env python3
"""
Created by: Evan Beaudoin
Created on: May 2024
This is the "Hello, World!" module
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)