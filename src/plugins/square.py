"""
Square a number. This is a plugin.
"""

from src.utils import func_args
from typing import List


@func_args(number_of_args=1)
def command(args: List[float]) -> float:
    """
    Square a number.
    """
    return args[0] ** 2
