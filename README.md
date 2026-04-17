# WhileLang Compiler

Este proyecto implementa un compilador básico para el lenguaje WhileLang utilizando ANTLR4 y Python, con énfasis en el análisis semántico.

## Estructura del Proyecto

- `src/grammar/`: Gramática ANTLR4 y archivos generados.
- `src/semantic/`: Tabla de símbolos y visitor semántico.
- `tests/`: Pruebas unitarias y casos de ejemplo.

## Instalación

1. Instalar ANTLR4: `pip install antlr4-tools`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Generar archivos: `cd src/grammar && antlr4 -Dlanguage=Python3 WhileLang.g4`

## Uso

Ejecutar análisis semántico: `python src/main.py tests/test_cases/valid_program.wl`

Ejecutar pruebas: `python -m unittest tests/test_semantic.py`