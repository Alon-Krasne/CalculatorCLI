from typing import Callable, List

import pydantic
from pydantic import BaseModel


class CommandDetails(BaseModel):
    name:  str
    description: str
    number_of_args: int
    func: Callable


class UserInput(BaseModel):
    name: str
    args: List[float]
    number_of_args: int

    @pydantic.validator('number_of_args')
    def length_of_argument(cls, v, values):
        if len(values['args']) != v:
            raise ValueError(f"Command {cls.name} requires {cls.number_of_args} arguments")
