import json
from rdf_utils.utils import format_to_graph, map_rdf_intent
from database.utils import create_session
from database.models import IntentTracker, IntentStatus
from components.intent_scheduler import schedule_processing
import os
import requests


def handle_intent(logger, queue, intent):
    """
        Handle the received intent. This function will take care of saving the intent 
        And  map it to be scheduled
    """
    logger.info("Intent Received successfully to be handled")
    # create an rdf graph from the received intent
    intent_graph = format_intent(logger, intent)
    # extract values from the graph and map them to a dict
    result_intent = map_rdf_intent(logger, intent_graph)
    # save the intent to be tracked
    save_intent(logger, result_intent['id'], intent_graph)
    # save intent in the graphdb
    save_intent_graphdb(logger, intent_graph)
    # schedule the processing of the intent
    schedule_processing(logger, queue, result_intent)


def format_intent(logger, intent):
    """
        Format the intent into an rdf graph to be saved. Log the intent in a human readable
        format. 
    """
    # stringify the received json intent
    intent_string = json.dumps(intent)
    # Format the intent and log it
    graph = format_to_graph(logger, intent_string)
    return graph


def save_intent(logger, intent_id, intent_graph):
    """
        Save the intent in order to be tracked later
    """
    # create session to the db
    db_session = create_session(logger)
    logger.info("Saving intent with id {}".format(intent_id))
    # Create a new intent to be tracked
    intent_tracker = IntentTracker(id=intent_id, intent_rdf=intent_graph.serialize(
        format="turtle"), status=IntentStatus.IN_PROGRESS)
    db_session.add(intent_tracker)
    db_session.commit()
    db_session.close()
    logger.info("Intent saved successfully")


def save_intent_graphdb(logger, intent_graph):
    # get graphdb url
    graphdb_url = os.environ['KNOWLEDGE_DB_URL']
    # check if repository is created
    response = requests.get(graphdb_url + '/rest/repositories')
    if response.status_code != 200:
        logger.error('Error accessing the intent tracker db')
        return
    if len(response.json()) == 0:
        # files
        files = {
            'config': open('repo-config.ttl', 'rb'),
        }
        # create a new repository
        response = requests.post(graphdb_url+'/rest/repositories', files=files)
        if response.status_code != 201:
            logger.error('Error creating repository in the intent tracker db')
            return
    # send the intent to the knowledge graph
    headers = {
        "Content-Type": "application/x-turtle"
    }
    resp = requests.post(
        graphdb_url+'/repositories/intent-tracker/statements', headers=headers, data=intent_graph.encode())
    if response.status_code != 204:
        logger.error('Error sending intent to the intent tracker db')
        return
