import json
from rdf_utils.utils import format_to_graph, map_rdf_intent
from rdflib import Literal
import os 

def handle_intent(logger, intent):
    """
        Handle the received intent. This function will take care of saving the intent 
        And  map it to be scheduled
    """
    logger.info("Intent Received successfully to be handled")
    # format the intent
    intent_graph = format_intent(logger, intent)
    # save the intent 
    save_intent(logger, intent_graph)


def format_intent(logger,intent):
    """
        Format the intent into an rdf graph to be saved. Log the intent in a human readable
        format. 
    """
    # stringify the received json intent 
    intent_string = json.dumps(intent)
    # Format the intent and log it 
    graph = format_to_graph(logger, intent_string)
    map_rdf_intent(logger, graph)
    return graph




def save_intent(logger, intent_graph):
    """
        Save the intent in order to be tracked later
    """
    
