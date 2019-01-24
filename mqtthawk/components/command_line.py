"""
"""
import logging
from utils.mqtter import MQTTTopic
from utils.configger import get_component_config

import subprocess

_LOGGER = logging.getLogger(__name__)
_CONFIG = get_component_config(__name__.split('.')[-1])


@MQTTTopic(_CONFIG['command_topic'])
def command_line(client, userdata, payload) -> None:
    """
    """
    result = None
    if payload.get('state'):
        _LOGGER.debug(f"Running command \'{payload['state']}\'")
        result = subprocess.check_output(payload['state'].split())
    else:
        _LOGGER.warning("No state given in payload")
    if _CONFIG.get('state_topic') and result:
        _LOGGER.debug(f"Publishing {result} to {_CONFIG['state_topic']}")
        client.publish(_CONFIG['state_topic'], {"result": result})
