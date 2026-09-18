import unittest

from starwars.tokens import (ARITHMETIC_OPERATORS, COMPARISON_OPERATORS, KEYWORD_PHRASES,
                             Token, TokenKind)


class TokensTest(unittest.TestCase):
    def test_keyword_phrases_are_longest_first(self):
        lengths = [len(phrase) for _, phrase in KEYWORD_PHRASES]
        self.assertEqual(lengths, sorted(lengths, reverse=True))

    def test_thematic_operators_map_to_c_symbols(self):
        symbols = {**ARITHMETIC_OPERATORS, **COMPARISON_OPERATORS}
        thematic = {kind: symbols[kind] for kind, _ in KEYWORD_PHRASES if kind in symbols}
        self.assertEqual(thematic, {
            TokenKind.PLUS: "+", TokenKind.MINUS: "-", TokenKind.STAR: "*", TokenKind.SLASH: "/",
            TokenKind.EQ: "==", TokenKind.GT: ">", TokenKind.GE: ">=", TokenKind.LT: "<",
            TokenKind.LE: "<=",
        })

    def test_repr_shows_kind_and_lexeme(self):
        self.assertEqual(repr(Token(TokenKind.BEGIN, "INICIA_SISTEMA", 1, 1)), "[BEGIN:INICIA_SISTEMA]")


if __name__ == "__main__":
    unittest.main()
