"""
brew install terminal-notifier
pip install pync
"""
import logging
from utils import MQTTTopic, get_component_config

import pync

_LOGGER = logging.getLogger(__name__)
_CONFIG = get_component_config(__name__.split('.')[-1])


@MQTTTopic(_CONFIG['state_topic'])
def show_notification(json_value):
    """
    Shows a macOS NC notification

    MQTT template:
        {
          "message": "Hello world",
          "title": "MQTT",
          "open": "https://google.com"
         }
    """
    try:
        pync.Notifier.notify(**json_value)
        _LOGGER.debug("Sent a pync notification")
    except Exception as err:
        _LOGGER.error(f"Error sending notification for {json_value}")
        _LOGGER.exception(err)