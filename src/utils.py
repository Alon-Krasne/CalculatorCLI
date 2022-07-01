from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import List, Callable


def configure_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger


def get_plugin_names(plugins_directory: Path = Path('plugins')) -> List[str]:
    files = os.listdir(plugins_directory)
    plugin_names = []
    for file in files:
        if file.startswith('__') or not file.endswith('.py'):
            continue

        plugin_names.append(file.replace('.py', ''))
    return plugin_names


def func_args(number_of_args: int) -> Callable:
    """
    Decorator that holds the number of arguments for the command.
    """
    def _func_args(fcn):
        fcn.number_of_args = number_of_args
        return fcn

    return _func_args
