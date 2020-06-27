from exceptions import InvalidOperation
from tests.utils import PymboTest


class TestClass(PymboTest):
    def testEmptyClass(self):
        code = """
        class A:
            pass
        def main():
            return True
        """
        self.translate(code)

    def testClassAttrLoad(self):
        code = """
        class A:
            b = True
        def main():
            return A.b
        """
        self.translate(code)

    def testClassAttrStore(self):
        code = """
        class A:
            b = False
        def main():
            A.b = True
            return A.b
        """
        self.translate(code)

    def testInheritance_not_allowed(self):
        code = """
        class A(str):
            pass
        def main():
            return True
        """
        self.check_raises(code, InvalidOperation)

    def testMetaClass_not_allowed(self):
        code = """
        class A(metaclass="B"):
            pass
        def main():
            return True
        """
        self.check_raises(code, InvalidOperation)
