from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from .codegen import generate_c
from .errors import CompilerError
from .lexer import tokenize
from .nodes import to_dict
from .pipeline import build_program


class CliError(Exception):
    pass


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="starwars", description="Transpila a linguagem Star Wars para C.")
    parser.add_argument("source", nargs="?", type=Path, metavar="arquivo", help="arquivo .starwars")
    parser.add_argument("-o", "--saida", dest="output", type=Path, help="salva o código C neste caminho")
    parser.add_argument("--tokens", action="store_true", help="mostra os tokens no stderr")
    parser.add_argument("--ast", action="store_true", help="mostra a AST no stderr")
    return parser


def find_source(source: Optional[Path]) -> Path:
    if source is not None:
        return source
    candidates = sorted(Path.cwd().glob("*.starwars"))
    if len(candidates) != 1:
        raise CliError("Informe o arquivo .starwars: a pasta deve conter exatamente um "
                       "quando o argumento for omitido.")
    return candidates[0]


def run(args: argparse.Namespace) -> None:
    source = find_source(args.source)
    if args.output is not None and args.output.resolve() == source.resolve():
        raise CliError("O arquivo de saída deve ser diferente do arquivo fonte.")
    tokens = tokenize(source.read_text(encoding="utf-8"))
    if args.tokens:
        for token in tokens:
            print(f"linha {token.line}, coluna {token.column}: {token!r}", file=sys.stderr)
    program = build_program(tokens)
    if args.ast:
        print(json.dumps(to_dict(program), ensure_ascii=False, indent=2), file=sys.stderr)
    code = generate_c(program)
    if args.output is None:
        print(code, end="")
    else:
        args.output.write_text(code, encoding="utf-8")
        print(f"Código C salvo em {args.output}", file=sys.stderr)


def main(argv: Optional[List[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    try:
        run(args)
    except (CompilerError, CliError, OSError, UnicodeError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0
