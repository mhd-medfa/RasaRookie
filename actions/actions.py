from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re

def detect_language(text: str) -> str:
    """
    Simple language detection based on character analysis.
    Returns 'ar' for Arabic, 'en' for English.
    """
    # Arabic Unicode range
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
    arabic_chars = len(arabic_pattern.findall(text))

    # If significant Arabic characters found, return Arabic
    if arabic_chars > 0:
        return 'ar'
    return 'en'

# Mapping of intents to response templates
INTENT_RESPONSES = {
    'greet': 'utter_greet',
    'goodbye': 'utter_goodbye',
    'transfer_status': 'utter_transfer_status',
    'branch_locations': 'utter_branch_locations',
    'working_hours': 'utter_working_hours',
    'fees_inquiry': 'utter_fees',
    'exchange_rates': 'utter_exchange_rates',
    'how_to_send': 'utter_how_to_send',
    'how_to_receive': 'utter_how_to_receive',
    'required_documents': 'utter_required_documents',
    'complaint': 'utter_complaint',
    'speak_to_human': 'utter_speak_to_human',
    'services_list': 'utter_services',
    'nlu_fallback': 'utter_default',
}

class ActionRespondWithLanguage(Action):
    """
    Custom action that detects the user's language and responds
    in the same language (Arabic or English).
    """

    def name(self) -> Text:
        return "action_respond_with_language"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # Get the user's message and detected intent
        user_message = tracker.latest_message.get('text', '')
        intent = tracker.latest_message.get('intent', {}).get('name', 'nlu_fallback')

        # Detect language
        language = detect_language(user_message)

        # Get the base response template for this intent
        base_response = INTENT_RESPONSES.get(intent, 'utter_default')

        # Add language suffix
        response_name = f"{base_response}_{language}"

        # Send the response
        dispatcher.utter_message(response=response_name)

        # Store detected language in slot
        return [SlotSet("detected_language", language)]