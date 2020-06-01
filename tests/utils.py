import unittest
import pymbo
import textwrap
import os

class PymboTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        dirPath = os.path.dirname(os.path.realpath(__file__))
        result_dir = os.path.join(dirPath,"results")
        try:
            os.mkdir(result_dir)
        except FileExistsError:
            pass
        cls.results_file = open(os.path.join(result_dir, cls.__name__ + ".c"),"w")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.results_file.close()

    def translate(self, text: str) -> str:
        text = textwrap.dedent(text)
        commented_original = textwrap.indent(self.id()+'\n\n'+text, "// ")
        self.results_file.write(commented_original)
        compiled_code = pymbo.convert(textwrap.dedent(text))
        self.results_file.write(compiled_code+'\n/*======================*/\n')
        return compiled_code