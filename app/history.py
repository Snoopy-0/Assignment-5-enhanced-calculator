
"""
History management using pandas and Observer pattern.
"""
from __future__ import annotations
import os
from typing import Callable, List, Optional
import pandas as pd
from .calculator_memento import HistoryMemento, Caretaker
from .exceptions import ValidationError

class Observable:
    def __init__(self):
        self._observers: List[Callable[[pd.DataFrame], None]] = []

    def attach(self, observer: Callable[[pd.DataFrame], None]):
        self._observers.append(observer)

    def notify(self, df: pd.DataFrame):
        for obs in list(self._observers):
            obs(df)

class History(Observable):
    def __init__(self, csv_path: Optional[str] = None, autosave: bool = True):
        super().__init__()
        self.csv_path = csv_path
        self.autosave = autosave
        self.df = pd.DataFrame(columns=["operator", "operands", "result"])
        self.caretaker = Caretaker()
        self.caretaker.push(HistoryMemento.from_df(self.df))
        if self.csv_path and os.path.exists(self.csv_path):
            self.load(self.csv_path)

        if self.autosave and self.csv_path:
            self.attach(self._csv_autosave)

    # Observer
    def _csv_autosave(self, df: pd.DataFrame):
        if self.csv_path:
            df.to_csv(self.csv_path, index=False)

    def add_record(self, operator: str, operands, result: float):
        if operator is None:
            raise ValidationError("operator cannot be None")
        new_row = {"operator": operator, "operands": list(operands), "result": float(result)}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.caretaker.push(HistoryMemento.from_df(self.df))
        self.notify(self.df)

    def clear(self):
        self.df = pd.DataFrame(columns=["operator", "operands", "result"])
        self.caretaker.push(HistoryMemento.from_df(self.df))
        self.notify(self.df)

    def undo(self):
        mem = self.caretaker.undo(HistoryMemento.from_df(self.df))
        self.df = mem.to_df()
        self.notify(self.df)

    def redo(self):
        mem = self.caretaker.redo(HistoryMemento.from_df(self.df))
        self.df = mem.to_df()
        self.notify(self.df)

    def load(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        self.df = pd.read_csv(path)
        # Normalize columns
        for col in ["operator", "operands", "result"]:
            if col not in self.df.columns:
                self.df[col] = None
        self.caretaker.push(HistoryMemento.from_df(self.df))
        self.notify(self.df)

    def save(self, path: Optional[str] = None):
        path = path or self.csv_path
        if not path:
            raise ValidationError("CSV path not configured")
        self.df.to_csv(path, index=False)
