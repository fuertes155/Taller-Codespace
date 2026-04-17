#!/usr/bin/env python3

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from antlr4 import *
from src.grammar.generated.WhileLangLexer import WhileLangLexer
from src.grammar.generated.WhileLangParser import WhileLangParser
from src.semantic.semantic_visitor import SemanticVisitor
from src.semantic.symbol_table import SemanticError

class TestSemanticAnalysis(unittest.TestCase):
    def analyze(self, code):
        input_stream = InputStream(code)
        lexer = WhileLangLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = WhileLangParser(stream)
        tree = parser.program()
        visitor = SemanticVisitor()
        try:
            visitor.visit(tree)
            return None  # Sin errores
        except Exception as e:
            return str(e)

    def test_valid_program(self):
        code = """
        int x = 5;
        string s = "hello";
        x = x + 1;
        if (x < 10) {
            int y = 2;
        }
        """
        result = self.analyze(code)
        self.assertIsNone(result)

    def test_case_2_assignment_string_to_int(self):
        code = "int x; x = \"hello\";"
        result = self.analyze(code)
        self.assertIn("No se puede asignar un valor de tipo 'string' a una variable de tipo 'int'", result)

    def test_case_3_undeclared_variable(self):
        code = "x = 5;"
        result = self.analyze(code)
        self.assertIn("Variable 'x' no declarada", result)

    def test_case_4_redeclaration(self):
        code = "int x; int x;"
        result = self.analyze(code)
        self.assertIn("Variable 'x' ya declarada", result)

    def test_case_5_string_in_if(self):
        code = "string s = \"test\"; if (s) {}"
        result = self.analyze(code)
        self.assertIn("La condición del 'if' debe ser de tipo 'bool'", result)

    def test_case_6_string_comparison(self):
        code = "string s1 = \"a\"; string s2 = \"b\"; if (s1 < s2) {}"
        result = self.analyze(code)
        self.assertIn("Operador '<' no definido para operandos de tipo 'string'", result)

    def test_case_10_string_arithmetic(self):
        code = "string s1 = \"a\"; string s2 = \"b\"; int x = s1 + s2;"
        result = self.analyze(code)
        self.assertIn("Operador '+' no definido para operandos de tipo 'string'", result)

if __name__ == '__main__':
    unittest.main()