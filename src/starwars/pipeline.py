from __future__ import annotations

from typing import List, Tuple

from .codegen import generate_c
from .lexer import tokenize
from .nodes import Program
from .parser import Parser
from .semantic import SemanticAnalyzer
from .tokens import Token


def build_program(tokens: List[Token]) -> Program:
    program = Parser(tokens).parse_program()
    SemanticAnalyzer().check(program)
    return program


def analyze(source: str) -> Tuple[List[Token], Program]:
    tokens = tokenize(source)
    return tokens, build_program(tokens)


def transpile(source: str) -> str:
    _, program = analyze(source)
    return generate_c(program)
