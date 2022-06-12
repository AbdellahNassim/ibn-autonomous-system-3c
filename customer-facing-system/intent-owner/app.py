from flask import Flask, request, jsonify
import os
from utils import setup_logger, save_intent, send_intent_backend
from database.utils import create_session
from hashlib import sha1



app = Flask(__name__)

# set up logger to be used 
logger = setup_logger()





@app.route('/')
def hello():
    return '<h1>Hello From Intent Owner  </h1>'


@app.route('/intents', methods=['POST'])
def create_new_intent():
    """
       Api route to allow the creation of a new intent based on the extracted 
       entities. 
       This function receives the extracted entities from the recognition module
       it saves the user intent in the intent store, it then formulate it in the 
       standard format to be sent to the backend system 
    """
    user_intent = request.get_json()
    # TODO Fixing hardcoded user id 
    # TODO The user id should be sent jointly with the other params    
    user_intent['user_id'] = 1

    # connect to database and create a session
    session = create_session(logger)
    # save the intent in the intent store 
    try:
        save_intent(session, logger, user_intent)
        # once the intent saved in intent store
        # we send it to be deployed
        send_intent_backend(logger, user_intent)
        return jsonify("Operation succeeded"), 200
    except Exception as e:
        logger.error(str(e))
        return jsonify("An error occured"), 500




    

port = int(os.environ.get('INTENT_OWNER_PORT', 8080))
app.run(debug=True,threaded=True, host='0.0.0.0', port=port)
