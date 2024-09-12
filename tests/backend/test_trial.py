import pytest
from dela1 import add, subtract

def test_add():
    result = add(4, 10)
    assert result == 14

def test_subtract():
    result = subtract(14, 10)
    assert result == 4