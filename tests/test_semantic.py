import unittest

from support import program
from starwars.errors import CompilerError, ErrorKind
from starwars.lexer import tokenize
from starwars.parser import Parser
from starwars.semantic import SemanticAnalyzer

INT_DECL = "Você era o escolhido"
FLOAT_DECL = "Eu sou C3PO, ciborgue de relações humanas"


def check(body):
    tree = Parser(tokenize(program(body))).parse_program()
    SemanticAnalyzer().check(tree)
    return tree


class SemanticTest(unittest.TestCase):
    def assert_semantic_error(self, body, message):
        with self.assertRaises(CompilerError) as caught:
            check(body)
        self.assertEqual(caught.exception.kind, ErrorKind.SEMANTIC)
        self.assertIn(message, caught.exception.message)
        return caught.exception

    def test_undeclared_variables(self):
        for body in ("Ajude-me Obi-Wan Kenobi (x);", f"x: {INT_DECL} = x;", f"x: {FLOAT_DECL} = y;",
                     "Hello There (x);", "Faça, ou não faça (x == 1) LOGOUT",
                     "Eu sinto uma perturbação na força (x > 0) LOGOUT"):
            with self.subTest(body=body):
                self.assert_semantic_error(body, "nao declarada")

    def test_redeclaration_in_same_scope(self):
        self.assert_semantic_error(f"x: {INT_DECL}; x: {INT_DECL};", "ja declarada")

    def test_float_is_not_assignable_to_int(self):
        for body in (f"x: {INT_DECL} = 1.5;", f"{INT_DECL} x Eu alterei o acordo 1.5;",
                     f"x: {INT_DECL}; x = 1 + 1.5;"):
            with self.subTest(body=body):
                self.assert_semantic_error(body, "incompatibilidade de tipos")

    def test_int_is_assignable_to_float(self):
        check(f"x: {FLOAT_DECL} = 2; x = x + 0.5;")

    def test_scope_does_not_leak(self):
        for block in (f"Faça, ou não faça (1 == 1) x: {INT_DECL}; LOGOUT",
                      f"Faça, ou não faça (1 == 0) Tentativa não há x: {INT_DECL}; LOGOUT",
                      f"Eu sinto uma perturbação na força (1 == 0) x: {INT_DECL}; LOGOUT"):
            with self.subTest(block=block):
                self.assert_semantic_error(block + " Hello There (x);", "nao declarada")
        self.assert_semantic_error(f"Faça, ou não faça (1 == 1) x: {INT_DECL}; "
                                   "Tentativa não há Hello There (x); LOGOUT", "nao declarada")

    def test_literal_limits(self):
        for literal in ("2147483648", "9" * 5000, "9" * 40 + ".0"):
            with self.subTest(size=len(literal)):
                self.assert_semantic_error(f"Hello There ({literal});", "fora do intervalo")
        check("Hello There (2147483647);")

    def test_annotates_types_and_c_names(self):
        declaration, output = check(f"x: {INT_DECL}; Hello There (x + 1.5);").statements
        expression = output.items[0]
        self.assertEqual(declaration.c_name, "sw_v0")
        self.assertEqual((expression.type_name, expression.left.c_name), ("float", "sw_v0"))

    def test_error_position(self):
        error = self.assert_semantic_error("Hello There (1);\n  x = 2;", "nao declarada")
        self.assertEqual((error.line, error.column), (3, 3))


if __name__ == "__main__":
    unittest.main()
