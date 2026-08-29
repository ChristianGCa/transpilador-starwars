"""
TRANSPILADOR DIDATICO COMPLETO - tema STAR WARS.
Pipeline: LEXER -> PARSER -> AST -> SEMANTICA -> GERADOR DE CODIGO C

Gramatica (EBNF):
<Programa>    ::= "INICIA_SISTEMA" <Bloco> "LOGOUT"
<Bloco>       ::= { <Declaracao> | <Comando> }
<Tipo>        ::= "Você era o escolhido" | "Eu sou C3PO, ciborgue de relações humanas"
<Declaracao>  ::= <Tipo> id [ "Eu alterei o acordo" <Expressao> ] ";"
<Comando>     ::= <Atribuicao> | <Condicional> | <Repeticao> | <Escrita>
<Atribuicao>  ::= id "Eu alterei o acordo" <Expressao> ";"
<Escrita>     ::= "Hello There" "(" ( string | <Expressao> ) ")" ";"
<Condicional> ::= "Faça, ou não faça" "(" <ExprLogica> ")" <Bloco> [ "Tentativa não há" <Bloco> ] "LOGOUT"
<Repeticao>   ::= "Eu sinto uma perturbação na força" "(" <ExprLogica> ")" <Bloco> "LOGOUT"
<ExprLogica>  ::= <Expressao> <OpRel> <Expressao>
<OpRel>       ::= "Como deve ser" | "!=" | "I have the high ground" | "A força é forte nele"
                | "Você subestima meu poder" | "Não, eu sou seu pai"
<Expressao>   ::= <Termo> { ("Que a força esteja com você"|"Acabou anakin") <Termo> }
<Termo>       ::= <Fator> { ("Eu sou todos os jedi"|"Eu sou todos os sith") <Fator> }
<Fator>       ::= id | num | "(" <Expressao> ")"
"""

import re
import sys
import glob
import os

# =================================================================
# 1. LEXER
# =================================================================

# Palavras-chave multi-palavra (ordem importa: mais longas primeiro)
KEYWORDS_MULTIWORD = [
    ("INICIA",        "INICIA_SISTEMA"),
    ("LOGOUT",        "LOGOUT"),
    ("NUM_TYPE",      "Você era o escolhido"),
    ("STR_TYPE",      "Eu sou C3PO, ciborgue de relações humanas"),
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
    ("FOR",           "This is the way"),
    ("FUNCTION",      "Execute a ordem 66"),
    ("RETURN",        "Palpatine retornou"),
]

# Tokens simples (regex)
TOKEN_SPEC_SIMPLE = [
    ("SKIP",          r"[ \t]+"),
    ("NEWLINE",       r"\n"),
    ("COMMENT",       r"#.*"),
    ("NUM",           r"\d+(\.\d+)?"),
    ("STRING",        r'"[^"\n]*"'),
    ("NEQ",           r"!="),
    ("LPAREN",        r"\("),
    ("RPAREN",        r"\)"),
    ("SEMI",          r";"),
    ("ID",            r"[a-zA-Z_\u00c0-\u024f][a-zA-Z0-9_\u00c0-\u024f]*"),
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
            if source.startswith(kw, pos):
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
    def __init__(self, conteudo, line): self.conteudo, self.line = conteudo, line

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
            if self.checar("NUM_TYPE", "STR_TYPE"):
                comandos.append(self.parse_declaracao())
            else:
                comandos.append(self.parse_comando())
        return comandos

    def parse_declaracao(self):
        tipo_tok = self.atual()
        self.pos += 1
        tipo = "int" if tipo_tok.kind == "NUM_TYPE" else "float"
        nome_tok = self.esperar("ID")
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
        if self.checar("STRING"):
            conteudo = StringLit(self.atual().value, self.atual().line)
            self.pos += 1
        else:
            conteudo = self.parse_expressao()
        self.esperar("RPAREN")
        self.esperar("SEMI")
        return Escrita(conteudo, tok.line)

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
        self.tabela = {}  # nome -> tipo

    def tipo_de_expr(self, no, line):
        if isinstance(no, Num):
            return "float" if "." in no.valor else "int"
        if isinstance(no, Var):
            if no.nome not in self.tabela:
                raise CompilerError(
                    f"ERRO SEMANTICO (linha {line}): variavel '{no.nome}' usada antes de ser declarada"
                )
            return self.tabela[no.nome]
        if isinstance(no, BinOp):
            t1 = self.tipo_de_expr(no.esq, line)
            t2 = self.tipo_de_expr(no.dire, line)
            return "float" if "float" in (t1, t2) else "int"
        return "int"

    def visitar_bloco(self, comandos):
        for c in comandos:
            self.visitar(c)

    def visitar(self, no):
        if isinstance(no, Declaracao):
            if no.nome in self.tabela:
                raise CompilerError(
                    f"ERRO SEMANTICO (linha {no.line}): variavel '{no.nome}' ja declarada"
                )
            self.tabela[no.nome] = no.tipo
            if no.expr is not None:
                self.tipo_de_expr(no.expr, no.line)
        elif isinstance(no, Atribuicao):
            if no.nome not in self.tabela:
                raise CompilerError(
                    f"ERRO SEMANTICO (linha {no.line}): atribuicao a variavel '{no.nome}' nao declarada"
                )
            t_expr = self.tipo_de_expr(no.expr, no.line)
            t_var = self.tabela[no.nome]
            if t_var == "int" and t_expr == "float":
                raise CompilerError(
                    f"ERRO SEMANTICO (linha {no.line}): incompatibilidade de tipos - "
                    f"nao e possivel atribuir float a variavel 'Você era o escolhido' '{no.nome}' sem conversao"
                )
        elif isinstance(no, Escrita):
            if not isinstance(no.conteudo, StringLit):
                self.tipo_de_expr(no.conteudo, no.line)
        elif isinstance(no, Condicional):
            self.tipo_de_expr(no.cond.esq, no.line)
            self.tipo_de_expr(no.cond.dire, no.line)
            self.visitar_bloco(no.bloco_if)
            if no.bloco_else:
                self.visitar_bloco(no.bloco_else)
        elif isinstance(no, Repeticao):
            self.tipo_de_expr(no.cond.esq, no.line)
            self.tipo_de_expr(no.cond.dire, no.line)
            self.visitar_bloco(no.bloco)


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

def gerar_expr(no):
    if isinstance(no, Num):
        return no.valor + ("f" if "." in no.valor else "")
    if isinstance(no, Var):
        return no.nome
    if isinstance(no, BinOp):
        op_c = ARITH_MAP.get(no.op, no.op)
        return f"({gerar_expr(no.esq)} {op_c} {gerar_expr(no.dire)})"
    raise CompilerError("no de expressao desconhecido no gerador")

def gerar_bloco(comandos, indent=1):
    linhas = []
    pad = "    " * indent
    for c in comandos:
        if isinstance(c, Declaracao):
            init = f" = {gerar_expr(c.expr)}" if c.expr else ""
            linhas.append(f"{pad}{c.tipo} {c.nome}{init};")
        elif isinstance(c, Atribuicao):
            linhas.append(f"{pad}{c.nome} = {gerar_expr(c.expr)};")
        elif isinstance(c, Escrita):
            if isinstance(c.conteudo, StringLit):
                linhas.append(f'{pad}printf({c.conteudo.valor});')
            else:
                linhas.append(f'{pad}printf("%g\\n", (double)({gerar_expr(c.conteudo)}));')
        elif isinstance(c, Condicional):
            op_c = OP_MAP.get(c.cond.op, c.cond.op)
            cond = f"{gerar_expr(c.cond.esq)} {op_c} {gerar_expr(c.cond.dire)}"
            linhas.append(f"{pad}if ({cond}) {{")
            linhas.extend(gerar_bloco(c.bloco_if, indent + 1))
            if c.bloco_else:
                linhas.append(f"{pad}}} else {{")
                linhas.extend(gerar_bloco(c.bloco_else, indent + 1))
            linhas.append(f"{pad}}}")
        elif isinstance(c, Repeticao):
            op_c = OP_MAP.get(c.cond.op, c.cond.op)
            cond = f"{gerar_expr(c.cond.esq)} {op_c} {gerar_expr(c.cond.dire)}"
            linhas.append(f"{pad}while ({cond}) {{")
            linhas.extend(gerar_bloco(c.bloco, indent + 1))
            linhas.append(f"{pad}}}")
    return linhas

def gerar_codigo_c(programa: Programa) -> str:
    corpo = "\n".join(gerar_bloco(programa.comandos))
    return f"#include <stdio.h>\n\nint main(void) {{\n{corpo}\n    return 0;\n}}\n"


# =================================================================
# 6. PIPELINE COMPLETO
# =================================================================

def transpilar(source: str) -> str:
    tokens = tokenize(source)
    programa = Parser(tokens).parse_programa()
    AnalisadorSemantico().visitar_bloco(programa.comandos)
    return gerar_codigo_c(programa)


# =================================================================
# 7. MAIN - le arquivo .starwars no diretorio atual
# =================================================================

if __name__ == "__main__":
    # Busca arquivo .starwars no diretório atual
    arquivos = glob.glob(os.path.join(os.getcwd(), "*.starwars"))

    if not arquivos:
        print("Nenhum arquivo .starwars encontrado no diretório atual.")
        sys.exit(1)

    if len(arquivos) > 1:
        print(f"Multiplos arquivos .starwars encontrados: {arquivos}")
        print(f"Usando o primeiro: {arquivos[0]}")

    arquivo = arquivos[0]
    print(f"{'='*60}")
    print(f"Lendo arquivo: {arquivo}")
    print(f"{'='*60}")

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            fonte = f.read()

        c_code = transpilar(fonte)
        print("SUCESSO. Codigo C gerado:\n")
        print(c_code)

    except CompilerError as e:
        print(str(e))
    except OSError as e:
        print(f"ERRO ao ler arquivo: {e}")
