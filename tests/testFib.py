import unittest
import pymbo
from tests.utils import PymboTest

TEST_CODE = """
def fib(a,b):
    if a>0:
        return a + b
    else:
        return a-b

def main():
    fib(1,2)
    return 0
"""


class TestFibonacci(PymboTest):
    def test_conversion(self):
        self.translate(TEST_CODE)
