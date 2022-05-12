# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, ActiveLoop
from .utils import setup
from .database import create_connection
class ActionProcessIntent(Action):
    """
        This class is an action that will be executed once the intent has been identified
        It gets the extracted entities and compose an intent and then save it. 
    """
    
    def name(self) -> Text:
        return "action_process_intent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # get logger
        logger = setup()
        logger.debug("Received Action to process intent")
        # connect to database
        create_connection(logger)
        # get values from the tracker
        user_intent = {
            "service_type":tracker.get_slot('service'),
            "latency":tracker.get_slot('latency'),
            "resolution":tracker.get_slot('resolution')
        }

        dispatcher.utter_message(text="Hello World!")
        return []
class ActionCustomizeVideoService(Action):
    """
        This class is an action that just clean up the slots reserved for the 
        video service parameters
    """
    
    def name(self) -> Text:
        return "action_customize_video_service"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Once the user wants to customize it's service we need to 
        # reinitialize all the default values 
        # reinitialize_latency = SlotSet("latency",None )
        # reinitialize_resolution =  SlotSet("resolution",None) 
        # Launch the form 
        start_form = FollowupAction("video_service_params_form")
        return [SlotSet("latency",None ),
                SlotSet("resolution",None) ,
                start_form ]