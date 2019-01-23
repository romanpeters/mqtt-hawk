try:
    import colorlog as logging
except ImportError:
    import logging
import logging as _logging

_LOGGER = logging.getLogger(__name__)

def set_log_level(CONFIG):
    """ Parse config.yaml['logging'] to a logging level """
    if not CONFIG.get('logging'):
        logging.basicConfig(level=_logging.CRITICAL)
        return

    config_logging = CONFIG['logging'].upper()
    log_levels = {"CRITICAL": _logging.CRITICAL,
                  "ERROR": _logging.ERROR,
                  "WARNING": _logging.WARNING,
                  "INFO": _logging.INFO,
                  "DEBUG": _logging.DEBUG}

    level = log_levels.get(config_logging, _logging.DEBUG)

    logging.basicConfig(level=level)

