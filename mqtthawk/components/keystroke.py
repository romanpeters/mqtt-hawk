"""
pip install keyboard
"""
import logging
from utils.mqtter import MQTTTopic
from utils.configger import get_component_config

import time
import keyboard


_LOGGER = logging.getLogger(__name__)
_CONFIG = get_component_config(__name__.split('.')[-1])


@MQTTTopic(_CONFIG['topic'])
def keystroke(client, userdata, payload) -> None:
    """
    Send a keystroke
    Use a list for simultanous key combinations and strings for typing
    """
    if payload.get('state'):
        if type(payload['state']) == list:
            payload['state'] = '+'.join(payload['state'])

            if payload.get('hold'):
                _LOGGER.debug(f"Holding \'{payload['state']}\' for {payload['hold']} seconds")
                keyboard.press(payload['state'])
                time.sleep(payload['hold'])
                keyboard.release(payload['state'])
            else:
                _LOGGER.debug(f"Sending keystroke \'{payload['state']}\'")
                keyboard.send(payload['state'])
        else:
            _LOGGER.debug(f"Writing \'{payload['state']}\'")
            keyboard.write(payload['state'])
    else:
        _LOGGER.warning("No state given in payload")
