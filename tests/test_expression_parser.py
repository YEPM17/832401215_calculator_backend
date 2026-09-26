from decimal import Decimal

import pytest

from app.services.expression_parser import (
    ExpressionError,
    ExpressionParser,
    normalize_expression,
)


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1+2", "3"),
        ("7-10", "-3"),
        ("6*7", "42"),
        ("8/2", "4"),
        ("2+3*4", "14"),
        ("(2+3)*4", "20"),
        ("-5", "-5"),
        ("3*-2", "-6"),
        ("1++2", "3"),
        ("+2.5", "2.5"),
        (".5+.25", "0.75"),
        ("1.5*4", "6"),
        ("  8 / 2 + 1 ", "5"),
        ("((2))", "2"),
    ],
)
def test_evaluate_valid_expression(expression, expected):
    assert ExpressionParser().evaluate(expression) == Decimal(expected)


@pytest.mark.parametrize(
    ("expression", "message"),
    [
        ("", "Expression cannot be empty"),
        ("   ", "Expression cannot be empty"),
        ("1+", "Missing operand"),
        ("*2", "Missing operand"),
        ("1/0", "Division by zero"),
        ("2**3", "Missing operand"),
        ("(1+2", "Missing closing parenthesis"),
        ("1+2)", "Unexpected token"),
        ("1a2", "Invalid character"),
        ("1/0.0", "Division by zero"),
        ("9" * 256, "Expression is too long"),
        ("1e10", "Invalid character"),
        ("1..2", "Invalid number"),
        ("9999999999.9*9999999999.9", "Result is out of range"),
    ],
)
def test_evaluate_invalid_expression(expression, message):
    with pytest.raises(ExpressionError, match=message):
        ExpressionParser().evaluate(expression)


def test_normalize_expression():
    assert normalize_expression(" 12×3÷2−1 ") == "12*3/2-1"
