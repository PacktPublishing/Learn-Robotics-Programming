
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import requests


class MyRobot(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.settings.load_skill_settings_from_file()
        self.base_url = self.settings.get("base_url")


    @intent_handler(IntentBuilder("").require("robot").require("DriveForward"))
    def handle_drive_forward(self, message):
        try:
            requests.get(self.base_url + "/run/behavior_line")
            self.speak_dialog('Robot')
            self.speak_dialog('Starting')
        except:
            self.speak_dialog("UnableToReach")
            LOG.exception("Can't reach the robot")



def create_skill():
    return MyRobot()
