"""
brew install terminal-notifier
pip install pync
"""
import logging
from utils.mqtter import MQTTTopic
from utils.configger import get_component_config

import pync

_LOGGER = logging.getLogger(__name__)
_CONFIG = get_component_config(__name__.split('.')[-1])


@MQTTTopic(_CONFIG['topic'])
def notify(client, userdata, payload) -> None:
    """
    Shows a macOS NC notification

    MQTT template:
        {
          "message": "Hello world",
          "title": "MQTT",
          "open": "https://google.com"
         }
    """
    _LOGGER.debug("Sending a pync notification")
    pync.Notifier.notify(**payload)
