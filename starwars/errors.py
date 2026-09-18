from enum import Enum


class ErrorKind(Enum):
    LEXICAL = "ERRO LÉXICO"
    SYNTAX = "ERRO SINTÁTICO"
    SEMANTIC = "ERRO SEMÂNTICO"


class CompilerError(Exception):
    def __init__(self, kind: ErrorKind, message: str, line: int, column: int):
        super().__init__(f"{kind.value} (linha {line}, coluna {column}): {message}")
        self.kind = kind
        self.message = message
        self.line = line
        self.column = column
