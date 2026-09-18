from enum import Enum


class ErrorKind(Enum):
    LEXICAL = "ERRO LEXICO"
    SYNTAX = "ERRO SINTATICO"
    SEMANTIC = "ERRO SEMANTICO"


class CompilerError(Exception):
    def __init__(self, kind: ErrorKind, message: str, line: int):
        super().__init__(f"{kind.value} (linha {line}): {message}")
        self.kind = kind
        self.message = message
        self.line = line
