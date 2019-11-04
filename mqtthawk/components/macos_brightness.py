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
def brightness(client, userdata, payload):
    """
    Set the screen brightness

    MQTT template:
        {"state": "ON", "brightness": 255}
    """
    screen = {}
    if payload['state'].upper() == "OFF":
        screen['brightness'] = 0
    else:
        if payload.get('brightness'):
            screen['brightness'] = payload['brightness']
        else:
            _LOGGER.debug("No brightness given, checking current brightness")
            result = subprocess.check_output('brightness -l'.split())
            _LOGGER.debug(f"Current brightness {float(result.strip().split()[-1])}")
            screen['brightness'] = int(float(result.strip().split()[-1]) * 255)
            if screen['brightness'] == 0:
                _LOGGER.debug("Turned on with brightness 0, changing to brightness 50%")
                screen['brightness'] = 127.5

    command = f"brightness {screen['brightness'] / 255}"
    _LOGGER.debug(f"running command \'{command}\'")
    subprocess.run(command.split())

    if screen['brightness'] > 0:
        screen['state'] = "ON"
    else:
        screen['state'] = "OFF"
    _LOGGER.debug(f"Sending {json.dumps(screen)} to {_CONFIG['state_topic']}")
    client.publish(_CONFIG['state_topic'], json.dumps(screen))