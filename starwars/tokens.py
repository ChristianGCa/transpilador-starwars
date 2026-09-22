from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple


class TokenKind(Enum):
    BEGIN = "'INICIA_SISTEMA'"
    END = "'LOGOUT'"
    INT_TYPE = "'Você era o escolhido'"
    FLOAT_TYPE = "'Eu sou C3PO, ciborgue de relações humanas'"
    IF = "'Faça, ou não faça'"
    ELSE = "'Tentativa não há'"
    WHILE = "'Eu sinto uma perturbação na força'"
    FOR = "'This is the way'"
    FROM = "'de'"
    TO = "'até'"
    PRINT = "'Hello There'"
    INPUT = "'Ajude-me Obi-Wan Kenobi'"
    ASSIGN = "'='"
    PLUS = "'+'"
    MINUS = "'-'"
    STAR = "'*'"
    SLASH = "'/'"
    EQ = "'=='"
    NEQ = "'!='"
    GT = "'>'"
    GE = "'>='"
    LT = "'<'"
    LE = "'<='"
    ARROW = "'->'"
    LPAREN = "'('"
    RPAREN = "')'"
    SEMI = "';'"
    COLON = "':'"
    COMMA = "','"
    ID = "identificador"
    NUM = "número"
    STRING = "texto"
    EOF = "fim do arquivo"


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    lexeme: Optional[str]
    line: int
    column: int

    def __repr__(self) -> str:
        return f"[{self.kind.name}:{self.lexeme}]"


KEYWORD_PHRASES: List[Tuple[TokenKind, str]] = sorted([
    (TokenKind.BEGIN, "INICIA_SISTEMA"),
    (TokenKind.BEGIN, "Há muito tempo, em uma galáxia muito, muito distante"),
    (TokenKind.END, "LOGOUT"),
    (TokenKind.END, "Chewie, estamos em casa"),
    (TokenKind.NEQ, "Estes não são os droides que você procura"),
    (TokenKind.INT_TYPE, "Você era o escolhido"),
    (TokenKind.FLOAT_TYPE, "Eu sou C3PO, ciborgue de relações humanas"),
    (TokenKind.ASSIGN, "Eu alterei o acordo"),
    (TokenKind.PLUS, "Que a força esteja com você"),
    (TokenKind.MINUS, "Acabou anakin"),
    (TokenKind.STAR, "Eu sou todos os jedi"),
    (TokenKind.SLASH, "Eu sou todos os sith"),
    (TokenKind.EQ, "Como deve ser"),
    (TokenKind.GT, "I have the high ground"),
    (TokenKind.GE, "A força é forte nele"),
    (TokenKind.LT, "Você subestima meu poder"),
    (TokenKind.LE, "Não, eu sou seu pai"),
    (TokenKind.IF, "Faça, ou não faça"),
    (TokenKind.ELSE, "Tentativa não há"),
    (TokenKind.PRINT, "Hello There"),
    (TokenKind.INPUT, "Ajude-me Obi-Wan Kenobi"),
    (TokenKind.WHILE, "Eu sinto uma perturbação na força"),
    (TokenKind.FOR, "This is the way"),
    (TokenKind.FROM, "de"),
    (TokenKind.TO, "até"),
], key=lambda entry: -len(entry[1]))

ARITHMETIC_OPERATORS: Dict[TokenKind, str] = {
    TokenKind.PLUS: "+", TokenKind.MINUS: "-", TokenKind.STAR: "*", TokenKind.SLASH: "/",
}

COMPARISON_OPERATORS: Dict[TokenKind, str] = {
    TokenKind.EQ: "==", TokenKind.NEQ: "!=", TokenKind.GT: ">",
    TokenKind.GE: ">=", TokenKind.LT: "<", TokenKind.LE: "<=",
}
