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
utils.logger.set_log_level(config)
component_dict = utils.mqtter.COMPONENT_DICT

_LOGGER.debug("Config: " + str(config))

def on_connect(client, *args, **kwargs):
    _LOGGER.info(f"Connected to MQTT broker")
    _LOGGER.debug("Publishing birth message")
    client.publish("mqtthawk/state", "online", retain=True)

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
    if config.get('components'):
        plugins = [i['platform'] for i in config['components']]
        _LOGGER.debug(f"Components to load: {plugins}")
        components.load_plugins(plugins)
    else:
        _LOGGER.warning("No components added to config.yaml")

    mqtt_conf = config['mqtt']
    _LOGGER.debug(f"MQTT config: {mqtt_conf}")

    client = mqtt.Client('mqtthawk')

    if mqtt_conf.get('username'):
        _LOGGER.info("Using MQTT username and password")
        client.username_pw_set(username=mqtt_conf['username'], password=mqtt_conf['password'])

    client.on_connect = on_connect
    client.connect(host=mqtt_conf['broker'], port=mqtt_conf['port'])
    client.will_set("mqtthawk/state", "offline")
    client.on_message = on_message

    for topic in component_dict.keys():
        _LOGGER.info(f"Subscribing to {topic}")
        client.subscribe(topic)

    client.loop_forever()