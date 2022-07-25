
from dotenv import load_dotenv
import logging
import os
from database.models import User
import jwt
import time


def setup_logger():
    """
        This is a simple setup function it load environment variables and
        configure a logger. 
        return@ logger 
    """
    # This will load environment variables from the .env
    load_dotenv()
    # Now we can access those variables like any environment variable
    # configure the logging format
    logging.basicConfig(
        format="[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s ")
    # set logger name
    log = logging.getLogger("Customer Authenticator")
    # Check if we are in debug mode
    isDebug = bool(os.environ["DEBUG"])
    # by default ignore debug logs
    logging_level = logging.WARNING
    if isDebug:
        logging_level = logging.DEBUG
    log.setLevel(logging_level)
    return log


def check_user(logger, db, username, enc_password):
    """
        Checking if a user exists in the database with the specified username and password 
    """
    user = db.query(User).filter(User.username == username,
                                 User.password == enc_password).first()
    if user == None:
        logger.info("Couldn't find user with the specified creds {} {}".format(
            username, enc_password))
        raise Exception(
            "Couldn't find any user with the provided credentials ")
    return user


def encode_jwt(logger, username, enc_password):
    """
        Creating a jwt token based on the username and the encrypted password
    """
    payload = {
        "username": username,
        "password": enc_password,
        "delivery_time": time.time()
    }
    # get the jwt secret
    if 'JWT_SECRET' not in os.environ:
        logger.info("environment variable 'JWT_SECRET' not specified")
        raise Exception("An error occured")
    jwt_secret = os.environ["JWT_SECRET"]
    # create a new jwt token
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    return token
