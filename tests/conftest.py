from dataclasses import dataclass
from typing import Type

import pytest

from arithmetic_expressions.engine import ArithmeticEngine
from arithmetic_expressions.expression import Expression


@dataclass
class CustomType:
    a: int
    b: str

    def deconstruct(self):
        return [self.a, self.b], {}


@pytest.fixture
def custom_engine() -> ArithmeticEngine:
    engine = ArithmeticEngine(register_default_functions=True)
    engine.register_custom_type(CustomType, CustomType.deconstruct)
    return engine


@pytest.fixture
def custom_expression_type(custom_engine) -> Type[Expression]:
    return custom_engine.build_expression_type()
