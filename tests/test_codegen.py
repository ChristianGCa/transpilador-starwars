import unittest

from support import compile_and_run, program
from starwars.pipeline import transpile
from starwars.tokens import COMPARISON_OPERATORS, KEYWORD_PHRASES

INT_DECL = "Você era o escolhido"
FLOAT_DECL = "Eu sou C3PO, ciborgue de relações humanas"


class CodegenTest(unittest.TestCase):
    def run_program(self, body, stdin=""):
        return compile_and_run(self, transpile(program(body)), stdin)

    def assert_output(self, body, expected, stdin=""):
        result = self.run_program(body, stdin)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, expected)

    def test_arithmetic_and_associativity(self):
        self.assert_output('Hello There (2 + 3 * 4, ",", (2 + 3) * 4, ",", 8 / 3, ",", 8 / 2.0);\n'
                           'Hello There (10 - 3 - 2, ",", 20 / 2 / 2);', "14,20,2,4\n5,5\n")

    def test_thematic_arithmetic_operators(self):
        self.assert_output("Hello There ((10 Acabou anakin 2) Eu sou todos os sith 2 "
                           "Que a força esteja com você 3 Eu sou todos os jedi 2);", "10\n")

    def test_comparison_operators(self):
        phrases = dict(KEYWORD_PHRASES)
        for kind, symbol in COMPARISON_OPERATORS.items():
            expected = "sim" if symbol in ("!=", ">", ">=") else "nao"
            for operator in {phrases.get(kind, symbol), symbol}:
                with self.subTest(operator=operator):
                    self.assert_output(f'Faça, ou não faça (2 {operator} 1) Hello There ("sim"); '
                                       'Tentativa não há Hello There ("nao"); LOGOUT', expected)

    def test_nested_blocks_update_outer_variable(self):
        self.assert_output(f"x: {INT_DECL} = 2; total: {INT_DECL};\n"
                           "Eu sinto uma perturbação na força (x > 0)\n"
                           f"local: {INT_DECL} = x;\n"
                           "Faça, ou não faça (local == 2) total = total + 10;\n"
                           "Tentativa não há total = total + 1; LOGOUT\n"
                           "x = x - 1; LOGOUT Hello There (total);", "11\n")

    def test_shadowing_uses_outer_value_in_initializer(self):
        self.assert_output(f"x: {INT_DECL} = 7;\n"
                           "Faça, ou não faça (1 == 1)\n"
                           f"x: {INT_DECL} = x + 1; Hello There (x);\n"
                           f"Tentativa não há x: {INT_DECL} = 2; Hello There (x); LOGOUT\n"
                           "Hello There (x);", "8\n7\n")

    def test_for_counts_inclusive_range(self):
        self.assert_output("This is the way (i de 0 - 1 até 2) Hello There (i); LOGOUT", "-1\n0\n1\n2\n")

    def test_for_with_empty_range(self):
        self.assert_output('This is the way (i de 5 até 1) Hello There (i); LOGOUT '
                           'Hello There ("fim");', "fim")

    def test_for_evaluates_stop_once(self):
        self.assert_output(f"n: {INT_DECL} = 3; voltas: {INT_DECL};\n"
                           "This is the way (i de 1 até n) n = n + 1; voltas = voltas + 1; LOGOUT\n"
                           'Hello There (voltas, ",", n);', "3,6\n")

    def test_nested_for_loops(self):
        self.assert_output("This is the way (i de 1 até 2) This is the way (j de i até 2) "
                           'Hello There (i, "x", j); LOGOUT LOGOUT', "1x1\n1x2\n2x2\n")

    def test_int_float_and_prompt_input(self):
        self.assert_output(f"i: {INT_DECL}; r: {FLOAT_DECL};\n"
                           'Ajude-me Obi-Wan Kenobi (i); Ajude-me Obi-Wan Kenobi ("Real: " -> r);\n'
                           'Hello There (i, ",", r);', "Real: -2,1.5\n", "-2\n1.5\n")

    def test_invalid_input_and_eof(self):
        for stdin in ("abc", ""):
            with self.subTest(stdin=stdin):
                result = self.run_program(f"x: {INT_DECL}; Ajude-me Obi-Wan Kenobi (x);", stdin)
                self.assertEqual(result.returncode, 1)
                self.assertIn("ERRO DE ENTRADA", result.stderr)

    def test_float_promotion(self):
        self.assert_output(f"x: {FLOAT_DECL} = 2; x = x + 0.5; Hello There (x);", "2.5\n")

    def test_default_initialization(self):
        self.assert_output(f'x: {INT_DECL}; r: {FLOAT_DECL}; Hello There (x, ",", r);', "0,0\n")

    def test_text_percent_escapes_and_trigraph(self):
        self.assert_output(r'Hello There ("100% de energia %n ??/ \\", "\"jedi\"\n\t");',
                           '100% de energia %n ??/ \\"jedi"\n\t')

    def test_safe_names_and_leading_zeros(self):
        self.assert_output(f"return: {INT_DECL} = 08; printf: {INT_DECL} = 010; "
                           f"LOGOUTx: {INT_DECL} = 2; ação: {INT_DECL} = 3; "
                           "Hello There (return + printf + LOGOUTx + ação);", "23\n")

    def test_largest_int_literal(self):
        self.assert_output("Hello There (2147483647);", "2147483647\n")


if __name__ == "__main__":
    unittest.main()
