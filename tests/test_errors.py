import unittest

from starwars.errors import CompilerError, ErrorKind


class CompilerErrorTest(unittest.TestCase):
    def test_message_includes_kind_and_line(self):
        error = CompilerError(ErrorKind.SYNTAX, "esperado ';'", 3, 7)
        self.assertEqual(str(error), "ERRO SINTATICO (linha 3, coluna 7): esperado ';'")
        self.assertEqual((error.kind, error.message, error.line, error.column),
                         (ErrorKind.SYNTAX, "esperado ';'", 3, 7))


if __name__ == "__main__":
    unittest.main()
