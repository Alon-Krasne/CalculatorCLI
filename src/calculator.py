from __future__ import annotations

import ast
import json
from typing import List, Callable, Tuple, Union, Dict, Optional

from src.exceptions import CommandError
from src.models import CommandDetails, UserInput
from src.utils import configure_logger, func_args

logger = configure_logger('calculator')


class CalculatorModel:
    """
    Calculator class that handles the commands and their execution.
    """
    _command_names: List[str]

    def __init__(self, commands: Optional[Dict[str, Callable]] = None):
        if commands is None:
            commands = {}

        for key, value in commands.items():
            if callable(value):
                logger.info(f"Adding command {key}")
                setattr(self, key, value)

    def reset_command_names(self) -> List[str]:
        self._command_names = []
        return self.command_names

    @property
    def command_names(self) -> List[str]:
        if not hasattr(self, '_command_names') or not self._command_names:
            self._command_names = []
            for name in dir(self):
                name_obj = getattr(self, name)
                if name_obj and hasattr(name_obj, 'number_of_args'):
                    self._command_names.append(name)
        return self._command_names

    def get_calculator_commands(self) -> List[dict]:
        commands = []
        for name in self.command_names:
            func = getattr(self, name)
            if not callable(func):
                continue
            commands.append(
                {
                    'name': name,
                    'description': func.__doc__.strip(),
                    'number_of_args': self.get_function_by_name(name).number_of_args
                }
            )
        return commands

    def get_function_by_name(self, name: str) -> Callable:
        return getattr(self, name)

    def list_commands(self) -> None:
        commands = self.get_calculator_commands()
        print(commands)

    @staticmethod
    @func_args(number_of_args=2)
    def add(args: List[float]) -> float:
        """
        Add two numbers
        """
        return args[0] + args[1]

    @staticmethod
    @func_args(number_of_args=2)
    def subtract(args: List[float]) -> float:
        """
        Subtract two numbers
        """
        return args[0] - args[1]

    @staticmethod
    @func_args(number_of_args=2)
    def multiply(args: List[float]) -> float:
        """
        Multiply two numbers
        """
        return args[0] * args[1]

    @staticmethod
    @func_args(number_of_args=2)
    def divide(args: List[float]) -> float:
        """
        Divide two numbers
        """
        try:
            return args[0] / args[1]
        except ZeroDivisionError:
            raise CommandError(f"Division by zero not allowed")


class CalculatorController:
    def __init__(self, calculator: CalculatorModel):
        self._calculator = calculator

    def print_commands(self):
        print(json.dumps(self._calculator.get_calculator_commands(), indent=2))

    @staticmethod
    def print_menu():
        print('Welcome to the calculator! Type "list" to see the available commands.')

    @staticmethod
    def get_user_input():
        user_input = input()
        logger.info('User input: %s', user_input)
        return user_input

    def interact_with_user(self, print_menu: bool = True):
        if print_menu:
            self.print_menu()
        user_input = self.get_user_input()
        try:
            command, args = self.validate_user_input(user_input)
            if command != 'list_commands':
                print(self.run_command(command, args))
            else:
                self.print_commands()
        except CommandError as e:
            logger.error('Could not validate user input with exception %r', e)

    def validate_user_input(self, user_input: str) -> Tuple[str, Union[List[float], CalculatorModel]]:
        try:
            if user_input == 'list':
                return 'list_commands', self._calculator

            splitted_input = user_input.split(' ')

            if len(splitted_input) != 2:
                raise CommandError(f"Invalid number of arguments, original input: {user_input}")

            command = splitted_input[0]
            try:
                number_of_args = self._calculator.get_function_by_name(command).number_of_args
            except AttributeError:
                raise CommandError(f"No data on number of arguments for {command} ")

            args = ast.literal_eval(splitted_input[1])
            try:
                user_input = UserInput(name=command, args=args, number_of_args=number_of_args)
            except ValueError as e:
                raise CommandError(f"Invalid arguments, original exception: {e!r}")

            if user_input.name not in self._calculator.command_names:
                raise CommandError(f"User chose {user_input.name} command, not found")

            return user_input.name, user_input.args

        except Exception as e:
            raise CommandError(f"Invalid user input: {user_input}, caused exception: {e!r}")

    def run_command(self, command: str, args: List[float]) -> float:
        return self._calculator.get_function_by_name(command)(args)
