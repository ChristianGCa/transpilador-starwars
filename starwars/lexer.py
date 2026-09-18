from __future__ import annotations

import re
from typing import List, Optional, Tuple

from .errors import CompilerError, ErrorKind
from .tokens import KEYWORD_PHRASES, Token, TokenKind

LETTER = "A-Za-z_À-ÖØ-öø-ÿ"
IDENTIFIER_CHAR = re.compile(f"[{LETTER}0-9]")

SIMPLE_PATTERNS = [
    ("SKIP", r"[ \t]+"),
    ("NEWLINE", r"\r\n|\r|\n"),
    ("COMMENT", r"#[^\r\n]*"),
    ("NUM", r"[0-9]+(\.[0-9]+)?"),
    ("STRING", r'"(?:[^"\\\x00-\x1f\x7f]|\\["\\nrt])*"'),
    ("ARROW", r"->"),
    ("EQ", r"=="),
    ("NEQ", r"!="),
    ("GE", r">="),
    ("LE", r"<="),
    ("GT", r">"),
    ("LT", r"<"),
    ("ASSIGN", r"="),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("STAR", r"\*"),
    ("SLASH", r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("SEMI", r";"),
    ("COLON", r":"),
    ("COMMA", r","),
    ("ID", f"[{LETTER}][{LETTER}0-9]*"),
]
SIMPLE_TOKEN = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in SIMPLE_PATTERNS))
IGNORED = {"SKIP", "COMMENT"}


def tokenize(source: str) -> List[Token]:
    tokens = []
    line, line_start, pos = 1, 0, 0
    while pos < len(source):
        column = pos - line_start + 1
        keyword = _match_keyword(source, pos)
        if keyword is not None:
            kind, phrase = keyword
            tokens.append(Token(kind, phrase, line, column))
            pos += len(phrase)
            continue
        match = SIMPLE_TOKEN.match(source, pos)
        if match is None:
            raise CompilerError(ErrorKind.LEXICAL, f"caractere invalido '{source[pos]}'", line)
        name, pos = match.lastgroup, match.end()
        if name == "NEWLINE":
            line, line_start = line + 1, pos
        elif name not in IGNORED:
            tokens.append(Token(TokenKind[name], match.group(), line, column))
    tokens.append(Token(TokenKind.EOF, None, line, pos - line_start + 1))
    return tokens


def _match_keyword(source: str, pos: int) -> Optional[Tuple[TokenKind, str]]:
    for kind, phrase in KEYWORD_PHRASES:
        end = pos + len(phrase)
        if source.startswith(phrase, pos) and not IDENTIFIER_CHAR.match(source, end):
            return kind, phrase
    return None
