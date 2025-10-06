
import pytest
from app.operations import operation_factory, Add, Subtract, Multiply, Divide, Power, Root
from app.exceptions import OperationError

def test_factory_success():
    assert isinstance(operation_factory("+"), Add)
    assert isinstance(operation_factory("-"), Subtract)
    assert isinstance(operation_factory("*"), Multiply)
    assert isinstance(operation_factory("/"), Divide)
    assert isinstance(operation_factory("^"), Power)
    assert isinstance(operation_factory("root"), Root)

def test_factory_failure():
    with pytest.raises(OperationError):
        operation_factory("%")
