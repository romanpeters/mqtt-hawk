"""
brew install brightness
"""
import logging
import subprocess
import json
from utils.mqtter import MQTTTopic
from utils.configger import get_component_config

_LOGGER = logging.getLogger(__name__)
_CONFIG = get_component_config(__name__.split('.')[-1])


@MQTTTopic(_CONFIG['command_topic'])
def set_brightness(client, userdata, json_value):
    """
    Set the screen brightness

    MQTT template:
        {"state": "ON", "brightness": 255}
    """
    screen = {}
    if json_value['state'].upper() == "OFF":
        screen['brightness'] = 0
    else:
        if json_value.get('brightness'):
            screen['brightness'] = json_value['brightness']
        else:
            _LOGGER.debug("No brightness given, checking current brightness")
            result = subprocess.check_output(['brightness', '-l'])
            _LOGGER.debug(f"Current brightness {float(result.strip().split()[-1])}")
            screen['brightness'] = int(float(result.strip().split()[-1]) * 255)
            if screen['brightness'] == 0:
                _LOGGER.debug("Turned on with brightness 0, changing to brightness 50%")
                screen['brightness'] = 127.5

    command = ["brightness", str(screen['brightness'] / 255)]
    _LOGGER.debug(f"running command \'{' '.join(command)}\'")
    subprocess.run(command)

    if screen['brightness'] > 0:
        screen['state'] = "ON"
    else:
        screen['state'] = "OFF"
    _LOGGER.debug(f"Sending {json.dumps(screen)} to {_CONFIG['state_topic']}")
    client.publish(_CONFIG['state_topic'], json.dumps(screen))