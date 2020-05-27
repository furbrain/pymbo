import unittest
import pymbo

BASIC_TEST = """
def main():
    return 1+2
"""

class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(pymbo.convert(BASIC_TEST))

if __name__ == '__main__':
    unittest.main()
