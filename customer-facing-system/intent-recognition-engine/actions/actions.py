# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os 
from .utils import setup
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
        logger.error("Received Action to process intent")
        print(tracker)
        print(domain)
        print(dispatcher)
        dispatcher.utter_message(text="Hello World!")

        return []
