#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from antlr4 import *
from src.grammar.generated.WhileLangLexer import WhileLangLexer
from src.grammar.generated.WhileLangParser import WhileLangParser
from src.semantic.semantic_visitor import SemanticVisitor

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo.wl>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Archivo {input_file} no encontrado.")
        sys.exit(1)

    input_stream = FileStream(input_file, encoding='utf-8')
    lexer = WhileLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = WhileLangParser(stream)
    tree = parser.program()

    visitor = SemanticVisitor()
    try:
        visitor.visit(tree)
        print("Análisis semántico completado sin errores.")
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()