
import pytest
from app.input_validators import parse_command, parse_operation_args
from app.exceptions import ValidationError

def test_parse_command_and_args():
    cmd, args = parse_command("+ 1 2 3")
    assert cmd == "+" and args == ["1","2","3"]
    with pytest.raises(ValidationError):
        parse_command("")
    assert parse_operation_args(["1","2"]) == [1.0, 2.0]
    with pytest.raises(ValidationError):
        parse_operation_args([])
    with pytest.raises(ValidationError):
        parse_operation_args(["x"])
