try:
    import colorlog as logging
except ImportError:
    import logging

import yaml


_LOGGER = logging.getLogger(__name__)

# Read configuration
with open("config.yaml", 'r') as yaml_file:
    CONFIG = yaml.load(yaml_file)

def get_component_config(name):
    component_config = next((i for i in CONFIG['components'] if i['platform'] == name), None)
    if not component_config:
        _LOGGER.error(f"Could not match components entry in config.yaml to {name}")
    else:
        _LOGGER.debug(f"Found component config for {name}")
        return component_config