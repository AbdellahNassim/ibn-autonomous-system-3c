import time
from database.models import ServicesCatalog
from database.utils import create_session

def process_intent(name, queue, logger):
    """
        Main function of the decision maker. 
        It loops on the queue until getting an item 
    """
    while True: 
        try:
            if not queue.empty():
                # getting intent from the queue
                intent = queue.get()
                logger.info("Intent will be processed by {}".format(name))
                # decide on the service to deploy
                service = decide_service(logger, intent['service_type'])
            # sleep for one second in order to save some resources
            # this will help minimizing the number of time the loop is executed 
            time.sleep(1)
        except Exception as e:
            logger.exception(e)
            


def decide_service(logger, service_type):
    """
        Function to decide on the service to be used for the intent.
        #TODO The implementation of the function is just checking the service catalog but can be further improved
        return @service The service description params (repository and chartName)
    """
    # create a new connection 
    session = create_session(logger)
    # fetch service descriptors from service catalog
    query_result = session.query(ServicesCatalog).filter(ServicesCatalog.service_type==service_type).first()
    if query_result is None:
        raise Exception("Service type {} not supported ".format(service_type))
    # close session 
    session.close()
    return query_result




def fetch_model_marketplace(logger, intent):
    """
        Fetching appropriate ml model from the SCORING ML marketplace. 
        Each service can have it's own ml model. 
        return @model the ML model 
    """
    # fetch model 


def execute_model_intent_params(logger, model, intent):
    """
        Execute ml model with the supplied intent parameters.
        return @resources The predicted resources for the supplied service params
    """
    # run ml model 


def generate_deploy_decision(service, resources ):
    """
        Generate Deployment decision and send to the policy generator
    """
    # generate decision 