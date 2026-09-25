import json
import re
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

from support import ROOT
from starwars.tokens import KEYWORD_PHRASES

EXTENSION = ROOT / "editors" / "vscode"
GRAMMAR = EXTENSION / "syntaxes" / "starwars.tmLanguage.json"
JS_TESTS = ROOT / "tests" / "vscode" / "language.test.js"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def grammar_regexes(node) -> list:
    if isinstance(node, dict):
        found = [node["match"]] if "match" in node else []
        return found + [regex for value in node.values() for regex in grammar_regexes(value)]
    if isinstance(node, list):
        return [regex for item in node for regex in grammar_regexes(item)]
    return []


class VscodeExtensionTest(unittest.TestCase):
    def test_grammar_highlights_every_keyword_phrase(self):
        patterns = [re.compile(regex) for regex in grammar_regexes(read_json(GRAMMAR))]
        for _, phrase in KEYWORD_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertTrue(any(pattern.fullmatch(phrase) for pattern in patterns))

    def test_hover_texts_cover_every_keyword_phrase(self):
        documented = set()
        for entry in read_json(EXTENSION / "phrases.json"):
            documented.update([entry["phrase"], *entry.get("aliases", [])])
        for _, phrase in KEYWORD_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, documented)

    @unittest.skipUnless(shutil.which("node"), "Node.js é necessário para testar o hover e o autocompletar")
    def test_hover_and_completion_logic(self):
        result = subprocess.run(["node", "--test", str(JS_TESTS)], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_extension_registers_language_and_grammar(self):
        package = read_json(EXTENSION / "package.json")
        language = package["contributes"]["languages"][0]
        grammar = package["contributes"]["grammars"][0]
        self.assertEqual(language["extensions"], [".starwars"])
        self.assertEqual(grammar["scopeName"], read_json(GRAMMAR)["scopeName"])
        self.assertTrue((EXTENSION / grammar["path"]).exists())
        self.assertTrue((EXTENSION / language["configuration"]).exists())
        self.assertTrue((EXTENSION / package["main"]).exists())

    def test_color_rules_only_touch_starwars_scopes(self):
        colors = read_json(EXTENSION / "package.json")["contributes"]["configurationDefaults"]
        customizations = colors["editor.tokenColorCustomizations"]
        rules = customizations["textMateRules"] + customizations["[*Light*]"]["textMateRules"]
        for rule in rules:
            scopes = rule["scope"] if isinstance(rule["scope"], list) else [rule["scope"]]
            for scope in scopes:
                with self.subTest(scope=scope):
                    self.assertTrue(scope.endswith(".starwars"))

    def test_sw_builds_installable_vsix(self):
        with tempfile.TemporaryDirectory() as tmp:
            vsix = Path(tmp) / "starwars.vsix"
            result = subprocess.run([str(ROOT / "sw"), "vscode", str(vsix)],
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            with zipfile.ZipFile(vsix) as archive:
                names = set(archive.namelist())
                package = json.loads(archive.read("extension/package.json"))
        self.assertLessEqual({"extension.vsixmanifest", "[Content_Types].xml",
                              "extension/syntaxes/starwars.tmLanguage.json",
                              "extension/language-configuration.json", "extension/extension.js",
                              "extension/language.js", "extension/phrases.json"}, names)
        self.assertEqual(package["name"], "starwars-language")


if __name__ == "__main__":
    unittest.main()
