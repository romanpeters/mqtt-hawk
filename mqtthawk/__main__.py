#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import paho.mqtt.client as mqtt
import json
import components
import utils

_LOGGER = logging.getLogger(__name__)
__author__ = 'Roman Peters <mail()romanpeters.nl>'

config = utils.CONFIG

# Configure logger
log_level = utils.get_log_level()
logging.basicConfig(level=log_level)
_LOGGER.info(f"Log level {_LOGGER.level}")


_LOGGER.debug("Config: " + str(config))


def on_message(client, userdata, message):
    _LOGGER.info(f"Message received: {message.payload.decode('utf-8')}")
    _LOGGER.info(f"\tTopic: {message.topic} {'[retained]' if message.retain else ''}")
    try:
        utils.COMPONENT_DICT[message.topic](json.loads(message.payload))
    except Exception as err:
        _LOGGER.error(f"Error loading {utils.COMPONENT_DICT[message.topic]}, json.loads(message.payload)")
        _LOGGER.exception(err)


if __name__ == '__main__':
    plugins = [i['platform'] for i in config['components']]
    _LOGGER.debug(f"Components to load: {plugins}")

    components.load_plugins(plugins)

    m_conf = config['mqtt']
    _LOGGER.debug(f"MQTT config: {m_conf}")

    client= mqtt.Client("mqttwarn-lite")

    if m_conf.get('username'):
        client.username_pw_set(username=m_conf['username'], password=m_conf['password'])
        _LOGGER.info("Using MQTT username and password")

    client.connect(host=m_conf['broker'], port=m_conf['port'])
    _LOGGER.info(f"Connected to MQTT broker {m_conf['broker']}")

    client.on_message = on_message
   
    for topic in utils.COMPONENT_DICT.keys():
        _LOGGER.info(f"Subscribing to {topic}")
        client.subscribe(topic)

    client.loop_forever()


