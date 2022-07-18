from flask import Flask, request, jsonify
import os
from utils import setup_logger


app = Flask(__name__)

# set up logger to be used 
logger = setup_logger()



@app.route('/')
def hello():
    return '<h1>Hello From Intent Monitor Component</h1>'


    

port = int(os.environ.get('INTENT_MANAGER_PORT', 8080))
app.run(debug=True,threaded=True, host='0.0.0.0', port=port)
