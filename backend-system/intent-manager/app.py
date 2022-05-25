from flask import Flask, request, jsonify
import os
from utils import setup_logger
from components.intent_handler import handle_intent
app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello From Intent Decision Maker  </h1>'


@app.route('/intents', methods=['POST'])
def process_intent():
    logger = setup_logger()
    # receive the intent in json format 
    received_intent = request.get_json()
    # pass the received intent to the intent handler
    handle_intent(logger, received_intent)
    return jsonify('Intent received successfully')


port = int(os.environ.get('PORT', 8000))
app.run(debug=True, host='0.0.0.0', port=port)
