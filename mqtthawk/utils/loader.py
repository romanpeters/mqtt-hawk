import logging
import os
import sys
import importlib
from pathlib import Path


_LOGGER = logging.getLogger(__name__)


def load_plugins(plugins):
    """ Import all python files in directory as plugins. """
    components_dir = str(Path(__file__).parent.parent.joinpath("components").resolve())  # components dir
    sys.path.insert(1, components_dir)  # look in components dir

    _LOGGER.info("Importing files from %s", components_dir)

    for _root, _dirs, files in os.walk(components_dir):
        python_files = [file for file in files if file.endswith(".py") and file != "__init__.py"]

        for plugin in python_files:
            plugin_name = plugin[:-3]  # Strip extension

            if plugin_name in plugins or plugins == []:  # load all plugins if no plugins specified
                _LOGGER.info("Loading plugin %s", plugin_name)

                try:
                    importlib.import_module(f"{plugin_name}", package=".")  # load component
                except (NameError, SyntaxError, Exception) as err:
                    _LOGGER.warning(f"Error loading {plugin_name}")
                    _LOGGER.warning(err)
                if plugins != []:
                    plugins.remove(plugin_name)
            else:
                _LOGGER.debug(f"Ignoring {plugin_name} because it's not in config.yaml")  

    for remaining in plugins:
        _LOGGER.warn(f"{remaining} not found")
