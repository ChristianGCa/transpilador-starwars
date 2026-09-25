import unittest

from support import EXAMPLES, compile_and_run, read
from starwars import CompilerError, ErrorKind, transpile

VALID = EXAMPLES / "valid"
INVALID = EXAMPLES / "invalid"
GENERATED = EXAMPLES / "generated"
SOURCES = {
    "01_hello_world": VALID / "01_hello_world.starwars",
    "02_if_else": VALID / "02_if_else.starwars",
    "03_while_for": VALID / "03_while_for.starwars",
    "04_input_expressions": VALID / "04_input_expressions.starwars",
    "05_functions": VALID / "05_functions.starwars",
    "06_rogue_squadron": VALID / "06_rogue_squadron.starwars",
}
INVALID_KINDS = {
    "01_lexical_error": ErrorKind.LEXICAL,
    "02_syntax_error": ErrorKind.SYNTAX,
    "03_semantic_error": ErrorKind.SEMANTIC,
    "04_redeclaration_error": ErrorKind.SEMANTIC,
    "05_type_error": ErrorKind.SEMANTIC,
    "06_scope_error": ErrorKind.SEMANTIC,
    "07_loop_variable_error": ErrorKind.SEMANTIC,
    "08_argument_error": ErrorKind.SEMANTIC,
}


class ExamplesTest(unittest.TestCase):
    def test_generated_c_matches_sources(self):
        for name, source in SOURCES.items():
            with self.subTest(name=name):
                self.assertEqual(transpile(read(source)), read(GENERATED / f"{name}.c"))

    def test_valid_examples_produce_expected_output(self):
        for name in SOURCES:
            with self.subTest(name=name):
                stdin_file = VALID / f"{name}.input.txt"
                stdin = read(stdin_file) if stdin_file.exists() else ""
                result = compile_and_run(self, transpile(read(SOURCES[name])), stdin)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, read(VALID / f"{name}.expected.txt"))

    def test_if_else_example_else_branch(self):
        result = compile_and_run(self, transpile(read(SOURCES["02_if_else"])), "2\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Nível do cristal kyber (0 a 10): \nnível + 3 * 4 = 14\n"
                                        "(nível + 3) * 4 = 20\n"
                                        "O cristal ainda está fraco: são necessários 40 de energia.\n")

    def test_invalid_examples(self):
        self.assertEqual(sorted(path.stem for path in INVALID.glob("*.starwars")), sorted(INVALID_KINDS))
        for name, kind in INVALID_KINDS.items():
            with self.subTest(name=name):
                with self.assertRaises(CompilerError) as caught:
                    transpile(read(INVALID / f"{name}.starwars"))
                self.assertEqual(caught.exception.kind, kind)


if __name__ == "__main__":
    unittest.main()
