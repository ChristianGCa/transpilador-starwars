import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
GCC_FLAGS = ["-std=c99", "-Wall", "-Wextra", "-pedantic", "-Werror=format"]


def program(body: str) -> str:
    return f"INICIA_SISTEMA\n{body}\nLOGOUT"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def compile_and_run(test: unittest.TestCase, c_code: str, stdin: str = "") -> subprocess.CompletedProcess:
    test.assertIsNotNone(shutil.which("gcc"), "GCC é obrigatório para estes testes")
    with tempfile.TemporaryDirectory() as tmp:
        source, binary = Path(tmp) / "program.c", Path(tmp) / "program"
        source.write_text(c_code, encoding="utf-8")
        build = subprocess.run(["gcc", *GCC_FLAGS, str(source), "-o", str(binary)],
                               capture_output=True, text=True, timeout=10)
        test.assertEqual(build.returncode, 0, build.stderr)
        return subprocess.run([str(binary)], input=stdin, capture_output=True, text=True, timeout=3)
