from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, ActiveLoop
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from .utils import setup_logger, send_entities


class ActionProcessIntent(Action):
    """
        This class is an action that will be executed once the intent has been identified
        It gets the extracted entities, and forward them to the intent owner 
    """

    def name(self) -> Text:
        return "action_process_intent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get logger
        logger = setup_logger()
        logger.info("Received Action to process intent")
        # get values from the tracker
        latency_value = tracker.get_slot('latency')
        resolution_value = tracker.get_slot('resolution')
        throughput_value = tracker.get_slot('throughput')
        # if the values are none we set the default values
        if (latency_value is None) and (resolution_value is None):
            latency_value = '20'
            resolution_value = '1920x1080'
            throughput_value = '10'
        user_intent = {
            "service_type": tracker.get_slot('service'),
            "latency": latency_value,
            "resolution": resolution_value,
            "throughput": throughput_value
        }
        logger.info(user_intent)
        # send the extracted entities to the intent owner
        try:
            send_entities(logger, user_intent)
            # we report back to the user that the intent will be sent
            dispatcher.utter_message(response='utter_service_will_be_deployed')
        except Exception as e:
            logger.error(str(e))
            dispatcher.utter_message(text="We are sorry an error has occured")

        return []

# This class will ensure the validation of video service parameters


class ValidateServiceParamsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_video_service_params_form"

    # Validate latency
    def validate_latency(
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

    # Validate throughput

    def validate_throughput(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate throughput value."""
        try:
            throughput = int(slot_value)
            return {"throughput": slot_value}
        except:
            return {"throughput": None}

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
