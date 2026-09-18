import unittest

from support import EXAMPLES, compile_and_run, read
from starwars import CompilerError, ErrorKind, transpile

VALID = EXAMPLES / "valid"
INVALID = EXAMPLES / "invalid"
GENERATED = EXAMPLES / "generated"
SOURCES = {
    "01_basic": VALID / "01_basic.starwars",
    "02_complete": VALID / "02_complete.starwars",
    "demo": EXAMPLES / "demo.starwars",
}
INVALID_KINDS = {
    "03_lexical_error": ErrorKind.LEXICAL,
    "04_syntax_error": ErrorKind.SYNTAX,
    "05_semantic_error": ErrorKind.SEMANTIC,
    "06_redeclaration_error": ErrorKind.SEMANTIC,
    "07_type_error": ErrorKind.SEMANTIC,
    "08_scope_error": ErrorKind.SEMANTIC,
}


class ExamplesTest(unittest.TestCase):
    def test_generated_c_matches_sources(self):
        for name, source in SOURCES.items():
            with self.subTest(name=name):
                self.assertEqual(transpile(read(source)), read(GENERATED / f"{name}.c"))

    def test_valid_examples_produce_expected_output(self):
        for name in ("01_basic", "02_complete"):
            with self.subTest(name=name):
                stdin_file = VALID / f"{name}.input.txt"
                stdin = read(stdin_file) if stdin_file.exists() else ""
                result = compile_and_run(self, transpile(read(SOURCES[name])), stdin)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, read(VALID / f"{name}.expected.txt"))

    def test_complete_example_else_branch(self):
        result = compile_and_run(self, transpile(read(SOURCES["02_complete"])), "0\n1\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Repeticoes: Nivel inicial: Resultado: 14 / 20\n"
                                        "acesso negado\nCodigo: 0\nNivel: 1\n")

    def test_demo_output(self):
        result = compile_and_run(self, transpile(read(SOURCES["demo"])))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "3\n2\n1\nacesso liberado")

    def test_invalid_examples(self):
        self.assertEqual(sorted(path.stem for path in INVALID.glob("*.starwars")), sorted(INVALID_KINDS))
        for name, kind in INVALID_KINDS.items():
            with self.subTest(name=name):
                with self.assertRaises(CompilerError) as caught:
                    transpile(read(INVALID / f"{name}.starwars"))
                self.assertEqual(caught.exception.kind, kind)


if __name__ == "__main__":
    unittest.main()
