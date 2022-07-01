import json

import pytest as pytest

from src.calculator import CalculatorModel, CalculatorController
from src.exceptions import CommandError
from src.plugins.plugin_loader import load_plugins


@pytest.fixture
def commands_json():
    with open('tests/assets/commands.json') as f:
        return json.load(f)


@pytest.fixture
def calculator():
    calculator = CalculatorModel()
    return calculator


@pytest.fixture
def calculator_with_plugins():
    plugins = load_plugins()
    return CalculatorModel(plugins)


def test_get_command_names(calculator):
    assert sorted(calculator.command_names) == sorted(['add', 'subtract', 'multiply', 'divide'])


def test_load_existing_plugin(calculator_with_plugins):
    assert sorted(calculator_with_plugins.command_names) == sorted(['add', 'subtract', 'multiply', 'divide', 'square'])


def test_get_calculator_commands(calculator, commands_json):
    assert calculator.get_calculator_commands() == commands_json


def test_get_function_by_name(calculator):
    assert calculator.get_function_by_name('add') == calculator.add


def test_add(calculator):
    assert calculator.add([1, 2]) == 3


def test_subtract(calculator):
    assert calculator.subtract([1, 2]) == -1


def test_multiply(calculator):
    assert calculator.multiply([1, 2]) == 2


def test_divide(calculator):
    assert calculator.divide([1, 2]) == 0.5


def test_division_by_zero(calculator):
    with pytest.raises(CommandError):
        calculator.divide([1, 0])


def test_validate_user_input_false(calculator):
    calculator_controller = CalculatorController(calculator)
    with pytest.raises(CommandError):
        calculator_controller.validate_user_input('add 1 2')


def test_validate_user_input_true(calculator):
    calculator_controller = CalculatorController(calculator)
    assert calculator_controller.validate_user_input('add [1,2]') == ('add', [1, 2])
