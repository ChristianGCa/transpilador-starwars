"""Regressoes do compilador e execucao real do C; usa unittest e GCC."""
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import transpilador_hacker as sw


def programa(corpo):
    return f"INICIA_SISTEMA\n{corpo}\nLOGOUT"


class TranspiladorTests(unittest.TestCase):
    def executar_c(self, fonte, entrada=""):
        self.assertIsNotNone(shutil.which("gcc"), "GCC e obrigatorio para estes testes")
        codigo = sw.transpilar(fonte)
        with tempfile.TemporaryDirectory() as pasta:
            caminho = pathlib.Path(pasta)
            (caminho / "saida.c").write_text(codigo, encoding="utf-8")
            compilacao = subprocess.run(
                ["gcc", "-std=c99", "-Wall", "-Wextra", "-pedantic", "-Werror=format",
                 str(caminho / "saida.c"), "-o", str(caminho / "programa")],
                capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(compilacao.returncode, 0, compilacao.stderr)
            return subprocess.run([str(caminho / "programa")], input=entrada,
                                  capture_output=True, text=True, timeout=3)

    def saida(self, corpo, esperado, entrada=""):
        resultado = self.executar_c(programa(corpo), entrada)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertEqual(resultado.stdout, esperado)

    def test_exemplo_original(self):
        r = self.executar_c((ROOT / "teste.starwars").read_text(encoding="utf-8"))
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "3\n2\n1\nacesso liberado")

    def test_arquivos_validos_e_c_entregue(self):
        for nome in ("01_valido_basico", "02_valido_completo"):
            with self.subTest(nome=nome):
                fonte = (ROOT / "testes" / f"{nome}.starwars").read_text(encoding="utf-8")
                entrada = ROOT / "testes" / f"{nome}.entrada.txt"
                r = self.executar_c(fonte, entrada.read_text() if entrada.exists() else "")
                self.assertEqual(r.returncode, 0, r.stderr)
                esperado = (ROOT / "testes" / f"{nome}.esperado.txt").read_text()
                self.assertEqual(r.stdout, esperado)
                self.assertEqual((ROOT / "gerados" / f"{nome}.c").read_text(), sw.transpilar(fonte))

    def test_arquivos_invalidos(self):
        for arquivo in sorted((ROOT / "testes").glob("*erro*.starwars")):
            with self.subTest(arquivo=arquivo.name):
                categoria = "LEXICO" if arquivo.name.startswith("03") else (
                    "SINTATICO" if arquivo.name.startswith("04") else "SEMANTICO")
                with self.assertRaisesRegex(sw.CompilerError, f"ERRO {categoria} \\(linha [0-9]+\\)"):
                    sw.transpilar(arquivo.read_text(encoding="utf-8"))

    def test_programa_completo_ramo_alternativo(self):
        fonte = (ROOT / 'testes/02_valido_completo.starwars').read_text(encoding='utf-8')
        r = self.executar_c(fonte, '0\n1\n')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, 'Repeticoes: Nivel inicial: Resultado: 14 / 20\n'
                         'acesso negado\nCodigo: 0\nNivel: 1\n')

    def test_blocos_aninhados_e_atribuicao_externa(self):
        self.saida('x: Você era o escolhido = 2; total: Você era o escolhido;\n'
                   'Eu sinto uma perturbação na força (x > 0)\n'
                   'local: Você era o escolhido = x;\n'
                   'Faça, ou não faça (local == 2) total = total + 10;\n'
                   'Tentativa não há total = total + 1; LOGOUT\n'
                   'x = x - 1; LOGOUT Hello There (total);', '11\n')

    def test_precedencia_na_ast(self):
        _, ast = sw.analisar(programa("Hello There (2 + 3 * 4);"))
        expr = ast.comandos[0].itens[0]
        self.assertEqual(expr.op, "+")
        self.assertEqual(expr.dire.op, "*")
        _, ast = sw.analisar(programa("Hello There ((2 + 3) * 4);"))
        self.assertEqual(ast.comandos[0].itens[0].esq.op, "+")

    def test_aritmetica_e_associatividade(self):
        self.saida('Hello There (2 + 3 * 4, ",", (2 + 3) * 4, ",", 8 / 3, ",", 8 / 2.0);\n'
                   'Hello There (10 - 3 - 2, ",", 20 / 2 / 2);', "14,20,2,4\n5,5\n")

    def test_operadores_tematicos(self):
        self.saida('Hello There ((10 Acabou anakin 2) Eu sou todos os sith 2 '
                   'Que a força esteja com você 3 Eu sou todos os jedi 2);', "10\n")

    def test_operadores_relacionais(self):
        for tematico, simbolico in sw.OP_MAP.items():
            for op in {tematico, simbolico}:
                with self.subTest(op=op):
                    esperado = "sim" if simbolico in ("!=", ">", ">=") else "nao"
                    self.saida(f'Faça, ou não faça (2 {op} 1) Hello There ("sim"); '
                               'Tentativa não há Hello There ("nao"); LOGOUT', esperado)

    def test_entrada_inteira_real_e_prompt(self):
        self.saida('i: Você era o escolhido; r: Eu sou C3PO, ciborgue de relações humanas;\n'
                   'Ajude-me Obi-Wan Kenobi (i); Ajude-me Obi-Wan Kenobi ("Real: " -> r);\n'
                   'Hello There (i, ",", r);', "Real: -2,1.5\n", "-2\n1.5\n")

    def test_entrada_invalida_e_eof(self):
        for entrada in ("abc", ""):
            with self.subTest(entrada=entrada):
                r = self.executar_c(programa('x: Você era o escolhido; Ajude-me Obi-Wan Kenobi (x);'), entrada)
                self.assertEqual(r.returncode, 1)
                self.assertIn("ERRO DE ENTRADA", r.stderr)

    def test_leitura_sem_declaracao(self):
        with self.assertRaisesRegex(sw.CompilerError, "SEMANTICO.*nao declarada"):
            sw.transpilar(programa("Ajude-me Obi-Wan Kenobi (x);"))

    def test_tipo_na_declaracao_e_atribuicao(self):
        for corpo in ('x: Você era o escolhido = 1.5;',
                      'Você era o escolhido x Eu alterei o acordo 1.5;',
                      'x: Você era o escolhido; x = 1 + 1.5;'):
            with self.subTest(corpo=corpo), self.assertRaisesRegex(sw.CompilerError, "incompatibilidade"):
                sw.transpilar(programa(corpo))
        self.saida('x: Eu sou C3PO, ciborgue de relações humanas = 2; x = x + 0.5; Hello There (x);', "2.5\n")

    def test_inicializadores_e_expressoes_sem_declaracao(self):
        for corpo in ('x: Você era o escolhido = x;',
                      'x: Eu sou C3PO, ciborgue de relações humanas = y;',
                      'Hello There (x);', 'Faça, ou não faça (x == 1) LOGOUT',
                      'Eu sinto uma perturbação na força (x > 0) LOGOUT'):
            with self.subTest(corpo=corpo), self.assertRaisesRegex(sw.CompilerError, "nao declarada"):
                sw.transpilar(programa(corpo))

    def test_escopos_sombreamento_e_inicializador_externo(self):
        self.saida('x: Você era o escolhido = 7;\n'
                   'Faça, ou não faça (1 == 1)\n'
                   'x: Você era o escolhido = x + 1; Hello There (x);\n'
                   'Tentativa não há x: Você era o escolhido = 2; Hello There (x); LOGOUT\n'
                   'Hello There (x);', "8\n7\n")

    def test_escopo_nao_vaza_de_if_else_ou_while(self):
        for bloco in ('Faça, ou não faça (1 == 1) x: Você era o escolhido; LOGOUT',
                      'Faça, ou não faça (1 == 0) Tentativa não há x: Você era o escolhido; LOGOUT',
                      'Eu sinto uma perturbação na força (1 == 0) x: Você era o escolhido; LOGOUT'):
            with self.subTest(bloco=bloco), self.assertRaisesRegex(sw.CompilerError, "nao declarada"):
                sw.transpilar(programa(bloco + ' Hello There (x);'))
        with self.assertRaisesRegex(sw.CompilerError, "nao declarada"):
            sw.transpilar(programa('Faça, ou não faça (1 == 1) x: Você era o escolhido; '
                                  'Tentativa não há Hello There (x); LOGOUT'))

    def test_inicializacao_padrao(self):
        self.saida('x: Você era o escolhido; r: Eu sou C3PO, ciborgue de relações humanas; Hello There (x, ",", r);', "0,0\n")

    def test_texto_percentual_escapes_e_trigraph(self):
        self.saida(r'Hello There ("100% de energia %n ??/ \\", "\"jedi\"\n\t");',
                   '100% de energia %n ??/ \\"jedi"\n\t')

    def test_nomes_seguros_e_zeros_iniciais(self):
        self.saida('return: Você era o escolhido = 08; printf: Você era o escolhido = 010; '
                   'LOGOUTx: Você era o escolhido = 2; ação: Você era o escolhido = 3; '
                   'Hello There (return + printf + LOGOUTx + ação);', "23\n")

    def test_limites_dos_literais(self):
        for literal in ('2147483648', '9' * 5000, '9' * 40 + '.0'):
            with self.subTest(tamanho=len(literal)), self.assertRaisesRegex(sw.CompilerError, "fora do intervalo"):
                sw.transpilar(programa(f'Hello There ({literal});'))
        self.saida('Hello There (2147483647);', "2147483647\n")

    def test_longest_match_e_fronteira_de_palavra(self):
        tokens = sw.tokenize('LOGOUTx >= > <= < == = != -> -')
        self.assertEqual([t.kind for t in tokens],
                         ['ID', 'GE', 'GT', 'LE', 'LT', 'EQ', 'ASSIGN', 'NEQ', 'ARROW', 'MINUS', 'EOF'])

    def test_comentarios_e_quebras_de_linha(self):
        self.assertEqual(sw.transpilar('INICIA_SISTEMA\r\n# comentario\rLOGOUT'),
                         sw.transpilar('INICIA_SISTEMA\nLOGOUT'))
        with self.assertRaisesRegex(sw.CompilerError, 'LEXICO \\(linha 3\\)'):
            sw.tokenize('INICIA_SISTEMA\r\n# comentario\r@')

    def test_strings_invalidas(self):
        for texto in ('"sem fim', '"linha\nquebrada"', r'"escape\q"'):
            with self.subTest(texto=texto), self.assertRaisesRegex(sw.CompilerError, "LEXICO"):
                sw.transpilar(programa(f'Hello There ({texto});'))

    def test_sintaxe_invalida(self):
        for corpo in ('Hello There ();', 'Hello There (1,);', 'x: = 1;',
                      'Ajude-me Obi-Wan Kenobi ("x" x);', 'Faça, ou não faça (1) LOGOUT',
                      'Faça, ou não faça (1 == 1)', 'Eu sinto uma perturbação na força (1 > 0)'):
            with self.subTest(corpo=corpo), self.assertRaisesRegex(sw.CompilerError, "SINTATICO"):
                sw.transpilar(programa(corpo))

    def test_cli_saida_ast_tokens_e_erros(self):
        with tempfile.TemporaryDirectory() as pasta:
            saida = pathlib.Path(pasta) / 'saida.c'
            cmd = [sys.executable, '-B', str(ROOT / 'transpilador_hacker.py')]
            r = subprocess.run(cmd + [str(ROOT / 'teste.starwars'), '-o', str(saida), '--ast', '--tokens'],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn('Programa', r.stderr)
            self.assertIn('[INICIA:', r.stderr)
            anterior = saida.read_text()
            r = subprocess.run(cmd + [str(ROOT / 'testes/05_erro_semantico.starwars'), '-o', str(saida)],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertIn('ERRO SEMANTICO', r.stderr)
            self.assertEqual(saida.read_text(), anterior)
            saida.unlink()
            r = subprocess.run(cmd + [str(ROOT / 'testes/03_erro_lexico.starwars'), '-o', str(saida)],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertFalse(saida.exists())
            r = subprocess.run(cmd, cwd=pasta, capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)


if __name__ == '__main__':
    unittest.main()
