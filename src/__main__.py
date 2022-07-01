import logging
import os
from pathlib import Path

from .calculator import CalculatorModel, CalculatorController
from .exceptions import CommandError
from .plugins.plugin_loader import PluginsManager, load_plugins

logger = logging.getLogger('calculator')
logger.setLevel(logging.DEBUG)

PLUGINS_PATH = Path(os.path.join(os.path.dirname(__file__), 'plugins'))


def main(plugins_path: str = PLUGINS_PATH):
    logger.debug('Starting calculator, fetching plugins from folder')
    plugins = load_plugins()
    calculator = CalculatorModel(plugins)

    logger.debug('Calculator set, starting calculator UI')
    calculator_controller = CalculatorController(calculator)

    logger.debug('Calculator UI started, starting plugins reloader. Observing folder: %s', plugins_path)
    reloader = PluginsManager(str(plugins_path), calculator)

    try:
        reloader.observer.start()
        while True:
            try:
                calculator_controller.interact_with_user()
            except CommandError as e:
                logger.warning('Error in calculator with exception:\n%r', e)

    except KeyboardInterrupt:
        logger.info('Exiting...')
    finally:
        reloader.observer.stop()
        reloader.observer.join()


if __name__ == "__main__":
    exit(main())
