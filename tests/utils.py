import os
import subprocess
import textwrap
import unittest
from typing import Type

import pymbo
from itypes.typedb import TypeDB

BUILDING = True


class PymboTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        result_dir = os.path.join(dir_path, "results")
        cls.build_dir = os.path.join(dir_path, 'build', cls.__name__)
        os.makedirs(result_dir, exist_ok=True)
        os.makedirs(cls.build_dir, exist_ok=True)
        cls.results_file = open(os.path.join(result_dir, cls.__name__ + ".c"), "w")

    @classmethod
    def tearDownClass(cls) -> None:
        # noinspection PyUnresolvedReferences
        cls.results_file.close()

    def setUp(self) -> None:
        TypeDB.reset()

    def translate(self, text: str) -> str:
        text = textwrap.dedent(text)
        commented_original = textwrap.indent(self.id() + '\n\n' + text, "// ")
        self.results_file.write(commented_original)
        compiled_code = pymbo.convert(textwrap.dedent(text))
        self.results_file.write(compiled_code + '\n/*======================*/\n')
        return self.compile_and_run(compiled_code)

    def compile_and_run(self, compiled_code):
        c_name = os.path.join(self.build_dir, f"{self.id()}.c")
        exe_name = os.path.join(self.build_dir, f"{self.id()}.exe")
        with open(c_name, 'w') as c_file:
            c_file.write(compiled_code)
        self.assertEqual(0, os.system(f"gcc {c_name} -o {exe_name}"), "Compile Failed")
        result = subprocess.run(exe_name, stdout=subprocess.PIPE)
        self.assertEqual(1, result.returncode, "Final code does not return True")
        if result.stdout:
            return str(result.stdout, encoding="utf-8")
        return ""

    def check_raises(self, text: str, exc: Type[Exception]):
        text = textwrap.dedent(text)
        with self.assertRaises(exc):
            pymbo.convert(textwrap.dedent(text))
