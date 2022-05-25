import json
from rdf_utils.utils import format_to_graph, map_rdf_intent
from database.utils import create_session
from database.models import IntentTracker, IntentStatus
from components.intent_scheduler import schedule_processing
import os 

def handle_intent(logger,queue, intent):
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
    # schedule the processing of the intent 
    schedule_processing(logger, queue, result_intent)


def format_intent(logger,intent):
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
    intent_tracker = IntentTracker(id=intent_id,intent_rdf=intent_graph.serialize(format="turtle"), status=IntentStatus.IN_PROGRESS)
    db_session.add(intent_tracker)
    db_session.commit()
    logger.info("Intent saved successfully")
    
