
"""
Custom exception types for the calculator app.
"""
class CalculatorError(Exception):
    """Base exception for calculator-related errors."""

class ConfigurationError(CalculatorError):
    """Raised when configuration is invalid or missing required keys."""

class OperationError(CalculatorError):
    """Raised for invalid operations or operation execution failures."""

class ValidationError(CalculatorError):
    """Raised when input validation fails."""

class UndoRedoError(CalculatorError):
    """Raised for invalid undo/redo actions."""
