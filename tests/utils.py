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
        cls.dirname = os.path.dirname(os.path.realpath(__file__))
        cls.build_dir = os.path.join(cls.dirname, 'build', cls.__name__)
        os.makedirs(cls.build_dir, exist_ok=True)

    def setUp(self) -> None:
        TypeDB.reset()

    def translate(self, text: str, check_result=True) -> str:
        text = textwrap.dedent(text)
        compiled_code = pymbo.convert(textwrap.dedent(text))
        return self.compile_and_run(compiled_code, check_result)

    def compile_and_run(self, compiled_code, check_result=True):
        c_name = os.path.join(self.build_dir, f"{self.id()}.c")
        exe_name = os.path.join(self.build_dir, f"{self.id()}.exe")
        library_dir = os.path.join(self.dirname, '..', 'c_libraries')
        with open(c_name, 'w') as c_file:
            c_file.write(compiled_code)
        self.assertEqual(0, os.system(f'gcc -I {library_dir} "{library_dir}/CException.c" {c_name} -o {exe_name}'),
                         "Compile Failed")
        result = subprocess.run(exe_name, stdout=subprocess.PIPE)
        if check_result:
            self.assertEqual(1, result.returncode, "Final code does not return True")
        if result.stdout:
            return str(result.stdout, encoding="utf-8")
        return ""

    def check_raises(self, text: str, exc: Type[Exception]):
        text = textwrap.dedent(text)
        with self.assertRaises(exc):
            pymbo.convert(textwrap.dedent(text))
