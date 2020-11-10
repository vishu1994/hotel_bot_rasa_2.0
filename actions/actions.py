# # This files contains your custom actions which can be used to run
# # custom Python code.
# #
# # See this guide on how to implement these action:
# # https://rasa.com/docs/rasa/custom-actions
#
#
# #This is a simple example for a custom action which utters "Hello World!"
#

from typing import Any, Text, Dict, List

import dateutil
from dateutil import parser

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import SlotSet

def Time(value):
    datetime_obj = dateutil.parser.parse(value)
    time = datetime_obj.strftime('%H:%M:%S')
    t = int(time.split(":")[0])
    m = int(time.split(":")[1])
    if t > 12:
        hm = "{}:{} pm".format(t-12, m)
        return hm
    else:
        hm = "{}:{} am".format(t, m)
        return hm

class ActionSetSingleRoom(Action):

    def name(self) -> Text:
        return "action_set_single_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        return [SlotSet("num_rooms", "1")]


class ActionSetTimeSlot(Action):

    def name(self) -> Text:
        return "action_set_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities= tracker.latest_message['entities']

        for entity in entities:
            if entity['extractor']=='DucklingEntityExtractor' and entity['entity']=='time':
                if type(entity['value'])==str:
                    time=entity['value']
                else:
                    time=entity['value']['from']
                break
        time = Time(time)

        return [SlotSet("time_from", time)]


class ActionAskQuestion(Action):

    def name(self) -> Text:
        return "action_question_after_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        list_of_events= tracker.events

        if len(list_of_events)>=5:
            event= list_of_events[-5]
            if event['event']=='bot':
                template= event['metadata']['template_name']

                if template=='utter_num_of_rooms' or template=='utter_room_type' or template=='utter_ask_when_to_clean':

                    dispatcher.utter_message(template= template)





        else:
            dispatcher.utter_message(template= "utter_greet")


        return []
