
import os, pandas as pd, pytest, tempfile
from app.history import History
from app.exceptions import ValidationError
from app.calculator_memento import HistoryMemento

def test_history_add_clear_undo_redo(tmp_path):
    csv = tmp_path / "h.csv"
    h = History(csv_path=str(csv), autosave=True)
    h.add_record("+", [1,2], 3.0)
    assert len(h.df) == 1
    # undo
    h.undo()
    assert len(h.df) == 0
    # redo
    h.redo()
    assert len(h.df) == 1
    # clear
    h.clear()
    assert len(h.df) == 0
    # save/load
    h.add_record("*", [2,3], 6.0)
    h.save()
    assert os.path.exists(csv)
    h2 = History(csv_path=str(csv), autosave=False)
    assert len(h2.df) == 1
    # memento serialization
    mem = HistoryMemento.from_df(h2.df)
    df2 = mem.to_df()
    assert len(df2) == 1

def test_history_validation(tmp_path):
    h = History(csv_path=str(tmp_path / "x.csv"), autosave=False)
    with pytest.raises(ValidationError):
        h.add_record(None, [1], 1.0)
    with pytest.raises(ValidationError):
        h.save("")  # no configured path
