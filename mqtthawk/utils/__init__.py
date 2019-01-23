import logging
import yaml

_LOGGER = logging.getLogger(__name__)

# Read configuration
with open("config.yaml", 'r') as yaml_file:
    CONFIG = yaml.load(yaml_file)

def get_log_level():
    """ Parse config.yaml['logging'] to a logging level """
    if not CONFIG.get('logging'):
        _LOGGER.warning("No logging configured in config.yaml")
        return logging.NOTSET

    config_logging = CONFIG['logging'].upper()
    log_levels = {"CRITICAL": logging.CRITICAL,
                  "ERROR": logging.ERROR,
                  "WARNING": logging.WARNING,
                  "INFO": logging.INFO,
                  "DEBUG": logging.DEBUG}
    level = log_levels.get(config_logging, logging.DEBUG)

    return level

def get_component_config(name):
    component_config = next((i for i in CONFIG['components'] if i['platform'] == name), None)
    if not component_config:
        _LOGGER.error(f"Could not match components entry in config.yaml to {name}")
    else:
        _LOGGER.debug(f"Found component config for {name}")
        return component_config

class RegisteringDecorator(object):
    """
        General decorator for registering.
        Must be overridden.
    """

    target_dict = {}

    def __init__(self, topic):
        """ Register component by topic. """
        self.topic = topic

    def __call__(self, func):
        """ Register the callable under the given MQTT topic. """
        self.target_dict[self.topic] = func

        return func


#: Dict for all registered commands, maps uppercase commands to functions
COMPONENT_DICT = {}


class MQTTTopic(RegisteringDecorator):
    """
        Decorator that registers it's function triggerable by MQTT topic.
    """

    target_dict = COMPONENT_DICT

    def __init__(self, topic):
        """ Store params and call super """
        super().__init__(topic)

    def __call__(self, func):
        return super().__call__(func)
