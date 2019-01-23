import logging

_LOGGER = logging.getLogger(__name__)

def get_log_level(CONFIG):
    """ Parse config.yaml['logging'] to a logging level """
    if not CONFIG.get('logging'):
        return logging.CRITICAL

    config_logging = CONFIG['logging'].upper()
    log_levels = {"CRITICAL": logging.CRITICAL,
                  "ERROR": logging.ERROR,
                  "WARNING": logging.WARNING,
                  "INFO": logging.INFO,
                  "DEBUG": logging.DEBUG}
    level = log_levels.get(config_logging, logging.DEBUG)

    return level
