import pytest

from arithmetic_expressions.engine import UndefinedVariableError
from arithmetic_expressions.expression import Expression


@pytest.fixture
def sample_expression(custom_expression_type):
    return custom_expression_type.parse("x + 1")


class TestExpressionBuilding:

    def test_parse(self, sample_expression):
        assert str(sample_expression) == "x + 1"

    def test_parse_invalid_expression(self):
        with pytest.raises(SyntaxError):
            Expression.parse("1 1")

    def test_evaluate_with_variable(self, sample_expression):
        assert sample_expression.evaluate(x=2) == 3

    def test_evaluate_with_undefined_variable(self, sample_expression):
        with pytest.raises(UndefinedVariableError):
            sample_expression.evaluate()

    def test_string_representation(self, sample_expression):
        assert str(sample_expression) == "x + 1"

    def test_representation(self, sample_expression):
        assert repr(sample_expression) == "x + 1"

    def test_lower_bound(self):
        assert Expression(1).upper_bound(Expression(2)) == Expression.parse("1 if 1 > 2 else 2")

    def test_upper_bound(self):
        assert Expression(1).upper_bound(Expression(2)) == Expression.parse("1 if 1 < 2 else 2")

    def test__add__(self):
        assert Expression(1) + Expression(2) == Expression.parse('1 + 2')
        assert Expression(1) + 2 == Expression.parse('1 + 2')

    def test__radd__(self):
        assert 1 + Expression(2) == Expression.parse('1 + 2')

    def test__sub__(self):
        assert Expression(1) - Expression(2) == Expression.parse('1 - 2')
        assert Expression(1) - 2 == Expression.parse('1 - 2')

    def test__rsub__(self):
        assert 1 - Expression(2) == Expression.parse('1 - 2')

    def test__mul__(self):
        assert Expression(1) * Expression(2) == Expression.parse('1 * 2')
        assert Expression(1) * 2 == Expression.parse('1 * 2')

    def test__rmul__(self):
        assert 1 * Expression(2) == Expression.parse('1 * 2')

    def test__truediv__(self):
        assert Expression(1) / Expression(2) == Expression.parse('1 / 2')
        assert Expression(1) / 2 == Expression.parse('1 / 2')

    def test__rtruediv__(self):
        assert 1 / Expression(2) == Expression.parse('1 / 2')

    def test__floordiv__(self):
        assert Expression(1) // Expression(2) == Expression.parse('1 // 2')
        assert Expression(1) // 2 == Expression.parse('1 // 2')

    def test__rfloordiv__(self):
        assert 1 // Expression(2) == Expression.parse('1 // 2')

    def test__mod__(self):
        assert Expression(1) % Expression(2) == Expression.parse('1 % 2')
        assert Expression(1) % 2 == Expression.parse('1 % 2')

    def test__rmod__(self):
        assert 1 % Expression(2) == Expression.parse('1 % 2')

    def test__pow__(self):
        assert Expression(1) ** Expression(2) == Expression.parse('1 ** 2')
        assert Expression(1) ** 2 == Expression.parse('1 ** 2')

    def test__rpow__(self):
        assert 1 ** Expression(2) == Expression.parse('1 ** 2')

    def test__eq__(self):
        assert (Expression(1) == Expression(1)) == Expression.parse('1 == 1')
        assert (Expression(1) == 2) == Expression.parse('1 == 2')

    def test__ne__(self):
        assert (Expression(1) != Expression(2)) == Expression.parse('1 != 2')
        assert (Expression(1) != 2) == Expression.parse('1 != 2')

    def test__ge__(self):
        assert (Expression(2) >= Expression(1)) == Expression.parse('2 >= 1')
        assert (Expression(2) >= 2) == Expression.parse('2 >= 2')

    def test__gt__(self):
        assert (Expression(2) > Expression(1)) == Expression.parse('2 > 1')
        assert (Expression(2) > 2) == Expression.parse('2 > 2')

    def test__le__(self):
        assert (Expression(1) <= Expression(2)) == Expression.parse('1 <= 2')
        assert (Expression(1) <= 2) == Expression.parse('1 <= 2')

    def test__lt__(self):
        assert (Expression(1) < Expression(2)) == Expression.parse('1 < 2')
        assert (Expression(1) < 2) == Expression.parse('1 < 2')

    def test__neg__(self):
        assert -Expression(1) == Expression.parse('-1')

    def test__pos__(self):
        assert +Expression(1) == Expression.parse('+1')
