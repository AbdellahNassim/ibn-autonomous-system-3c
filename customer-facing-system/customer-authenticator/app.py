from flask import Flask, request, jsonify
import os
from utils import setup_logger, check_user, encode_jwt
from database.utils import create_session
from hashlib import sha1
from flask_cors import CORS, cross_origin




app = Flask(__name__)

# set up logger to be used 
logger = setup_logger()

# enable cors to allow access from the intent ingestion
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'




@app.route('/')
def hello():
    return '<h1>Hello From Customer authenticator  </h1>'


@app.route('/auth/login', methods=['POST'])
@cross_origin()
def login_user():
    """
        Api route to allow user to login with credentials 
        returns the jwt token in case of success
    """
    # creating a session to the database
    db = create_session(logger)
    # getting username and password from request 
    json_request = request.get_json()
    if 'username'not in json_request:
        logger.error("Request doesn't include 'username' field ")
    username = json_request['username']
    if 'password'not in json_request:
        logger.error("Request doesn't include 'password' field ")
    password = json_request['password']
    # encrypt password with sha1 to compare with stored password
    enc_password = sha1(bytes(password,'utf-8')).hexdigest()
    # getting user with username and password 
    try:
        user = check_user(logger, db, username, enc_password)
        # encode a jwt token 
        token = encode_jwt(logger, username, enc_password)
        return jsonify({"token":token}), 200
    except Exception as e:
        return jsonify(str(e)), 401




    

port = int(os.environ.get('CUSTOMER_AUTHENTICATOR_PORT', 8080))
app.run(debug=True,threaded=True, host='0.0.0.0', port=port)
