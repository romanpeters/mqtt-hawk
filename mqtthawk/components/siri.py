"""
pip install keyboard
"""
import logging
from utils.mqtter import MQTTTopic
from utils.configger import get_component_config

import subprocess
import re
import time
import keyboard


_LOGGER = logging.getLogger(__name__)
_CONFIG = get_component_config(__name__.split('.')[-1])


@MQTTTopic(_CONFIG['topic'])
def siri(client, userdata, payload) -> None:
    """

    """
    _LOGGER.debug("Triggering Siri")
    keyboard.press('command+space')
    time.sleep(0.3)
    keyboard.release('command+space')
    time.sleep(0.2)
    if not payload.get('state'):
        _LOGGER.warning("No state given in payload")
    else:
        _LOGGER.debug(f"Sending \'{payload['state']}\' to Siri")
        keyboard.write(payload.get('state'))
        keyboard.send('enter')

