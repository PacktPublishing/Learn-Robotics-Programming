
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import requests


class MyRobot(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.settings.load_skill_settings_from_file()
        self.base_url = self.settings.get("base_url")

    def handle_start_behavior(self, mode_name):
        try:
            requests.get(self.base_url + "/run/" + mode_name)
            self.speak_dialog('Robot')
            self.speak_dialog('Starting')
        except:
            self.speak_dialog("UnableToReach")
            LOG.exception("Can't reach the robot")

    @intent_handler(IntentBuilder("").require("robot").require("DriveForward"))
    def handle_drive_forward(self, message):
        self.handle_start_behavior("behavior_line")

    @intent_handler(IntentBuilder("").require("robot").require("FollowLine"))
    def handle_follow_line(self, message):
        self.handle_start_behavior("line_following")

def create_skill():
    return MyRobot()
