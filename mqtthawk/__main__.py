#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import paho.mqtt.client as mqtt
import json
import components
import utils

_LOGGER = logging.getLogger(__name__)
__author__ = 'Roman Peters <mail()romanpeters.nl>'

config = utils.configger.CONFIG
component_dict = utils.mqtter.COMPONENT_DICT

# Configure logger
log_level = utils.logger.get_log_level(config)
logging.basicConfig(level=log_level)
_LOGGER.info(f"Log level {_LOGGER.level}")


_LOGGER.debug("Config: " + str(config))


def on_message(client, userdata, message):
    _LOGGER.info(f"Message received: {message.payload.decode('utf-8')}")
    _LOGGER.info(f"\tTopic: {message.topic} {'[retained]' if message.retain else ''}")


    component_func = utils.mqtter.COMPONENT_DICT[message.topic]
    _LOGGER.debug(f"Calling function {component_func}")

    try:
        component_func(client, userdata, json.loads(message.payload))
    except Exception as err:
        _LOGGER.error(f"Error loading {component_func}, {json.loads(message.payload)}")
        _LOGGER.exception(err)


if __name__ == '__main__':
    plugins = [i['platform'] for i in config['components']]
    _LOGGER.debug(f"Components to load: {plugins}")

    components.load_plugins(plugins)

    mqtt_conf = config['mqtt']
    _LOGGER.debug(f"MQTT config: {mqtt_conf}")

    client = mqtt.Client('mqtthawk')

    if mqtt_conf.get('username'):
        client.username_pw_set(username=mqtt_conf['username'], password=mqtt_conf['password'])
        _LOGGER.info("Using MQTT username and password")

    client.connect(host=mqtt_conf['broker'], port=mqtt_conf['port'])
    _LOGGER.info(f"Connected to MQTT broker {mqtt_conf['broker']}")

    client.on_message = on_message
   
    for topic in component_dict.keys():
        _LOGGER.info(f"Subscribing to {topic}")
        client.subscribe(topic)

    client.loop_forever()


