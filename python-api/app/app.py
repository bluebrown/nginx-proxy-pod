from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def root():
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.now()
    })

