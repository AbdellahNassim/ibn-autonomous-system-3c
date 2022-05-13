from dotenv import load_dotenv
import logging
import os
import uuid
from .database.models import *
import datetime

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
    intent_id = str(uuid.uuid4())
    logger.info(f'Generated unique intent id {intent_id}')
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
    intent_service = IntentService(type_id=service_type.id)
    # TODO this should be done dynamically
    if service_type.name =='video':
        logger.info('Saving the video service parameters')
        # create new video service params 
        video_service_params = VideoServiceParams(intent_service= intent_service,
                                                latency_min=user_intent['latency'], 
                                                resolution=user_intent['resolution'],
                                                )
        # save intent 
        intent = Intent(id=intent_id,
                               user=user,
                               service=intent_service, 
                               request_date=datetime.datetime.now(),
                               delivery_status="REQUESTED"
                                )
        # persisting 
        session.add(intent_service)
        session.add(video_service_params)
        session.add(intent)
        # commit transactions 
        session.commit()
        # close session
        session.close()
        
