import pytest
from app.exceptions import UndoRedoError, ValidationError, OperationError

def test_undo_redo_error_message():
    err = UndoRedoError("Nothing to undo")
    assert "Nothing to undo" in str(err)

def test_validation_error_message():
    err = ValidationError("Invalid data")
    assert "Invalid data" in str(err)

def test_operation_error_message():
    err = OperationError("Cannot divide by zero")
    assert "Cannot divide by zero" in str(err)

def test_exceptions_are_subclasses_of_exception():
    for exc in (UndoRedoError, ValidationError, OperationError):
        assert issubclass(exc, Exception)
