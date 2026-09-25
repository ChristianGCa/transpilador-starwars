from __future__ import annotations

from typing import List, Union

from .nodes import (INT, Assignment, BinaryOp, Call, CallStatement, Comparison, Declaration,
                    Expression, For, Function, If, Number, Print, Program, Read, Return, Statement,
                    StringLiteral, Variable, While)

INDENT = "    "


def generate_c(program: Program) -> str:
    headers = "#include <stdio.h>\n"
    functions = ""
    if program.functions:
        headers += "#include <stdlib.h>\n"
        prototypes = "".join(f"{c_signature(function)};\n" for function in program.functions)
        definitions = "".join(f"\n{c_function(function)}" for function in program.functions)
        functions = f"\n{prototypes}{definitions}"
    body = "\n".join(CGenerator(in_function=False).block(program.statements, 1))
    return f"{headers}{functions}\nint main(void) {{\n{body}\n    return 0;\n}}\n"


def c_signature(function: Function) -> str:
    params = ", ".join(f"{param.type_name} {param.c_name}" for param in function.params) or "void"
    return f"{function.return_type or 'void'} {function.c_name}({params})"


def c_function(function: Function) -> str:
    body = "".join(f"{line}\n" for line in CGenerator(in_function=True).block(function.body, 1))
    return f"{c_signature(function)} {{\n{body}}}\n"


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
    if isinstance(node, Call):
        return f"{node.c_name}({', '.join(c_expression(arg) for arg in node.args)})"
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
    def __init__(self, in_function: bool):
        self.in_function = in_function
        self.emitters = {
            Declaration: self.emit_declaration,
            Assignment: self.emit_assignment,
            Read: self.emit_read,
            Print: self.emit_print,
            If: self.emit_if,
            While: self.emit_while,
            For: self.emit_for,
            CallStatement: self.emit_call_statement,
            Return: self.emit_return,
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
        # Fora do main, `return 1` não encerra o programa; por isso as funções usam exit(1).
        stop = "exit(1);" if self.in_function else "return 1;"
        return lines + [
            f'{pad}if (scanf("{conversion}", &{node.c_name}) != 1) {{',
            f'{pad}    fprintf(stderr, "ERRO DE ENTRADA (linha {node.line}): esperado valor numerico.\\n");',
            f"{pad}    {stop}",
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

    def emit_call_statement(self, node: CallStatement, depth: int) -> List[str]:
        return [f"{INDENT * depth}{c_expression(node.call)};"]

    def emit_return(self, node: Return, depth: int) -> List[str]:
        if node.value is None:
            return [f"{INDENT * depth}return;"]
        return [f"{INDENT * depth}return {c_expression(node.value)};"]

    def emit_for(self, node: For, depth: int) -> List[str]:
        pad = INDENT * depth
        counter, limit = node.c_name, node.limit_c_name
        header = (f"for (int {counter} = {c_expression(node.start)}, {limit} = {c_expression(node.stop)}; "
                  f"{counter} <= {limit}; {counter}++) {{")
        return [f"{pad}{header}", *self.block(node.body, depth + 1), f"{pad}}}"]
