import logging
import os.path
import importlib

_LOGGER = logging.getLogger(__name__)


def load_plugins(plugins):
    """ Import all python files in directory as plugins. """
    root = os.path.dirname(__file__)
    _LOGGER.info("Importing files from %s", root)

    for _root, _dirs, files in os.walk(root):
        python_files = [file for file in files if file.endswith(".py") and file != "__init__.py"]

        for plugin in python_files:
            plugin_name = plugin[:-3]  # Strip extension

            if plugin_name in plugins or plugins == []:  # load all plugins if no plugins specified
                _LOGGER.info("Loading plugin %s", plugin_name)
                try:
                    importlib.import_module(f".{plugin_name}", package=__name__)
                except (NameError, SyntaxError, Exception) as err:
                    _LOGGER.warning(f"Error loading {plugin_name}")
                    #_LOGGER.exception(err)
                if plugins != []:
                    plugins.remove(plugin_name)
            else:
                _LOGGER.debug(f"Ignoring {plugin_name} because it's not in config.yaml")  

    for remaining in plugins:
        _LOGGER.warn(f"{remaining} not found")
