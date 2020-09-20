from flask import Flask, jsonify, request
from datetime import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://mongoadmin:secret@localhost:27017/?authSource=admin')
db = client.sampleDB

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.now()
    })

@app.route('/mongo', methods=['GET'])
def getPosts():
    posts = db.posts
    post = posts.find_one()
    return jsonify(post)

@app.route('/mongo', methods=['POST'])
def addPost():
    posts = db.posts
    json = request.get_json()
    posts.insert_one(json)
    return jsonify({"status": "ok"})
