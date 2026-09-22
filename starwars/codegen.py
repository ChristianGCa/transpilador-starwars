from __future__ import annotations

from typing import List, Union

from .nodes import (INT, Assignment, BinaryOp, Comparison, Declaration, Expression, For, If,
                    Number, Print, Program, Read, Statement, StringLiteral, Variable, While)

INDENT = "    "


def generate_c(program: Program) -> str:
    body = "\n".join(CGenerator().block(program.statements, 1))
    return f"#include <stdio.h>\n\nint main(void) {{\n{body}\n    return 0;\n}}\n"


def c_string(literal: str) -> str:
    # Evita que trigraphs do C99 mudem textos como "??/" antes do parsing do C.
    return literal.replace("?", r"\?")


def c_number(text: str) -> str:
    if "." in text:
        integer, fraction = text.split(".")
        return f"{integer.lstrip('0') or '0'}.{fraction}f"
    return text.lstrip("0") or "0"


def c_expression(node: Expression) -> str:
    if isinstance(node, Number):
        return c_number(node.text)
    if isinstance(node, Variable):
        return node.c_name
    if isinstance(node, BinaryOp):
        return f"({c_expression(node.left)} {node.op} {c_expression(node.right)})"
    raise TypeError(f"expressão desconhecida: {type(node).__name__}")


def c_condition(condition: Comparison) -> str:
    return f"{c_expression(condition.left)} {condition.op} {c_expression(condition.right)}"


def c_print_call(item: Union[StringLiteral, Expression]) -> str:
    if isinstance(item, StringLiteral):
        return f'printf("%s", {c_string(item.text)});'
    if item.type_name == INT:
        return f'printf("%d", {c_expression(item)});'
    return f'printf("%g", (double)({c_expression(item)}));'


class CGenerator:
    def __init__(self):
        self.emitters = {
            Declaration: self.emit_declaration,
            Assignment: self.emit_assignment,
            Read: self.emit_read,
            Print: self.emit_print,
            If: self.emit_if,
            While: self.emit_while,
            For: self.emit_for,
        }

    def block(self, statements: List[Statement], depth: int) -> List[str]:
        lines = []
        for statement in statements:
            emit = self.emitters.get(type(statement))
            if emit is None:
                raise TypeError(f"comando desconhecido: {type(statement).__name__}")
            lines.extend(emit(statement, depth))
        return lines

    def emit_declaration(self, node: Declaration, depth: int) -> List[str]:
        init = c_expression(node.init) if node.init is not None else "0"
        return [f"{INDENT * depth}{node.type_name} {node.c_name} = {init};"]

    def emit_assignment(self, node: Assignment, depth: int) -> List[str]:
        return [f"{INDENT * depth}{node.c_name} = {c_expression(node.value)};"]

    def emit_read(self, node: Read, depth: int) -> List[str]:
        pad = INDENT * depth
        lines = []
        if node.prompt is not None:
            lines += [f'{pad}printf("%s", {c_string(node.prompt)});', f"{pad}fflush(stdout);"]
        conversion = "%d" if node.type_name == INT else "%f"
        return lines + [
            f'{pad}if (scanf("{conversion}", &{node.c_name}) != 1) {{',
            f'{pad}    fprintf(stderr, "ERRO DE ENTRADA (linha {node.line}): esperado valor numerico.\\n");',
            f"{pad}    return 1;",
            f"{pad}}}",
        ]

    def emit_print(self, node: Print, depth: int) -> List[str]:
        pad = INDENT * depth
        lines = [f"{pad}{c_print_call(item)}" for item in node.items]
        if any(not isinstance(item, StringLiteral) for item in node.items):
            lines.append(f'{pad}printf("\\n");')
        return lines

    def emit_if(self, node: If, depth: int) -> List[str]:
        pad = INDENT * depth
        lines = [f"{pad}if ({c_condition(node.condition)}) {{", *self.block(node.then_block, depth + 1)]
        if node.else_block is not None:
            lines += [f"{pad}}} else {{", *self.block(node.else_block, depth + 1)]
        return lines + [f"{pad}}}"]

    def emit_while(self, node: While, depth: int) -> List[str]:
        pad = INDENT * depth
        return [f"{pad}while ({c_condition(node.condition)}) {{", *self.block(node.body, depth + 1), f"{pad}}}"]

    def emit_for(self, node: For, depth: int) -> List[str]:
        pad = INDENT * depth
        counter, limit = node.c_name, node.limit_c_name
        header = (f"for (int {counter} = {c_expression(node.start)}, {limit} = {c_expression(node.stop)}; "
                  f"{counter} <= {limit}; {counter}++) {{")
        return [f"{pad}{header}", *self.block(node.body, depth + 1), f"{pad}}}"]
