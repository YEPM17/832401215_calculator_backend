from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

from app.config import get_settings


class ExpressionError(ValueError):
    pass


_PRECISION = Decimal("0.0000000001")
_MAX_VALUE = Decimal("9999999999.9999999999")
_NUMBER = re.compile(r"(?:\d+(?:\.\d*)?|\.\d+)")


def normalize_expression(expression: str) -> str:
    return expression.replace("×", "*").replace("÷", "/").replace("−", "-").strip()


class ExpressionParser:
    def evaluate(self, expression: str) -> Decimal:
        normalized = normalize_expression(expression)
        if not normalized:
            raise ExpressionError("Expression cannot be empty")
        if len(normalized) > get_settings().max_expression_length:
            raise ExpressionError("Expression is too long")

        self._tokens = self._tokenize(normalized)
        self._position = 0
        result = self._expression()
        if self._peek()[0] != "EOF":
            raise ExpressionError("Unexpected token")
        return self._finalize(result)

    def _expression(self) -> Decimal:
        value = self._term()
        while self._peek()[0] in {"+", "-"}:
            operator = self._advance()[0]
            right = self._term()
            value = value + right if operator == "+" else value - right
        return value

    def _term(self) -> Decimal:
        value = self._unary()
        while self._peek()[0] in {"*", "/"}:
            operator = self._advance()[0]
            right = self._unary()
            if operator == "*":
                value = value * right
            else:
                if right == 0:
                    raise ExpressionError("Division by zero")
                value = value / right
        return value

    def _unary(self) -> Decimal:
        if self._peek()[0] in {"+", "-"}:
            operator = self._advance()[0]
            value = self._unary()
            return value if operator == "+" else -value
        return self._primary()

    def _primary(self) -> Decimal:
        token, value = self._peek()
        if token == "NUMBER":
            self._advance()
            return value
        if token == "(":
            self._advance()
            result = self._expression()
            if self._peek()[0] != ")":
                raise ExpressionError("Missing closing parenthesis")
            self._advance()
            return result
        if token == ")":
            raise ExpressionError("Unexpected token")
        raise ExpressionError("Missing operand")

    def _tokenize(self, expression: str) -> list[tuple[str, Decimal | str]]:
        tokens: list[tuple[str, Decimal | str]] = []
        position = 0
        while position < len(expression):
            char = expression[position]
            if char.isspace():
                position += 1
                continue
            if char in "+-*/()":
                tokens.append((char, char))
                position += 1
                continue
            if (
                char == "."
                and position + 1 < len(expression)
                and expression[position + 1] == "."
            ):
                raise ExpressionError("Invalid number")

            match = _NUMBER.match(expression, position)
            if match is None:
                raise ExpressionError(f"Invalid character: {char}")

            literal = match.group(0)
            if literal.endswith(".") and position + len(literal) < len(expression):
                if expression[position + len(literal)] == ".":
                    raise ExpressionError("Invalid number")
            try:
                number = Decimal(literal)
            except InvalidOperation as error:
                raise ExpressionError("Invalid number") from error
            tokens.append(("NUMBER", number))
            position = match.end()

        tokens.append(("EOF", "EOF"))
        return tokens

    def _peek(self) -> tuple[str, Decimal | str]:
        return self._tokens[self._position]

    def _advance(self) -> tuple[str, Decimal | str]:
        token = self._tokens[self._position]
        self._position += 1
        return token

    @staticmethod
    def _finalize(value: Decimal) -> Decimal:
        if not value.is_finite() or abs(value) > _MAX_VALUE:
            raise ExpressionError("Result is out of range")
        return value.quantize(_PRECISION, rounding=ROUND_HALF_UP)
