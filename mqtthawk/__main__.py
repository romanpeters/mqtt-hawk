#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import paho.mqtt.client as mqtt
import json
import pathlib
import components
import utils
try:
    import coloredlogs
    coloredlogs.install()
except:
    pass



_LOGGER = logging.getLogger(__name__)
__author__ = 'Roman Peters <mail()romanpeters.nl>'

config = utils.configger.CONFIG
utils.logger.set_log_level(config)
component_dict = utils.mqtter.COMPONENT_DICT

_LOGGER.debug("Config: " + str(config))


def on_connect(client, *args, **kwargs):
    _LOGGER.info("Connected to MQTT broker")
    _LOGGER.debug("Publishing birth message")
    client.publish("mqtthawk/state", "online", retain=True)


def on_disconnect(client, *args, **kwargs):
    _LOGGER.info(f"Disconnected from MQTT broker")
    _LOGGER.debug("Publishing offline message")
    client.publish("mqtthawk/state", "offline", retain=True)


def on_message(client, userdata, message):
    _LOGGER.info(f"MQTT: {message.topic}: {message.payload.decode('utf-8')} {'[retained]' if message.retain else ''}")

    try:
        payload = json.loads(message.payload)
    except ValueError:
        _LOGGER.warning("Payload is not valid JSON")
        payload = str(message.payload)

    component_func = utils.mqtter.COMPONENT_DICT[message.topic]
    _LOGGER.debug(f"Calling function {component_func}(client={client}, userdata={userdata}, payload={payload})")

    try:
        component_func(client=client, userdata=userdata, payload=payload)
    except Exception as err:
        _LOGGER.error(f"Error loading {component_func}, {payload}")
        _LOGGER.exception(err)


if __name__ == '__main__':
    if config.get('components'):
        plugins = [i['platform'] for i in config['components']]
        _LOGGER.debug(f"Components to load: {plugins}")
        utils.loader.load_plugins(plugins)
    else:
        _LOGGER.warning("No components added to config.yaml")

    mqtt_conf = config['mqtt']
    _LOGGER.debug(f"MQTT config: {mqtt_conf}")

    client = mqtt.Client('mqtthawk')

    if mqtt_conf.get('username'):
        _LOGGER.info("Using MQTT username and password")
        client.username_pw_set(username=mqtt_conf['username'], password=mqtt_conf['password'])

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(host=mqtt_conf['broker'], port=int(mqtt_conf['port']))

    client.will_set("mqtthawk/state", "offline")
    client.on_message = on_message

    for topic in component_dict.keys():
        _LOGGER.info(f"Subscribing to {topic}")
        client.subscribe(topic)


    if config.get('testrun'):
        import time
        client.loop_start()
        time.sleep(60)
        client.disconnect()
        client.loop_stop()
    else:
        client.loop_forever()
