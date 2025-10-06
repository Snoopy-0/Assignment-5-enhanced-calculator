
"""
Input validation helpers demonstrating LBYL and EAFP styles.
"""
from __future__ import annotations
from typing import Tuple, List
from .exceptions import ValidationError

def parse_command(line: str) -> Tuple[str, List[str]]:
    if not line:
        raise ValidationError("Empty input")
    parts = line.strip().split()
    cmd, args = parts[0].lower(), parts[1:]
    return cmd, args

def parse_operation_args(args: List[str]) -> List[float]:
    # LBYL: check before converting
    if not args:
        raise ValidationError("No operands provided")
    try:
        return [float(x) for x in args]
    except ValueError as exc:
        raise ValidationError("All operands must be numeric") from exc
