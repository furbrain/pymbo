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

    def testClassInstanceCreate(self):
        code = """
        class A:
            def __init__(self, retval):
                self.b = retval
                
        def main():
            a = A(True)
            return a.b
        """
        self.translate(code)

    def testClassInstanceAttrCreate(self):
        code = """
        class A:
            pass

        def main():
            a = A()
            a.b = True
            return a.b
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
