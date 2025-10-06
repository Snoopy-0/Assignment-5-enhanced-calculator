
import builtins, io, contextlib, pytest, os, tempfile
from app.calculator_repl import CalculatorFacade
from app.calculator_config import Config

def test_facade_and_history(tmp_path):
    cfg = Config(history_csv=str(tmp_path / "h.csv"), autosave=True)
    facade = CalculatorFacade(cfg)
    res = facade.perform("+", ["1","2","3"])
    assert res == 6.0
    assert len(facade.history.df) == 1
    facade.history.undo()
    assert len(facade.history.df) == 0
    facade.history.redo()
    assert len(facade.history.df) == 1
