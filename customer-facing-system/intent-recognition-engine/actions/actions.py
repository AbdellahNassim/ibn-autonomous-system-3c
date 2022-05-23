from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, ActiveLoop
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from .utils import setup_logger, save_intent, send_intent_backend
from .database.utils import create_session

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
        logger = setup_logger()
        logger.info("Received Action to process intent")
        # connect to database and create a session
        session = create_session(logger)
        # get values from the tracker
        user_intent = {
            "service_type":tracker.get_slot('service'),
            "latency":tracker.get_slot('latency'),
            "resolution":tracker.get_slot('resolution'),
            # This is just a mockup until we implement the user authentication
            # TODO 
            "user_id":1
        }
        # save the intent in the intent store 
        try:
            save_intent(session, logger, user_intent)
            # once the intent saved in intent store
            # we send it to be deployed
            send_intent_backend(user_intent)
            dispatcher.utter_message(response='utter_service_will_be_deployed')
        except Exception as e:
            logger.error(str(e))
            dispatcher.utter_message(text="We are sorry an error has occured")
        
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
        # Launch the form 
        start_form = FollowupAction("video_service_params_form")
        return [SlotSet("latency",None ),
                SlotSet("resolution",None) ,
                start_form ]

# This class will ensure the validation of video service parameters
class ValidateRestaurantForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_video_service_params_form"

    # Validate latency 
    def validate_resolution(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate latency value."""
        try:
            latency = int(slot_value)
            return {"latency": slot_value}
        except:
           return {"latency": None} 

    # Validate the resolution
    def validate_resolution(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate resolution value."""
        # We will check if the value extracted is in the resolutions we have 
        if slot_value in domain["slots"]["resolution"]["values"]:
            return {"resolution": slot_value}
        else:
            return {"resolution": None}

            