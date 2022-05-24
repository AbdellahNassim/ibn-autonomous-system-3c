from dotenv import load_dotenv
import logging
import os
import requests
from rdflib import Graph
import json
from flask import Response


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
        format="[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s")
    # set logger name
    log = logging.getLogger("API Gateway")
    # Check if we are in debug mode
    isDebug = bool(os.environ["DEBUG"])
    # by default ignore debug logs
    logging_level = logging.WARNING
    if isDebug:
        logging_level = logging.DEBUG
    log.setLevel(logging_level)
    return log


def validate_intent_format(received_format, data, logger):
    """
        Takes in as input the received format either json or xml for now
        and the received data, verify if the received data is an rdf.

            The function returns none if the intent is invalid and return 
            the intent in json on the other case
        #todo enhance this function to verify if the rdf is an intent 
    """
    if received_format == "json":
        # dump it to a string json
        received_intent_json = json.dumps(data)
        # creating a graph back
        g = Graph()
        # parsing the format
        g.parse(format="json-ld", data=received_intent_json)
        if len(g) == 0:
            return None
        else:
            logger.debug("The received intent in turtle format")
            logger.debug(g.serialize(format="turtle"))
            return data
    # If we are receiving an intent in xml format
    if received_format == "xml":
        # The received intent is in bytes we need to parse it to str
        received_intent = data.decode('utf-8')
        # creating a graph back
        g = Graph()
        # parsing the format
        g.parse(format="xml", data=received_intent)
        if len(g) == 0:
            return None
        else:
            logger.debug("The received intent in turtle format")
            logger.debug(g.serialize(format="turtle"))
            # return the intent in json format
            return json.loads(g.serialize(format="json-ld"))


def forward_intent(intent, logger):
    """
        Forward the intent to the decision making component and return response 
        This function acts like a reverse proxy 
        @params intent the intent in json format 
    """
    # getting the url for the decision making component
    DECISION_MAKING_API = os.environ["DECISION_MAKING_API"]
    logger.info(
        "Sending the received intent back to the decision making component")
    # sending the received intent to the decision making
    decision_making_response = requests.post(
        DECISION_MAKING_API+"/intents", json=intent)
    # As the service acts as a reverse proxy we should exclude the headers
    # About the inner connection details
    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in decision_making_response.raw.headers.items()
               if name.lower() not in excluded_headers]
    logger.info("Returning response back to client ")
    # returning response
    response = Response(decision_making_response.content,
                        decision_making_response.status_code, headers)
    logger.info(response)
    return response
