
"""
Calculation entity tying together operands and an operation strategy.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any
from .operations import OperationStrategy
from .exceptions import OperationError

@dataclass
class Calculation:
    operator: str
    operands: List[float]
    strategy: OperationStrategy
    result: float = field(init=False)

    def perform(self) -> float:
        try:
            self.result = self.strategy.execute(self.operands)
            return self.result
        except Exception as exc:  # EAFP: execute and catch
            raise OperationError(str(exc)) from exc

    def to_record(self) -> Dict[str, Any]:
        return {
            "operator": self.operator,
            "operands": self.operands,
            "result": getattr(self, "result", None),
        }
