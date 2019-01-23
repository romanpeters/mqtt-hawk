import logging
import utils
from utils import MQTTTopic

import pync

_LOGGER = logging.getLogger(__name__)
_CONFIG = utils.get_component_config(__name__.split('.')[-1])


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