
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import LOG

import requests


class MyRobot(MycroftSkill):
    def __init__(self):
        self.base_url = self.settings.get("base_url")
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder("").require("robot").require("FollowLine"))
    def handle_follow_line(self, message):
        try:
            requests.get(self.base_url + "/run/line_following")
            self.speak_dialog('Robot')
            self.speak_dialog('Starting')
        except:

            self.speak_dialog("UnableToReach")

    @intent_handler(IntentBuilder("").require("robot").require("AvoidWalls"))
    def handle_avoid_walls(self, message):
        try:
            requests.get(self.base_url + "/run/avoid_behavior")
            self.speak_dialog('Robot')
            self.speak_dialog('Starting')
        except:
            self.speak_dialog("UnableToReach")

    @intent_handler(IntentBuilder("").require("robot").require("Stop"))
    def handle_stop_robot(self, message):
        requests.get(self.base_url + "/stop")
        self.speak_dialog('Robot')
        self.speak_dialog('Stopping')


def create_skill():
    return MyRobot()
