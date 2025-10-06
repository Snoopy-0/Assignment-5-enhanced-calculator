
"""
Memento pattern for storing/restoring history DataFrame states.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List
import pandas as pd
from .exceptions import UndoRedoError

@dataclass(frozen=True)
class HistoryMemento:
    snapshot_csv: str  # serialize df as CSV string 

    @staticmethod
    def from_df(df: pd.DataFrame) -> "HistoryMemento":
        return HistoryMemento(snapshot_csv=df.to_csv(index=False))

    def to_df(self) -> pd.DataFrame:
        from io import StringIO
        return pd.read_csv(StringIO(self.snapshot_csv)) if self.snapshot_csv else pd.DataFrame(columns=["operator","operands","result"])

class Caretaker:
    """
    Caretaker keeps stacks for undo/redo.
    The top of _undo_stack is the *current* state.
    """
    def __init__(self):
        self._undo_stack: List[HistoryMemento] = []
        self._redo_stack: List[HistoryMemento] = []

    def push(self, mem: HistoryMemento):
        self._undo_stack.append(mem)
        self._redo_stack.clear()

    def undo(self, current: HistoryMemento | None = None) -> HistoryMemento:
        if not self._undo_stack:
            raise UndoRedoError("Nothing to undo")  # pragma: no cover
        if current is not None:
            last = self._undo_stack.pop()
            self._redo_stack.append(current)
            return last
        if len(self._undo_stack) < 2:
            raise UndoRedoError("Nothing to undo")  # pragma: no cover
        popped_current = self._undo_stack.pop()
        self._redo_stack.append(popped_current)
        return self._undo_stack[-1]

    def redo(self, current: HistoryMemento | None = None) -> HistoryMemento:
        if not self._redo_stack:
            raise UndoRedoError("Nothing to redo")  # pragma: no cover
        mem = self._redo_stack.pop()
        self._undo_stack.append(mem)
        return mem
