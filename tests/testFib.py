from tests.utils import PymboTest

TEST_CODE = """
def fib(a,b):
    if a>0:
        return a + b
    else:
        return a-b

def main():
    c = fib(1,2)
    return 1
"""


class TestFibonacci(PymboTest):
    def test_conversion(self):
        self.translate(TEST_CODE)
