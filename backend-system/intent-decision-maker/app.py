from flask import Flask, request, jsonify
import os
app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello From Intent Decision Maker  </h1>'


@app.route('/intents', methods=['POST'])
def process_intent():
    print(request.get_json())
    return jsonify('Intent received successfully')


port = int(os.environ.get('PORT', 8000))
app.run(debug=True, host='0.0.0.0', port=port)
