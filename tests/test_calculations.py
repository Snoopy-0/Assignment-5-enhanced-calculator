
import pytest
from app.calculation import Calculation
from app.operations import Add, Subtract, Multiply, Divide, Power, Root
from app.exceptions import OperationError

@pytest.mark.parametrize("operands,expected", [([1,2,3], 6.0), ([], 0.0)])
def test_addition(operands, expected):
    calc = Calculation("+", operands, Add())
    assert pytest.approx(calc.perform()) == expected

@pytest.mark.parametrize("operands,expected", [([10,2,3], 5.0), ([5], 5.0)])
def test_subtraction(operands, expected):
    calc = Calculation("-", operands, Subtract())
    assert pytest.approx(calc.perform()) == expected

@pytest.mark.parametrize("operands,expected", [([2,3,4], 24.0), ([7], 7.0)])
def test_multiplication(operands, expected):
    calc = Calculation("*", operands, Multiply())
    assert pytest.approx(calc.perform()) == expected

def test_division_and_zero():
    assert Calculation("/", [8,2], Divide()).perform() == 4.0
    with pytest.raises(OperationError):
        Calculation("/", [1,0], Divide()).perform()

def test_power():
    assert Calculation("^", [2,3], Power()).perform() == 8.0
    with pytest.raises(OperationError):
        Calculation("^", [2], Power()).perform()

def test_root():
    assert Calculation("root", [2,9], Root()).perform() == 3.0
    with pytest.raises(OperationError):
        Calculation("root", [0,9], Root()).perform()
