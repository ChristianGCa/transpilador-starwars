import unittest

from starwars.errors import CompilerError, ErrorKind
from starwars.lexer import tokenize
from starwars.tokens import TokenKind


def kinds(source):
    return [token.kind.name for token in tokenize(source)]


class LexerTest(unittest.TestCase):
    def test_longest_match_and_word_boundary(self):
        self.assertEqual(kinds("LOGOUTx >= > <= < == = != -> -"),
                         ["ID", "GE", "GT", "LE", "LT", "EQ", "ASSIGN", "NEQ", "ARROW", "MINUS", "EOF"])

    def test_thematic_phrase_keeps_original_lexeme(self):
        token = tokenize("Que a força esteja com você")[0]
        self.assertEqual((token.kind, token.lexeme), (TokenKind.PLUS, "Que a força esteja com você"))

    def test_thematic_phrases_for_begin_end_and_not_equal(self):
        phrases = {
            "Há muito tempo, em uma galáxia muito, muito distante": TokenKind.BEGIN,
            "Chewie, estamos em casa": TokenKind.END,
            "Estes não são os droides que você procura": TokenKind.NEQ,
        }
        for phrase, kind in phrases.items():
            with self.subTest(phrase=phrase):
                token = tokenize(phrase)[0]
                self.assertEqual((token.kind, token.lexeme), (kind, phrase))

    def test_thematic_program_matches_symbolic_program(self):
        thematic = ("Há muito tempo, em uma galáxia muito, muito distante\n"
                    "Faça, ou não faça (1 Estes não são os droides que você procura 2)\n"
                    "Chewie, estamos em casa\nChewie, estamos em casa")
        self.assertEqual(kinds(thematic), kinds("INICIA_SISTEMA Faça, ou não faça (1 != 2) LOGOUT LOGOUT"))

    def test_for_keywords(self):
        self.assertEqual(kinds("This is the way (i de 1 até n)"),
                         ["FOR", "LPAREN", "ID", "FROM", "NUM", "TO", "ID", "RPAREN", "EOF"])

    def test_function_keywords(self):
        self.assertEqual(kinds("Execute a ordem 66 dobro(x: y) Palpatine retornou x;"),
                         ["FUNCTION", "ID", "LPAREN", "ID", "COLON", "ID", "RPAREN", "RETURN", "ID",
                          "SEMI", "EOF"])

    def test_for_keywords_respect_word_boundary(self):
        self.assertEqual(kinds("desde ate atéque de_novo"), ["ID", "ID", "ID", "ID", "EOF"])

    def test_comments_and_line_breaks(self):
        self.assertEqual(kinds("INICIA_SISTEMA\r\n# comentario\rLOGOUT"), kinds("INICIA_SISTEMA\nLOGOUT"))
        with self.assertRaises(CompilerError) as caught:
            tokenize("INICIA_SISTEMA\r\n# comentario\r@")
        self.assertEqual((caught.exception.kind, caught.exception.line, caught.exception.column),
                         (ErrorKind.LEXICAL, 3, 1))

    def test_invalid_strings(self):
        for text in ('"sem fim', '"linha\nquebrada"', r'"escape\q"'):
            with self.subTest(text=text):
                with self.assertRaises(CompilerError) as caught:
                    tokenize(text)
                self.assertEqual(caught.exception.kind, ErrorKind.LEXICAL)

    def test_lexical_error_column(self):
        with self.assertRaises(CompilerError) as caught:
            tokenize("x = @")
        self.assertEqual((caught.exception.line, caught.exception.column), (1, 5))

    def test_lexical_error_message(self):
        with self.assertRaises(CompilerError) as caught:
            tokenize("@")
        self.assertEqual(str(caught.exception), "ERRO LÉXICO (linha 1, coluna 1): caractere inválido '@'")

    def test_lines_and_columns(self):
        tokens = tokenize("x = 1;\r\n  ação: y")
        self.assertEqual([(t.lexeme, t.line, t.column) for t in tokens], [
            ("x", 1, 1), ("=", 1, 3), ("1", 1, 5), (";", 1, 6),
            ("ação", 2, 3), (":", 2, 7), ("y", 2, 9), (None, 2, 10),
        ])


if __name__ == "__main__":
    unittest.main()
