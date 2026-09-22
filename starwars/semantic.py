from __future__ import annotations

import math
from typing import List, Union

from .errors import CompilerError, ErrorKind
from .nodes import (FLOAT, INT, Assignment, BinaryOp, Comparison, Declaration, Expression, For, If,
                    Number, Print, Program, Read, Statement, StringLiteral, Variable, While)
from .symbols import Symbol, SymbolTable

INT_MAX = 2147483647
FLOAT_MAX = 3.4028234663852886e38

Positioned = Union[Statement, Expression]


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = SymbolTable()
        self.statement_checks = {
            Declaration: self.check_declaration,
            Assignment: self.check_assignment,
            Read: self.check_read,
            Print: self.check_print,
            If: self.check_if,
            While: self.check_while,
            For: self.check_for,
        }
        self.expression_types = {
            Number: self.type_of_number,
            Variable: self.type_of_variable,
            BinaryOp: self.type_of_binary_op,
        }

    def check(self, program: Program) -> None:
        self.check_block(program.statements)

    def check_block(self, statements: List[Statement]) -> None:
        for statement in statements:
            check = self.statement_checks.get(type(statement))
            if check is None:
                raise TypeError(f"comando desconhecido: {type(statement).__name__}")
            check(statement)

    def check_scoped_block(self, statements: List[Statement]) -> None:
        self.symbols.push()
        self.check_block(statements)
        self.symbols.pop()

    def check_declaration(self, node: Declaration) -> None:
        if self.symbols.declared_here(node.name):
            raise self.error(node, f"variável '{node.name}' já declarada neste escopo")
        # O nome só fica visível depois do inicializador: `x: int = x;` é erro.
        if node.init is not None:
            self.check_assignable(node.type_name, node.init, node.name, node)
        node.c_name = self.symbols.declare(node.name, node.type_name).c_name

    def check_assignment(self, node: Assignment) -> None:
        symbol = self.resolve_writable(node.name, node)
        node.c_name, node.type_name = symbol.c_name, symbol.type_name
        self.check_assignable(symbol.type_name, node.value, node.name, node)

    def check_read(self, node: Read) -> None:
        symbol = self.resolve_writable(node.name, node)
        node.c_name, node.type_name = symbol.c_name, symbol.type_name

    def check_print(self, node: Print) -> None:
        for item in node.items:
            if not isinstance(item, StringLiteral):
                self.type_of(item)

    def check_if(self, node: If) -> None:
        self.check_condition(node.condition)
        self.check_scoped_block(node.then_block)
        if node.else_block is not None:
            self.check_scoped_block(node.else_block)

    def check_while(self, node: While) -> None:
        self.check_condition(node.condition)
        self.check_scoped_block(node.body)

    def check_for(self, node: For) -> None:
        for limit in (node.start, node.stop):
            if self.type_of(limit) != INT:
                raise self.error(limit, "os limites do laço 'This is the way' devem ser inteiros")
        self.symbols.push()
        node.c_name = self.symbols.declare(node.name, INT, read_only=True).c_name
        node.limit_c_name = self.symbols.new_c_name()
        self.check_block(node.body)
        self.symbols.pop()

    def check_condition(self, condition: Comparison) -> None:
        self.type_of(condition.left)
        self.type_of(condition.right)

    def check_assignable(self, target_type: str, value: Expression, name: str, node: Positioned) -> None:
        value_type = self.type_of(value)
        if target_type == INT and value_type == FLOAT:
            raise self.error(node, "incompatibilidade de tipos: "
                                   f"não é possível atribuir float à variável int '{name}'")

    def resolve(self, name: str, node: Positioned) -> Symbol:
        symbol = self.symbols.lookup(name)
        if symbol is None:
            raise self.error(node, f"variável '{name}' não declarada neste escopo")
        return symbol

    def resolve_writable(self, name: str, node: Positioned) -> Symbol:
        symbol = self.resolve(name, node)
        if symbol.read_only:
            raise self.error(node, f"variável de controle '{name}' não pode ser alterada dentro do laço")
        return symbol

    def type_of(self, node: Expression) -> str:
        compute = self.expression_types.get(type(node))
        if compute is None:
            raise TypeError(f"expressão desconhecida: {type(node).__name__}")
        node.type_name = compute(node)
        return node.type_name

    def type_of_number(self, node: Number) -> str:
        if "." in node.text:
            value = float(node.text)
            type_name, out_of_range = FLOAT, not math.isfinite(value) or value > FLOAT_MAX
        else:
            digits = node.text.lstrip("0") or "0"
            type_name, out_of_range = INT, len(digits) > 10 or int(digits) > INT_MAX
        if out_of_range:
            raise self.error(node, f"literal fora do intervalo de {type_name}")
        return type_name

    def type_of_variable(self, node: Variable) -> str:
        symbol = self.resolve(node.name, node)
        node.c_name = symbol.c_name
        return symbol.type_name

    def type_of_binary_op(self, node: BinaryOp) -> str:
        operand_types = (self.type_of(node.left), self.type_of(node.right))
        return FLOAT if FLOAT in operand_types else INT

    @staticmethod
    def error(node: Positioned, message: str) -> CompilerError:
        return CompilerError(ErrorKind.SEMANTIC, message, node.line, node.column)
