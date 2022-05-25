from flask import Flask, request, jsonify
import os
from utils import setup_logger
from components.intent_handler import handle_intent
from components.intent_scheduler import setup_queue, setup_workers
import atexit
import threading

app = Flask(__name__)

# set up logger to be used 
logger = setup_logger()

# setting up the queue
queue = setup_queue(logger)

# launching the workers 
workers = setup_workers(logger, queue)

@app.route('/')
def hello():
    return '<h1>Hello From Intent Decision Maker  </h1>'


@app.route('/intents', methods=['POST'])
def process_intent():
    # receive the intent in json format 
    received_intent = request.get_json()
    # pass the received intent to the intent handler
    handle_intent(logger, queue, received_intent)
    return jsonify('Intent received successfully')



# define function
@atexit.register
def cleanup():
    """
        Stop the tasks of decision maker
        This will be called once the server exit
    """
    logger.info("Shutting down all the workers")
    for worker in workers:
        worker.join()
    

port = int(os.environ.get('PORT', 8000))
app.run(debug=True,threaded=True, host='0.0.0.0', port=port)
