"""
Configuration variables. Make changes to config_custom.py.

..versionchanged::30.09.21
	* Added config_custom.py to avoid git conflicts.
"""
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

catkin_ws = "/home/lauri/catkin_ws/src"
homework_bundle_path = f"{PROJECT_DIR}/data"
results_file = "results.txt"
supplemental_dir = "supplemental"
catkin_command = "catkin_make"
rospack_command = "rospack profile"
launch_command = "roslaunch {} differential_robot.launch"

try:
    with open(__file__.replace("config.py", "config_custom.py")) as source_file:
        exec(source_file.read())
except IOError:
    "No custom config detected"
