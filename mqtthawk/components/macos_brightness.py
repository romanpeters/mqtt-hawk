"""
brew install brightness
"""
import subprocess
import logging
from utils.mqtter import MQTTTopic
from utils.configger import get_component_config

_LOGGER = logging.getLogger(__name__)
_CONFIG = get_component_config(__name__.split('.')[-1])


@MQTTTopic(_CONFIG['command_topic'])
def set_brightness(client, userdata, json_value) -> MQTTState:
    """
    Set the screen brightness

    MQTT template:
        {"state": "ON", "brightness": 255}
    """
    if json_value['state'].upper() == "OFF":
        brightness = 0
    else:
        if json_value.get('brightness'):
            brightness = json_value['brightness'] / 255
        else:
            _LOGGER.debug("No brightness given, checking current brightness")
            result = subprocess.check_output(['brightness', '-l'])
            brightness = float(result.split('.')[-1])
            if brightness < 0.1:
                _LOGGER.debug(f"Brightness was {brightness}, setting it to 0.5")
                brightness = 0.5
    command = ["brightness", str(brightness)]

    _LOGGER.debug(f"running command '{command}'")
    subprocess.run(command)
    client.publish(_CONFIG['state_topic'], brightness*255)