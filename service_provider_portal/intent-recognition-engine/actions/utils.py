from dotenv import load_dotenv
import logging
import os
import datetime
import requests

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
    logging.basicConfig(format="[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s")
    # set logger name 
    log = logging.getLogger("Action Server")
    # Check if we are in debug mode 
    isDebug = bool(os.environ["DEBUG"])
    # by default ignore debug logs
    logging_level = logging.WARNING
    if isDebug:
        logging_level = logging.DEBUG
    log.setLevel(logging_level)
    return log



def send_entities(logger, user_intent):
    """
        Send the extracted entities to the intent in order to be formulated
    """
    # check if the url of intent owner was set 
    if 'INTENT_OWNER_URL' not in os.environ:
        raise Exception("Environment Variable 'INTENT_OWNER_URL' not set")
    intent_owner_url = os.environ['INTENT_OWNER_URL']
    # sending post request to the intent owner 
    response = requests.post(intent_owner_url+'/intents', json=user_intent)
    if response.status_code != 200:
        raise Exception("An uknown error occurred while sending the extracted entities")
    logger.info("Request sent and received {}".format(response.raw))
