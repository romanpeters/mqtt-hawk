"""
brew install terminal-notifier
pip install pync
"""
import logging
from utils.mqtter import MQTTTopic
from utils.configger import get_component_config

from pprint import pprint

_LOGGER = logging.getLogger(__name__)
_CONFIG = get_component_config(__name__.split('.')[-1])


@MQTTTopic(_CONFIG['command_topic'])
def print(client, userdata, payload) -> None:
    """
    prints to the console

    """
    pprint(payload)
