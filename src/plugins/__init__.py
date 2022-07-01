import importlib
import os
import pathlib

plugins = {}
HERE = pathlib.Path(__file__).parent.resolve()
for item in os.listdir(HERE):
    if item.endswith('.py') and not item.startswith('__') and item != 'plugin_loader.py':
        command_name = item.replace('.py', '')
        name_for_import = f"src.{HERE.name}.{command_name}"
        plugins[command_name] = importlib.import_module(name_for_import, '.').command
