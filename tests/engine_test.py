import ast

import pytest

from arithmetic_expressions.engine import IllegalFunctionCallError, UndefinedVariableError
from arithmetic_expressions.expression import Expression
from tests.conftest import CustomType


class TestArithmeticEngine:

    def test_register_custom_type(self, custom_engine):
        assert "CustomType" in custom_engine._custom_types

    def test_build_expression_type(self, custom_engine):
        assert issubclass(custom_engine.build_expression_type(), Expression)

    def test_build_ast_object(self, custom_engine):
        # Test that AST objects are returned unchanged
        test_ast_obj = ast.parse('[x + 4, 2]')
        ast_obj = custom_engine.build_ast_object(test_ast_obj)
        assert ast_obj == test_ast_obj

        # Test that strings are turned into AST variable names
        test_string = "test_string"
        ast_obj = custom_engine.build_ast_object(test_string)
        assert isinstance(ast_obj, ast.Name)
        assert ast_obj.id == test_string

        # Test that numeric values are turned into AST constants
        test_float = 5.41
        ast_obj = custom_engine.build_ast_object(test_float)
        assert isinstance(ast_obj, ast.Constant)
        assert ast_obj.value == test_float

        test_int = 541
        ast_obj = custom_engine.build_ast_object(test_int)
        assert isinstance(ast_obj, ast.Constant)
        assert ast_obj.value == test_int

        # Test that custom types are turned into ast.Calls with constant terms
        test_custom_object = CustomType(4, "test")
        ast_obj = custom_engine.build_ast_object(test_custom_object)
        assert isinstance(ast_obj, ast.Call)
        for x in ast_obj.args:
            assert isinstance(x, ast.Constant)

    @classmethod
    def _parse_single_expression(cls, expression):
        return ast.parse(expression).body[0].value

    def test_evaluate_basic_binary_operations(self, custom_engine):
        assert custom_engine.evaluate(self._parse_single_expression("2 + 3")) == 5
        assert custom_engine.evaluate(self._parse_single_expression("4 - 2")) == 2
        assert custom_engine.evaluate(self._parse_single_expression("3 * 6")) == 18
        assert custom_engine.evaluate(self._parse_single_expression("10 / 2")) == 5.0
        assert custom_engine.evaluate(self._parse_single_expression("8 // 3")) == 2
        assert custom_engine.evaluate(self._parse_single_expression("5 % 2")) == 1
        assert custom_engine.evaluate(self._parse_single_expression("2 ** 3")) == 8

    def test_evaluate_basic_unary_operations(self, custom_engine):
        assert custom_engine.evaluate(self._parse_single_expression("-5")) == -5
        assert custom_engine.evaluate(self._parse_single_expression("+3")) == 3

    def test_evaluate_comparisons(self, custom_engine):
        assert custom_engine.evaluate(self._parse_single_expression("2 == 2")) is True
        assert custom_engine.evaluate(self._parse_single_expression("3 != 2")) is True
        assert custom_engine.evaluate(self._parse_single_expression("5 > 3")) is True
        assert custom_engine.evaluate(self._parse_single_expression("4 >= 4")) is True
        assert custom_engine.evaluate(self._parse_single_expression("1 < 3")) is True
        assert custom_engine.evaluate(self._parse_single_expression("2 <= 2")) is True

    def test_evaluate_ternary_operator(self, custom_engine):
        assert custom_engine.evaluate(self._parse_single_expression("5 if True else 3")) == 5
        assert custom_engine.evaluate(self._parse_single_expression("5 if 1 > 2 else 3")) == 3

    def test_evaluate_with_context(self, custom_engine):
        context = {'x': 10, 'y': 5}
        assert custom_engine.evaluate(self._parse_single_expression("x + y + 1"), context) == 16

    def test_evaluate_with_missing_context(self, custom_engine):
        context = {'x': 10}

        with pytest.raises(UndefinedVariableError):
            assert custom_engine.evaluate(self._parse_single_expression("x + y + 1"), context) == 16

    def test_evaluate_custom_type(self, custom_engine):
        result = custom_engine.evaluate(self._parse_single_expression("CustomType(1 + 1, 'test')"))
        assert isinstance(result, CustomType)
        assert result.a == 2
        assert result.b == 'test'

    def test_evaluate_custom_function(self, custom_engine):
        assert custom_engine.evaluate(self._parse_single_expression("min(1, 2)")) == 1

    def test_evaluate_illegal_function(self, custom_engine):
        with pytest.raises(IllegalFunctionCallError):
            custom_engine.evaluate(self._parse_single_expression("sin(1)"))
