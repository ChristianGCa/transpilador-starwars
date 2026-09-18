import unittest

from support import program
from starwars.errors import CompilerError, ErrorKind
from starwars.lexer import tokenize
from starwars.parser import Parser


def parse(body):
    return Parser(tokenize(program(body))).parse_program()


class ParserTest(unittest.TestCase):
    def test_precedence(self):
        expression = parse("Hello There (2 + 3 * 4);").statements[0].items[0]
        self.assertEqual((expression.op, expression.right.op), ("+", "*"))
        grouped = parse("Hello There ((2 + 3) * 4);").statements[0].items[0]
        self.assertEqual((grouped.op, grouped.left.op), ("*", "+"))

    def test_thematic_operators_become_c_symbols(self):
        expression = parse("Hello There (1 Que a força esteja com você 2 Eu sou todos os jedi 3);")
        self.assertEqual(expression.statements[0].items[0].op, "+")
        condition = parse("Faça, ou não faça (1 A força é forte nele 2) LOGOUT").statements[0].condition
        self.assertEqual(condition.op, ">=")

    def test_declaration_forms(self):
        first, second = parse("x: Você era o escolhido = 1; "
                              "Eu sou C3PO, ciborgue de relações humanas y;").statements
        self.assertEqual((first.type_name, first.name, first.init.text), ("int", "x", "1"))
        self.assertEqual((second.type_name, second.name, second.init), ("float", "y", None))

    def test_node_positions(self):
        read = parse("x: Você era o escolhido;\n  Ajude-me Obi-Wan Kenobi (x);").statements[1]
        self.assertEqual((read.line, read.column), (3, 3))

    def test_readable_error_messages(self):
        cases = {
            program("x = 1"): "esperado ';', encontrado 'LOGOUT'",
            program("Hello There (1"): "esperado ')', encontrado 'LOGOUT'",
            "INICIA_SISTEMA\nx = 1;": "esperado 'LOGOUT', encontrado fim do arquivo",
            program("x: Você era o escolhido = ;"): "esperado identificador, número ou '(', encontrado ';'",
        }
        for source, message in cases.items():
            with self.subTest(source=source):
                with self.assertRaises(CompilerError) as caught:
                    Parser(tokenize(source)).parse_program()
                self.assertEqual(caught.exception.message, message)

    def test_invalid_syntax(self):
        for body in ('Hello There ();', 'Hello There (1,);', 'x: = 1;',
                     'Ajude-me Obi-Wan Kenobi ("x" x);', 'Faça, ou não faça (1) LOGOUT',
                     'Faça, ou não faça (1 == 1)', 'Eu sinto uma perturbação na força (1 > 0)'):
            with self.subTest(body=body):
                with self.assertRaises(CompilerError) as caught:
                    parse(body)
                self.assertEqual(caught.exception.kind, ErrorKind.SYNTAX)


if __name__ == "__main__":
    unittest.main()
