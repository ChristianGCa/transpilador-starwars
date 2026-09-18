"""Transpilador Star Wars: lexer -> parser -> AST -> semantica -> C.

A especificacao completa, incluindo a EBNF, esta em RELATORIO.md.
Somente a biblioteca padrao do Python e necessaria para transpilar.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

# =================================================================
# 1. LEXER
# =================================================================

# Palavras-chave multi-palavra (ordem importa: mais longas primeiro)
KEYWORDS_MULTIWORD = [
    ("INICIA",        "INICIA_SISTEMA"),
    ("LOGOUT",        "LOGOUT"),
    ("NUM_TYPE",      "Você era o escolhido"),
    ("REAL_TYPE",     "Eu sou C3PO, ciborgue de relações humanas"),
    ("ASSIGN",        "Eu alterei o acordo"),
    ("PLUS",          "Que a força esteja com você"),
    ("MINUS",         "Acabou anakin"),
    ("STAR",          "Eu sou todos os jedi"),
    ("SLASH",         "Eu sou todos os sith"),
    ("EQ",            "Como deve ser"),
    ("GT",            "I have the high ground"),
    ("GE",            "A força é forte nele"),
    ("LT",            "Você subestima meu poder"),
    ("LE",            "Não, eu sou seu pai"),
    ("IF",            "Faça, ou não faça"),
    ("ELSE",          "Tentativa não há"),
    ("PRINT",         "Hello There"),
    ("INPUT",         "Ajude-me Obi-Wan Kenobi"),
    ("WHILE",         "Eu sinto uma perturbação na força"),
]

# Letras portuguesas e ASCII; os nomes sao renomeados antes de gerar C.
ID_START = r"[A-Za-z_À-ÖØ-öø-ÿ]"
ID_CONT = r"[A-Za-z0-9_À-ÖØ-öø-ÿ]"

# Tokens simples (regex)
TOKEN_SPEC_SIMPLE = [
    ("SKIP",          r"[ \t]+"),
    ("NEWLINE",       r"\r\n|\r|\n"),
    ("COMMENT",       r"#[^\r\n]*"),
    ("NUM",           r"[0-9]+(\.[0-9]+)?"),
    ("STRING",        r'"(?:[^"\\\x00-\x1f\x7f]|\\["\\nrt])*"'),
    ("ARROW",         r"->"),
    ("EQ",            r"=="),
    ("NEQ",           r"!="),
    ("GE",            r">="),
    ("LE",            r"<="),
    ("GT",            r">"),
    ("LT",            r"<"),
    ("ASSIGN",        r"="),
    ("PLUS",          r"\+"),
    ("MINUS",         r"-"),
    ("STAR",          r"\*"),
    ("SLASH",         r"/"),
    ("LPAREN",        r"\("),
    ("RPAREN",        r"\)"),
    ("SEMI",          r";"),
    ("COLON",         r":"),
    ("COMMA",         r","),
    ("ID",            ID_START + ID_CONT + "*"),
]


class Token:
    def __init__(self, kind, value, line):
        self.kind, self.value, self.line = kind, value, line

    def __repr__(self):
        return f"[{self.kind}:{self.value}]"


class CompilerError(Exception):
    pass


def tokenize(source: str):
    tokens = []
    line = 1
    pos = 0

    simple_re = re.compile("|".join(f"(?P<{n}>{p})" for n, p in TOKEN_SPEC_SIMPLE))

    # Ordena palavras-chave da mais longa para a mais curta
    kw_sorted = sorted(KEYWORDS_MULTIWORD, key=lambda x: -len(x[1]))

    while pos < len(source):
        # Tenta casar palavras-chave multi-palavra primeiro
        matched_kw = False
        for kind, kw in kw_sorted:
            end = pos + len(kw)
            boundary = end == len(source) or not re.match(ID_CONT, source[end:end + 1])
            if source.startswith(kw, pos) and boundary:
                tokens.append(Token(kind, kw, line))
                pos += len(kw)
                matched_kw = True
                break

        if matched_kw:
            continue

        # Tenta casar tokens simples
        m = simple_re.match(source, pos)
        if not m:
            raise CompilerError(
                f"ERRO LEXICO (linha {line}): caractere invalido '{source[pos]}'"
            )
        kind, value = m.lastgroup, m.group()
        if kind == "NEWLINE":
            line += 1
        elif kind not in ("SKIP", "COMMENT"):
            tokens.append(Token(kind, value, line))
        pos = m.end()

    tokens.append(Token("EOF", None, line))
    return tokens


# =================================================================
# 2. AST (nos da arvore)
# =================================================================

class Node:
    pass

class Programa(Node):
    def __init__(self, comandos): self.comandos = comandos

class Declaracao(Node):
    def __init__(self, tipo, nome, expr, line):
        self.tipo, self.nome, self.expr, self.line = tipo, nome, expr, line

class Atribuicao(Node):
    def __init__(self, nome, expr, line):
        self.nome, self.expr, self.line = nome, expr, line

class Escrita(Node):
    def __init__(self, itens, line): self.itens, self.line = itens, line

class Leitura(Node):
    def __init__(self, nome, prompt, line):
        self.nome, self.prompt, self.line = nome, prompt, line

class Condicional(Node):
    def __init__(self, cond, bloco_if, bloco_else, line):
        self.cond, self.bloco_if, self.bloco_else, self.line = cond, bloco_if, bloco_else, line

class Repeticao(Node):
    def __init__(self, cond, bloco, line):
        self.cond, self.bloco, self.line = cond, bloco, line

class ExprLogica(Node):
    def __init__(self, esq, op, dire, line):
        self.esq, self.op, self.dire, self.line = esq, op, dire, line

class BinOp(Node):
    def __init__(self, esq, op, dire, line):
        self.esq, self.op, self.dire, self.line = esq, op, dire, line

class Num(Node):
    def __init__(self, valor, line): self.valor, self.line = valor, line

class StringLit(Node):
    def __init__(self, valor, line): self.valor, self.line = valor, line

class Var(Node):
    def __init__(self, nome, line): self.nome, self.line = nome, line


# =================================================================
# 3. PARSER (descida recursiva) -> constroi a AST
# =================================================================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def atual(self):
        return self.tokens[self.pos]

    def esperar(self, kind):
        tok = self.atual()
        if tok.kind != kind:
            raise CompilerError(
                f"ERRO SINTATICO (linha {tok.line}): esperado {kind}, encontrado {tok.kind} ('{tok.value}')"
            )
        self.pos += 1
        return tok

    def checar(self, *kinds):
        return self.atual().kind in kinds

    # <Programa> ::= "INICIA_SISTEMA" <Bloco> "LOGOUT"
    def parse_programa(self):
        self.esperar("INICIA")
        comandos = self.parse_bloco(fim_kinds=("LOGOUT",))
        self.esperar("LOGOUT")
        self.esperar("EOF")
        return Programa(comandos)

    # <Bloco> ::= { <Declaracao> | <Comando> }
    def parse_bloco(self, fim_kinds):
        comandos = []
        while not self.checar(*fim_kinds) and not self.checar("EOF"):
            if self.checar("NUM_TYPE", "REAL_TYPE") or (
                self.checar("ID") and self.tokens[self.pos + 1].kind == "COLON"
            ):
                comandos.append(self.parse_declaracao())
            else:
                comandos.append(self.parse_comando())
        return comandos

    def parse_declaracao(self):
        if self.checar("ID"):
            nome_tok = self.esperar("ID")
            self.esperar("COLON")
            tipo_tok = self.atual()
            if not self.checar("NUM_TYPE", "REAL_TYPE"):
                raise CompilerError(
                    f"ERRO SINTATICO (linha {tipo_tok.line}): esperado tipo inteiro ou real, "
                    f"encontrado '{tipo_tok.value}'"
                )
            self.pos += 1
        else:
            tipo_tok = self.atual()
            self.pos += 1
            nome_tok = self.esperar("ID")
        tipo = "int" if tipo_tok.kind == "NUM_TYPE" else "float"
        expr = None
        if self.checar("ASSIGN"):
            self.pos += 1
            expr = self.parse_expressao()
        self.esperar("SEMI")
        return Declaracao(tipo, nome_tok.value, expr, tipo_tok.line)

    def parse_comando(self):
        if self.checar("ID"):
            return self.parse_atribuicao()
        if self.checar("PRINT"):
            return self.parse_escrita()
        if self.checar("INPUT"):
            return self.parse_leitura()
        if self.checar("IF"):
            return self.parse_condicional()
        if self.checar("WHILE"):
            return self.parse_repeticao()
        tok = self.atual()
        raise CompilerError(
            f"ERRO SINTATICO (linha {tok.line}): comando invalido comecando com '{tok.value}'"
        )

    def parse_atribuicao(self):
        nome_tok = self.esperar("ID")
        self.esperar("ASSIGN")
        expr = self.parse_expressao()
        self.esperar("SEMI")
        return Atribuicao(nome_tok.value, expr, nome_tok.line)

    def parse_escrita(self):
        tok = self.esperar("PRINT")
        self.esperar("LPAREN")
        itens = []
        while True:
            if self.checar("STRING"):
                itens.append(StringLit(self.atual().value, self.atual().line))
                self.pos += 1
            else:
                itens.append(self.parse_expressao())
            if not self.checar("COMMA"):
                break
            self.pos += 1
        self.esperar("RPAREN")
        self.esperar("SEMI")
        return Escrita(itens, tok.line)

    def parse_leitura(self):
        tok = self.esperar("INPUT")
        self.esperar("LPAREN")
        prompt = None
        if self.checar("STRING"):
            prompt = self.esperar("STRING").value
            self.esperar("ARROW")
        nome = self.esperar("ID").value
        self.esperar("RPAREN")
        self.esperar("SEMI")
        return Leitura(nome, prompt, tok.line)

    def parse_condicional(self):
        tok = self.esperar("IF")
        self.esperar("LPAREN")
        cond = self.parse_expr_logica()
        self.esperar("RPAREN")
        bloco_if = self.parse_bloco(fim_kinds=("ELSE", "LOGOUT"))
        bloco_else = None
        if self.checar("ELSE"):
            self.pos += 1
            bloco_else = self.parse_bloco(fim_kinds=("LOGOUT",))
        self.esperar("LOGOUT")
        return Condicional(cond, bloco_if, bloco_else, tok.line)

    def parse_repeticao(self):
        tok = self.esperar("WHILE")
        self.esperar("LPAREN")
        cond = self.parse_expr_logica()
        self.esperar("RPAREN")
        bloco = self.parse_bloco(fim_kinds=("LOGOUT",))
        self.esperar("LOGOUT")
        return Repeticao(cond, bloco, tok.line)

    def parse_expr_logica(self):
        esq = self.parse_expressao()
        if not self.checar("EQ", "NEQ", "GT", "GE", "LT", "LE"):
            tok = self.atual()
            raise CompilerError(
                f"ERRO SINTATICO (linha {tok.line}): esperado operador relacional, encontrado '{tok.value}'"
            )
        op_tok = self.atual()
        self.pos += 1
        dire = self.parse_expressao()
        return ExprLogica(esq, op_tok.value, dire, op_tok.line)

    # <Expressao> ::= <Termo> { (PLUS|MINUS) <Termo> }
    def parse_expressao(self):
        no = self.parse_termo()
        while self.checar("PLUS", "MINUS"):
            op_tok = self.atual()
            self.pos += 1
            dire = self.parse_termo()
            no = BinOp(no, op_tok.value, dire, op_tok.line)
        return no

    # <Termo> ::= <Fator> { (STAR|SLASH) <Fator> }
    def parse_termo(self):
        no = self.parse_fator()
        while self.checar("STAR", "SLASH"):
            op_tok = self.atual()
            self.pos += 1
            dire = self.parse_fator()
            no = BinOp(no, op_tok.value, dire, op_tok.line)
        return no

    # <Fator> ::= id | num | "(" <Expressao> ")"
    def parse_fator(self):
        tok = self.atual()
        if tok.kind == "ID":
            self.pos += 1
            return Var(tok.value, tok.line)
        if tok.kind == "NUM":
            self.pos += 1
            return Num(tok.value, tok.line)
        if tok.kind == "LPAREN":
            self.pos += 1
            no = self.parse_expressao()
            self.esperar("RPAREN")
            return no
        raise CompilerError(
            f"ERRO SINTATICO (linha {tok.line}): esperado identificador, numero ou '(', encontrado '{tok.value}'"
        )


# =================================================================
# 4. ANALISE SEMANTICA (tabela de simbolos + verificacoes)
# =================================================================

class AnalisadorSemantico:
    def __init__(self):
        self.escopos = [{}]  # Cada tabela associa nome a tipo e nome no C.
        self.proximo_id = 0

    def resolver(self, nome, line):
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]
        raise CompilerError(
            f"ERRO SEMANTICO (linha {line}): variavel '{nome}' nao declarada neste escopo"
        )

    def tipo_de_expr(self, no):
        if isinstance(no, Num):
            tipo = "float" if "." in no.valor else "int"
            # Limites do alvo adotado: int de 32 bits e float IEEE-754 binario32.
            if tipo == "int":
                digitos = no.valor.lstrip("0") or "0"
                invalido = len(digitos) > 10 or int(digitos) > 2147483647
            else:
                valor = float(no.valor)
                invalido = not math.isfinite(valor) or valor > 3.4028234663852886e38
            if invalido:
                raise CompilerError(
                    f"ERRO SEMANTICO (linha {no.line}): literal fora do intervalo de {tipo}"
                )
        elif isinstance(no, Var):
            simbolo = self.resolver(no.nome, no.line)
            tipo, no.nome_c = simbolo["tipo"], simbolo["nome_c"]
        elif isinstance(no, BinOp):
            t1 = self.tipo_de_expr(no.esq)
            t2 = self.tipo_de_expr(no.dire)
            tipo = "float" if "float" in (t1, t2) else "int"
        else:
            raise CompilerError("ERRO SEMANTICO: expressao numerica desconhecida")
        no.tipo = tipo
        return tipo

    def verificar_tipo(self, tipo, expr, nome, line):
        tipo_expr = self.tipo_de_expr(expr)
        if tipo == "int" and tipo_expr == "float":
            raise CompilerError(
                f"ERRO SEMANTICO (linha {line}): incompatibilidade de tipos: "
                f"nao e possivel atribuir float a variavel int '{nome}'"
            )

    def visitar_bloco(self, comandos, novo_escopo=False):
        if novo_escopo:
            self.escopos.append({})
        try:
            for c in comandos:
                self.visitar(c)
        finally:
            if novo_escopo:
                self.escopos.pop()

    def visitar(self, no):
        if isinstance(no, Declaracao):
            if no.nome in self.escopos[-1]:
                raise CompilerError(
                    f"ERRO SEMANTICO (linha {no.line}): variavel '{no.nome}' ja declarada neste escopo"
                )
            # O nome novo fica visivel somente depois de avaliar seu inicializador.
            if no.expr is not None:
                self.verificar_tipo(no.tipo, no.expr, no.nome, no.line)
            no.nome_c = f"sw_v{self.proximo_id}"
            self.proximo_id += 1
            self.escopos[-1][no.nome] = {"tipo": no.tipo, "nome_c": no.nome_c}
        elif isinstance(no, (Atribuicao, Leitura)):
            simbolo = self.resolver(no.nome, no.line)
            no.nome_c, no.tipo = simbolo["nome_c"], simbolo["tipo"]
            if isinstance(no, Atribuicao):
                self.verificar_tipo(no.tipo, no.expr, no.nome, no.line)
        elif isinstance(no, Escrita):
            for item in no.itens:
                if not isinstance(item, StringLit):
                    self.tipo_de_expr(item)
        elif isinstance(no, (Condicional, Repeticao)):
            self.tipo_de_expr(no.cond.esq)
            self.tipo_de_expr(no.cond.dire)
            if isinstance(no, Condicional):
                self.visitar_bloco(no.bloco_if, novo_escopo=True)
                if no.bloco_else is not None:
                    self.visitar_bloco(no.bloco_else, novo_escopo=True)
            else:
                self.visitar_bloco(no.bloco, novo_escopo=True)
        else:
            raise CompilerError("ERRO SEMANTICO: comando desconhecido")


# =================================================================
# 5. GERADOR DE CODIGO C
# =================================================================

# Mapeamento dos tokens de operador relacional para C
OP_MAP = {
    "Como deve ser":            "==",
    "!=":                       "!=",
    "I have the high ground":   ">",
    "A força é forte nele":     ">=",
    "Você subestima meu poder": "<",
    "Não, eu sou seu pai":      "<=",
}

# Mapeamento dos tokens de operador aritmético para C
ARITH_MAP = {
    "Que a força esteja com você": "+",
    "Acabou anakin":               "-",
    "Eu sou todos os jedi":        "*",
    "Eu sou todos os sith":        "/",
}

def literal_c(valor):
    # Evita que trigraphs do C99 mudem textos como "??/" antes do parsing do C.
    return valor.replace("?", r"\?")


def gerar_expr(no):
    if isinstance(no, Num):
        if "." in no.valor:
            inteiro, fracao = no.valor.split(".")
            return f"{inteiro.lstrip('0') or '0'}.{fracao}f"
        return no.valor.lstrip("0") or "0"
    if isinstance(no, Var):
        return no.nome_c
    if isinstance(no, BinOp):
        op_c = ARITH_MAP.get(no.op, no.op)
        return f"({gerar_expr(no.esq)} {op_c} {gerar_expr(no.dire)})"
    raise CompilerError("no de expressao desconhecido no gerador")


def gerar_bloco(comandos, indent=1):
    linhas = []
    pad = "    " * indent
    for c in comandos:
        if isinstance(c, Declaracao):
            # Inicializacao padrao definida pela linguagem, evitando lixo de memoria.
            init = gerar_expr(c.expr) if c.expr is not None else "0"
            linhas.append(f"{pad}{c.tipo} {c.nome_c} = {init};")
        elif isinstance(c, Atribuicao):
            linhas.append(f"{pad}{c.nome_c} = {gerar_expr(c.expr)};")
        elif isinstance(c, Leitura):
            if c.prompt is not None:
                linhas.append(f'{pad}printf("%s", {literal_c(c.prompt)});')
                linhas.append(f"{pad}fflush(stdout);")
            formato = "%d" if c.tipo == "int" else "%f"
            linhas.append(f'{pad}if (scanf("{formato}", &{c.nome_c}) != 1) {{')
            linhas.append(
                f'{pad}    fprintf(stderr, "ERRO DE ENTRADA (linha {c.line}): '
                'esperado valor numerico.\\n");'
            )
            linhas.append(f"{pad}    return 1;")
            linhas.append(f"{pad}}}")
        elif isinstance(c, Escrita):
            for item in c.itens:
                if isinstance(item, StringLit):
                    linhas.append(f'{pad}printf("%s", {literal_c(item.valor)});')
                elif item.tipo == "int":
                    linhas.append(f'{pad}printf("%d", {gerar_expr(item)});')
                else:
                    linhas.append(f'{pad}printf("%g", (double)({gerar_expr(item)}));')
            # Preserva a saida antiga: texto puro nao recebe quebra automatica;
            # comandos com valores numericos terminam a linha uma unica vez.
            if any(not isinstance(item, StringLit) for item in c.itens):
                linhas.append(f'{pad}printf("\\n");')
        elif isinstance(c, (Condicional, Repeticao)):
            op_c = OP_MAP.get(c.cond.op, c.cond.op)
            cond = f"{gerar_expr(c.cond.esq)} {op_c} {gerar_expr(c.cond.dire)}"
            if isinstance(c, Condicional):
                linhas.append(f"{pad}if ({cond}) {{")
                linhas.extend(gerar_bloco(c.bloco_if, indent + 1))
                if c.bloco_else is not None:
                    linhas.append(f"{pad}}} else {{")
                    linhas.extend(gerar_bloco(c.bloco_else, indent + 1))
            else:
                linhas.append(f"{pad}while ({cond}) {{")
                linhas.extend(gerar_bloco(c.bloco, indent + 1))
            linhas.append(f"{pad}}}")
        else:
            raise CompilerError("no de comando desconhecido no gerador")
    return linhas


def gerar_codigo_c(programa: Programa) -> str:
    corpo = "\n".join(gerar_bloco(programa.comandos))
    return f"#include <stdio.h>\n\nint main(void) {{\n{corpo}\n    return 0;\n}}\n"


# =================================================================
# 6. PIPELINE COMPLETO
# =================================================================

def analisar(source: str):
    tokens = tokenize(source)
    programa = Parser(tokens).parse_programa()
    AnalisadorSemantico().visitar_bloco(programa.comandos)
    return tokens, programa


def transpilar(source: str) -> str:
    _, programa = analisar(source)
    return gerar_codigo_c(programa)


def ast_dict(valor):
    """Serializacao didatica da AST para --ast e demonstracoes."""
    if isinstance(valor, Node):
        return {"no": type(valor).__name__, **{
            chave: ast_dict(item) for chave, item in vars(valor).items()
        }}
    if isinstance(valor, list):
        return [ast_dict(item) for item in valor]
    return valor


# =================================================================
# 7. INTERFACE DE LINHA DE COMANDO
# =================================================================

def main(argv=None):
    cli = argparse.ArgumentParser(description="Transpila a linguagem Star Wars para C.")
    cli.add_argument("arquivo", nargs="?", type=Path, help="arquivo .starwars")
    cli.add_argument("-o", "--saida", type=Path, help="salva o codigo C neste caminho")
    cli.add_argument("--tokens", action="store_true", help="mostra os tokens no stderr")
    cli.add_argument("--ast", action="store_true", help="mostra a AST no stderr")
    args = cli.parse_args(argv)
    try:
        arquivo = args.arquivo
        if arquivo is None:
            arquivos = sorted(Path.cwd().glob("*.starwars"))
            if len(arquivos) != 1:
                raise CompilerError(
                    "Informe o arquivo .starwars: a pasta deve conter exatamente um "
                    "quando o argumento for omitido."
                )
            arquivo = arquivos[0]
        if args.saida is not None and args.saida.resolve() == arquivo.resolve():
            raise CompilerError("O arquivo de saida deve ser diferente do arquivo fonte.")
        fonte = arquivo.read_text(encoding="utf-8")
        tokens, programa = analisar(fonte)
        codigo = gerar_codigo_c(programa)
        if args.tokens:
            for token in tokens:
                print(f"linha {token.line}: {token!r}", file=sys.stderr)
        if args.ast:
            print(json.dumps(ast_dict(programa), ensure_ascii=False, indent=2), file=sys.stderr)
        if args.saida:
            args.saida.write_text(codigo, encoding="utf-8")
            print(f"Codigo C salvo em {args.saida}", file=sys.stderr)
        else:
            print(codigo, end="")
        return 0
    except (CompilerError, OSError, UnicodeError) as erro:
        print(str(erro), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
