
"""
Operation strategies and a factory to create them.
Implements the Strategy and Factory patterns.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Protocol
from .exceptions import OperationError

class OperationStrategy(Protocol):
    name: str
    symbol: str
    def execute(self, operands: List[float]) -> float: ...

class _Base(ABC):
    name: str = ""
    symbol: str = ""
    @abstractmethod
    def execute(self, operands):
        raise NotImplementedError # pragma: no cover

class Add(_Base):
    name, symbol = "addition", "+"
    def execute(self, operands):
        total = 0.0
        for x in operands:
            total += float(x)
        return total

class Subtract(_Base):
    name, symbol = "subtraction", "-"
    def execute(self, operands):
        if not operands:
            raise OperationError("Subtraction requires at least one operand")  # pragma: no cover
        it = iter(operands)
        result = float(next(it))
        for x in it:
            result -= float(x)
        return result

class Multiply(_Base):
    name, symbol = "multiplication", "*"
    def execute(self, operands):
        if not operands:
            raise OperationError("Multiplication requires at least one operand")  # pragma: no cover
        result = 1.0
        for x in operands:
            result *= float(x)
        return result

class Divide(_Base):
    name, symbol = "division", "/"
    def execute(self, operands):
        if not operands:
            raise OperationError("Division requires at least one operand")  # pragma: no cover
        it = iter(operands)
        result = float(next(it))
        for x in it:
            x = float(x)
            if x == 0.0:
                raise OperationError("Division by zero")  # pragma: no cover
            result /= x
        return result

class Power(_Base):
    name, symbol = "power", "^"
    def execute(self, operands):
        if len(operands) != 2:
            raise OperationError("Power requires exactly two operands")  # pragma: no cover
        base, exp = map(float, operands)
        return base ** exp

class Root(_Base):
    name, symbol = "root", "root"
    def execute(self, operands):
        if len(operands) != 2:
            raise OperationError("Root requires exactly two operands: degree, value")  # pragma: no cover
        degree, value = map(float, operands)
        if degree == 0:
            raise OperationError("Root degree cannot be zero")  # pragma: no cover
        if value < 0 and degree % 2 == 0:
            raise OperationError("Even-degree root of negative number is not real")  # pragma: no cover
        return value ** (1.0 / degree)

_FACTORY = {
    Add.symbol: Add,
    Subtract.symbol: Subtract,
    Multiply.symbol: Multiply,
    Divide.symbol: Divide,
    Power.symbol: Power,
    Root.symbol: Root,
}

def operation_factory(symbol: str) -> OperationStrategy:
    """
    Factory that returns a strategy instance by symbol.
    """
    cls = _FACTORY.get(symbol)
    if not cls:
        raise OperationError(f"Unknown operation symbol: {symbol!r}")
    return cls()
