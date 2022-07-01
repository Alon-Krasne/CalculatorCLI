from __future__ import annotations

import importlib
import logging
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEvent

from src.calculator import CalculatorModel
from src.exceptions import CommandError

logger = logging.getLogger('calculator')


class PluginsManager:
    def __init__(self, path: str, calculator: CalculatorModel):
        self._calculator = calculator

        self._event_handler = PatternMatchingEventHandler(
            patterns=["*.py"], ignore_directories=True
        )

        self._event_handler.on_created = self.on_created_or_updated
        self._event_handler.on_modified = self.on_created_or_updated
        self._event_handler.on_deleted = self.on_deleted
        self._event_handler.on_moved = self.on_created_or_updated

        self._path = path
        self.observer = Observer()
        self.observer.schedule(self._event_handler, self._path, recursive=True)

    def on_created_or_updated(self, event: FileSystemEvent):
        logger.info(f"{event.src_path} created or updated")
        command_name = Path(event.src_path).stem
        if hasattr(self._calculator, command_name):
            logger.info("Command %s already exists, deleting", command_name)
            delattr(self._calculator, command_name)
        try:
            logger.info("Validating command %s", command_name)
            plugin = get_and_validate_plugin(command_name)

            logger.debug("Command %s Validated, Adding it to calculator", command_name)
            setattr(self._calculator, command_name, plugin.command)

            new_commands = self._calculator.reset_command_names()
            logger.info("Command %s added", command_name)
            logger.debug("New commands: %s", new_commands)

        except CommandError:
            logger.warning(f"{event.src_path} is not a valid command plugin")

        except Exception:
            logger.exception(f"Error loading command {command_name}")
            raise

    def on_deleted(self, event: FileSystemEvent):
        logger.info('%s deleted', event.src_path)
        command_name = Path(event.src_path).stem
        if hasattr(self._calculator, command_name):
            logger.info("Deleting command %s", command_name)
            delattr(self._calculator, command_name)
            logger.debug('Command %s deleted', command_name)


def get_and_validate_plugin(command_name: str, package_path: str = 'src.plugins'):
    plugin = importlib.import_module(f'{package_path}.{command_name}', '.')
    if not hasattr(plugin, 'command') or not hasattr(plugin.command, 'number_of_args'):
        raise CommandError(f"Plugin {command_name} does not have required attributes")
    return plugin


def load_plugins():
    return importlib.import_module('src.plugins', '.').plugins