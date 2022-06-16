import time
from database.models import ServicesCatalog
from database.utils import create_session
import requests
import os
import tempfile
from tensorflow import keras
from utils import map_resolution
import numpy as np


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
                # fetching appropriate ml model
                ml_model_file = fetch_model_marketplace(logger, intent)
                # use keras to load model
                ml_model = keras.models.load_model(ml_model_file.name)
                # use the model to make predictions
                predictions = execute_model_intent_params(
                    logger, ml_model, intent)
                # generating decisions now
                generate_deploy_decision(logger, service, intent, predictions)
            # sleep for one second in order to save some resources
            # this will help minimizing the number of time the loop is executed
            time.sleep(1)
        except Exception as e:
            logger.exception(e)


def decide_service(logger, service_type):
    """
        Function to decide on the service to be used for the intent.
        # TODO The implementation of the function is just checking the service catalog but can be further improved
        return @service The service description params (repository and chartName)
    """
    # create a new connection
    session = create_session(logger)
    # fetch service descriptors from service catalog
    query_result = session.query(ServicesCatalog).filter(
        ServicesCatalog.service_type == service_type).first()
    if query_result is None:
        raise Exception("Service type {} not supported ".format(service_type))
    # close session
    session.close()
    return query_result


def fetch_model_marketplace(logger, intent):
    """
        Fetching appropriate ml model from the SCORING ML marketplace.
        Each service can have it's own ml model.
        First the ML marketplace will be queried to search model and once a model got,
        The ML marketplace is queried again to get the model in raw format. We will then save
        it in a temporary file to be used directly.
        return @model file  the ML model
    """
    # search for appropriate model first
    # mapping service params to model inputs
    model_inputs = []
    for param, value in intent["service_params"].items():
        model_inputs.append(param)
    data = {
        "service": intent['service_type'],
        "input": model_inputs,
        "output": ['cpu', 'memory', 'network', 'storage'],
        "is_trained": True,
        "format": "h5"
    }
    logger.info(data)
    # sending search request for model
    response = requests.get(
        os.environ['ML_MARKET_PLACE_HOST']+'/models/search', json=data)
    if response.status_code != 200:
        logger.error(response.raw)
        raise Exception('Error searching ml model from ml marketplace')
    else:
        # We have now received a search result
        search_result = response.json()
        logger.info(search_result)
        # get the model id to be used to fetch model
        model_id = search_result['model_id']

        logger.info(
            'Search resulted successfully, model with id {} will be fetched'.format(model_id))
        # now get the model
        response = requests.get(
            os.environ['ML_MARKET_PLACE_HOST']+'/models/'+model_id)
        if response.status_code != 200:
            # in case of errors in the request reporting the error
            logger.error(response.raw)
            raise Exception('Error Getting model with {}'.format(model_id))
        else:
            logger.info("Model fetched successfully")
            # getting the raw content of the model
            model = response.content
            # creating a temporary file
            temp = tempfile.NamedTemporaryFile()
            # writing content to that temp file
            temp.write(model)
            return temp


def execute_model_intent_params(logger, model, intent):
    """
        Execute ml model with the supplied intent parameters.
        return @resources The predicted resources for the supplied service params
    """
    # normalize the parameters
    # TODO this should be done in different manner
    model_input = []
    logger.info("Executing model to make predictions on the needed resources")
    for param, value in intent["service_params"].items():
        try:
            model_input.append(int(value))
        except:
            model_input.append(map_resolution(value))
    # map it to a numpy array
    model_input = np.asarray([model_input])
    # make predictions
    results = np.rint(model.predict(model_input))
    mapped_results = {
        "cpu": 1400,
        "memory": 1500,
        "network": 60,
        "storage": int(results[0][3]),
    }
    logger.info("Predicted resources are as follow {}".format(mapped_results))
    return mapped_results


def generate_deploy_decision(logger, service, intent, resources):
    """
        Generate Deployment decision and send to the policy generator
    """
    # generate decision
    decision = {
        "decision": "DEPLOYMENT_DECISION",
        "intent-id": intent['id'],
        "params": {
            "service": {
                "name": service.service_name,
                "repository": service.service_repository,
                "repository_url": service.service_repository_url
            },
            "resources": resources,
        }
    }
    logger.info('Generating decision {}'.format(decision))
    # sending the decision to the policy generator
    response = requests.post(
        os.environ["POLICY_GENERATOR_HOST"]+"/decisions", json=decision)
    if response.status_code != 200:
        # in case of errors in the request reporting the error
        logger.error(response.raw)
        raise Exception('Error Sending decision to the policy generator ')
    else:
        logger.info("Decision sent successfully")
