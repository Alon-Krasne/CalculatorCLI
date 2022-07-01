# Calculator CLI

## Overview
This is a calculator CLI that can be used to perform basic arithmetic operations.
It also allows you to extend the calculator with new operations, just put them by template 
in the `src/plugins` folder

## Running
To run the project, use [pipenv](https://pipenv.pypa.io/en/latest/):
* `python -m pipenv install` - To build the environment and install dependencies
* `python -m pipenv run test` - To run unit tests
* `python -m pipenv run calculator` - To run the calculator CLI program

### Extensions
Extensions that can be added to the calculator CLI are `*.py` files that are placed in the `src/plugins` folder.
* The name of the file dictates the name of the operation.
* The file should contain a function with the following signature:
    * `def command(args: List[float]) -> float`
    * A decorator of type `@func_args` with the number of arguments allowed - e.g: `@func_args(number_of_args=1)`
    
_See `src/plugins/square.py` for an example._

**NOTE: I had issues with the file observer (plugins loader) on my WSL, it works fine on my Windows machine.**