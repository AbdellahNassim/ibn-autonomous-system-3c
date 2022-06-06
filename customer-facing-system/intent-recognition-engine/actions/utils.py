from dotenv import load_dotenv
import logging
import os
import uuid
from .database.models import *
from .rdf.utils import *
import datetime
import requests
import json

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

def save_intent(session, logger, user_intent):
    # generate unique intent id 
    intent_id = "intent-"+str(uuid.uuid4())[:8]
    logger.info('Generated unique intent id {}'.format(intent_id))
    # get service type by type name 
    service_type = session.query(ServiceType).filter(ServiceType.name==user_intent['service_type']).first()
    if service_type== None:
        raise Exception("Couldn't find a service type with the supplied name")
    logger.info('Found a service type {}'.format(service_type))
    # get user by id 
    user = session.query(User).filter(User.id== user_intent['user_id']).first()
    # if no user found raise exception
    if user== None:
        raise Exception("Couldn't find a user with the supplied id")
    logger.info('Found a user {}'.format(user))
    # create a new service 
    service = Service(type_id=service_type.id)
    # TODO this should be done dynamically
    # In order to allow having multiple services 
    if service_type.name =='video':
        logger.info('Saving the video service parameters')
        # create new video service params 
        video_service_params = VideoServiceParams(service= service,
                                                latency_min=user_intent['latency'], 
                                                resolution=user_intent['resolution'],
                                                )
        # save intent 
        intent = Intent(id=intent_id,
                               user=user,
                               service=service, 
                               request_date=datetime.datetime.now(),
                               delivery_status="REQUESTED"
                                )
        # persisting 
        session.add(service)
        session.add(video_service_params)
        session.add(intent)
        # commit transactions 
        session.commit()
        logger.info('The user intent has been saved successfully')
        # updating the user intent with intent id 
        user_intent['id'] = intent_id

        



def send_intent_backend(logger, user_intent):
    """
        Takes in the user extracted intent, map it into a standard format 
        and send it to the backend system
    """
    standard_intent = standardize_intent(logger, user_intent)
    if "BACKEND_URL" not in os.environ:
        raise Exception("Environment variable $BACKEND_URL was not set ")
    backend_url = os.environ["BACKEND_URL"]
    # send intent to backend service 
    logger.info("Sending standardized intent to backend "+backend_url)
    standard_intent = json.loads(standard_intent)
    response = requests.post(backend_url,json=standard_intent)
    if response.status_code !=200:
        raise Exception(f"An error occurred while sending the intent {response.status_code} was received")
    logger.info("Intent sent successfully ")

