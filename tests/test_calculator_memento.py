
import pandas as pd, pytest
from app.calculator_memento import HistoryMemento, Caretaker
from app.exceptions import UndoRedoError

def test_memento_roundtrip_and_stacks():
    df = pd.DataFrame({"operator": ["+"], "operands": [[1,2]], "result": [3.0]})
    mem = HistoryMemento.from_df(df)
    df2 = mem.to_df()
    assert len(df2) == 1
    ct = Caretaker()
    ct.push(mem)
    with pytest.raises(UndoRedoError):
        ct.redo(mem)  # nothing to redo initially
    cur = HistoryMemento.from_df(pd.DataFrame())
    prev = ct.undo(cur)
    assert isinstance(prev, HistoryMemento)
