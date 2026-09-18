import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from support import EXAMPLES, ROOT, read

DEMO = EXAMPLES / "demo.starwars"
DEMO_C = EXAMPLES / "generated" / "demo.c"
ENV = {**os.environ, "PYTHONPATH": str(ROOT)}


def run_cli(*args, cwd=ROOT):
    return subprocess.run([sys.executable, "-B", "-m", "starwars", *map(str, args)],
                          capture_output=True, text=True, cwd=cwd, env=ENV)


class CliTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.folder = Path(tmp.name)
        self.output = self.folder / "out.c"

    def test_writes_c_and_prints_tokens_and_ast(self):
        result = run_cli(DEMO, "-o", self.output, "--tokens", "--ast")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("linha 1, coluna 1: [BEGIN:INICIA_SISTEMA]", result.stderr)
        self.assertIn('"node": "Program"', result.stderr)
        self.assertEqual(read(self.output), read(DEMO_C))

    def test_prints_c_without_output_option(self):
        result = run_cli(DEMO)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, read(DEMO_C))

    def test_error_keeps_existing_output(self):
        self.output.write_text("anterior", encoding="utf-8")
        result = run_cli(EXAMPLES / "invalid" / "05_semantic_error.starwars", "-o", self.output)
        self.assertEqual(result.returncode, 1)
        self.assertIn("ERRO SEMÂNTICO", result.stderr)
        self.assertEqual(read(self.output), "anterior")

    def test_error_does_not_create_output(self):
        result = run_cli(EXAMPLES / "invalid" / "03_lexical_error.starwars", "-o", self.output)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.output.exists())

    def test_requires_single_source_when_omitted(self):
        result = run_cli(cwd=self.folder)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Informe o arquivo .starwars", result.stderr)

    def test_uses_single_source_in_current_directory(self):
        (self.folder / "programa.starwars").write_text(read(DEMO), encoding="utf-8")
        result = run_cli(cwd=self.folder)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, read(DEMO_C))

    def test_output_must_differ_from_source(self):
        result = run_cli(DEMO, "-o", DEMO)
        self.assertEqual(result.returncode, 1)
        self.assertIn("deve ser diferente", result.stderr)

    def test_prints_tokens_before_syntax_error(self):
        result = run_cli(EXAMPLES / "invalid" / "04_syntax_error.starwars", "--tokens")
        self.assertEqual(result.returncode, 1)
        self.assertIn("[BEGIN:INICIA_SISTEMA]", result.stderr)
        self.assertIn("ERRO SINTÁTICO", result.stderr)


if __name__ == "__main__":
    unittest.main()
