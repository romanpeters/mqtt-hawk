

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


#: Dict for all registered components, maps MQTT topics to functions
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