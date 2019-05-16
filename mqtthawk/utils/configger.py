import os
import logging
import yaml


_LOGGER = logging.getLogger(__name__)

def read_env_vars(CONFIG):
    for i in ["MQTT_BROKER", "MQTT_PORT", "MQTT_USER", "MQTT_PASSWORD"]:
        if os.environ.get(i):
            group, var = i.lower().split('_')
            CONFIG[group].update({var: os.environ[i]})
    return CONFIG

try:
    # Read configuration
    with open("config.yaml", 'r') as yaml_file:
        CONFIG = yaml.load(yaml_file)
except FileNotFoundError:
    _LOGGER.warn("Couldn't find config.yaml")
    CONFIG = {}

CONFIG = read_env_vars(CONFIG)



def get_component_config(name):
    component_config = next((i for i in CONFIG['components'] if i['platform'] == name), None)
    if not component_config:
        _LOGGER.error(f"Could not match components entry in config.yaml to {name}")
    else:
        _LOGGER.debug(f"Found component config for {name}")
        return component_config
