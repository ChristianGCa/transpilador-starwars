import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from support import EXAMPLES, ROOT, read

SCRIPT = ROOT / "sw"
BASIC = EXAMPLES / "valid" / "01_basic.starwars"
COMPLETE = EXAMPLES / "valid" / "02_complete.starwars"
SEMANTIC_ERROR = EXAMPLES / "invalid" / "05_semantic_error.starwars"


class ScriptTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.folder = Path(tmp.name)
        self.build = self.folder / "build"
        self.env = {**os.environ, "SW_BUILD_DIR": str(self.build)}

    def run_script(self, *args, stdin="", cwd=ROOT, env=None):
        return subprocess.run([str(SCRIPT), *map(str, args)], input=stdin, capture_output=True,
                              text=True, cwd=cwd, env=env or self.env, timeout=30)

    def test_help_lists_commands(self):
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        for command in ("run", "build", "c", "check", "test", "regen", "demo", "clean"):
            self.assertIn(f"./sw {command}", result.stdout)

    def test_unknown_command(self):
        result = self.run_script("voar")
        self.assertEqual(result.returncode, 2)
        self.assertIn("comando desconhecido: voar", result.stderr)

    def test_run_executes_program(self):
        result = self.run_script("run", BASIC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Energia: 14\n")
        self.assertEqual(result.stderr, "")

    def test_run_forwards_stdin_from_any_directory(self):
        relative = os.path.relpath(COMPLETE, self.folder)
        result = self.run_script("run", relative, cwd=self.folder,
                                 stdin=read(EXAMPLES / "valid" / "02_complete.input.txt"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, read(EXAMPLES / "valid" / "02_complete.expected.txt"))

    def test_run_stops_on_compiler_error(self):
        result = self.run_script("run", SEMANTIC_ERROR)
        self.assertEqual(result.returncode, 1)
        self.assertIn("ERRO SEMÂNTICO", result.stderr)
        self.assertFalse((self.build / "05_semantic_error").exists())

    def test_build_creates_c_and_binary_without_running(self):
        result = self.run_script("build", BASIC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(read(self.build / "01_basic.c"), read(EXAMPLES / "generated" / "01_basic.c"))
        self.assertTrue(os.access(self.build / "01_basic", os.X_OK))
        self.assertNotIn("Energia", result.stdout)

    def test_c_prints_generated_code(self):
        result = self.run_script("c", BASIC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, read(EXAMPLES / "generated" / "01_basic.c"))

    def test_c_forwards_inspection_options(self):
        result = self.run_script("c", BASIC, "--ast")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"node": "Program"', result.stderr)

    def test_check_accepts_valid_program(self):
        result = self.run_script("check", BASIC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("nenhum erro", result.stdout)

    def test_check_reports_error(self):
        result = self.run_script("check", SEMANTIC_ERROR)
        self.assertEqual(result.returncode, 1)
        self.assertIn("ERRO SEMÂNTICO", result.stderr)

    def test_requires_source_argument(self):
        result = self.run_script("run")
        self.assertEqual(result.returncode, 2)
        self.assertIn("informe o arquivo .starwars", result.stderr)

    def test_missing_source_file(self):
        result = self.run_script("run", "inexistente.starwars")
        self.assertEqual(result.returncode, 1)
        self.assertIn("arquivo não encontrado: inexistente.starwars", result.stderr)

    def test_missing_c_compiler(self):
        result = self.run_script("run", BASIC, env={**self.env, "CC": "compilador-inexistente"})
        self.assertEqual(result.returncode, 1)
        self.assertIn("compilador C 'compilador-inexistente' não encontrado", result.stderr)

    def test_regen_writes_generated_examples(self):
        result = self.run_script("regen", self.folder)
        self.assertEqual(result.returncode, 0, result.stderr)
        for path in (EXAMPLES / "generated").glob("*.c"):
            with self.subTest(name=path.name):
                self.assertEqual(read(self.folder / path.name), read(path))

    def test_demo_shows_programs_and_errors(self):
        result = self.run_script("demo")
        self.assertEqual(result.returncode, 0, result.stderr)
        output = result.stdout + result.stderr
        for expected in ("Energia: 14", "Resultado: 14 / 20", "ERRO LÉXICO", "ERRO SINTÁTICO",
                         "ERRO SEMÂNTICO"):
            self.assertIn(expected, output)

    def test_clean_removes_build_directory(self):
        self.run_script("build", BASIC)
        result = self.run_script("clean")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.build.exists())


if __name__ == "__main__":
    unittest.main()
