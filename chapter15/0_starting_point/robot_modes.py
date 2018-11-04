import subprocess


class RobotModes(object):
    """Our robot behaviors and tests as running modes"""

    # Mode config goes from a "mode_name" to a script to run. Configured for look up
    # We could convert the path segment into a python script by adding '.py'
    # but this is a bad idea for at least 2 reasons:
    # * We may want to switch the script it really runs (avoid_behavior.py for simple_avoid_behavior.py)
    # * It's not a great security idea to let this run anything but the scripts we specify here.
    mode_config = {
        "avoid_behavior": "avoid_behavior.py",
        "circle_head": "circle_pan_tilt_behavior.py",
        "test_leds": "leds_test.py",
        "test_hcsr04": "test_hcsr04.py",
        "stop_at_line": "stop_at_line.py",
        "line_following": "line_following_behavior.py",
        "behavior_line": "straight_line_drive.py",
        "behavior_path": "drive_square.py"
    }

    # Menu config is a list of mode_names and text to display. Ordered as we'd like our menu.
    menu_config = [
        {"mode_name": "avoid_behavior", "text": "Avoid Behavior"},
        {"mode_name": "circle_head", "text": "Circle Head"},
        {"mode_name": "test_leds", "text": "Test LEDS"},
        {"mode_name": "test_hcsr04", "text": "Test HC-SR04"},
        {"mode_name": "stop_at_line", "text": "Stop At Line"},
        {"mode_name": "line_following", "text": "Line Following"},
        {"mode_name": "behavior_line", "text": "Drive In A Line"},
        {"mode_name": "behavior_path", "text": "Drive a Square Path"}
    ]

    def __init__(self):
        self.current_process = None

    def is_running(self):
        """Check if there is a process running. Returncode is only set when a process finishes"""
        return self.current_process and self.current_process.returncode is None
    
    def run(self, mode_name):
        """Run the mode as a subprocess, but not if we still have one running"""
        while self.is_running():
            self.stop()
        script = self.mode_config[mode_name]
        self.current_process = subprocess.Popen(["python", script])
        return True

    def stop(self):
        """Stop a process"""
        if self.is_running():
            # Sending the signal sigint is (on Linux) similar to pressing ctrl-c. 
            # The behavior will do the same clean up.
            self.current_process.send_signal(subprocess.signal.SIGINT)
            self.current_process = None
