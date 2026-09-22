from __future__ import annotations

import math
from typing import Dict, List, Optional, Union

from .errors import CompilerError, ErrorKind
from .nodes import (FLOAT, INT, Assignment, BinaryOp, Call, CallStatement, Comparison, Declaration,
                    Expression, For, Function, If, Number, Parameter, Print, Program, Read, Return,
                    Statement, StringLiteral, Variable, While)
from .symbols import Symbol, SymbolTable

INT_MAX = 2147483647
FLOAT_MAX = 3.4028234663852886e38

Positioned = Union[Statement, Expression, Function, Parameter]


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = SymbolTable()
        self.functions: Dict[str, Function] = {}
        self.current_function: Optional[Function] = None
        self.statement_checks = {
            Declaration: self.check_declaration,
            Assignment: self.check_assignment,
            Read: self.check_read,
            Print: self.check_print,
            If: self.check_if,
            While: self.check_while,
            For: self.check_for,
            CallStatement: self.check_call_statement,
            Return: self.check_return,
        }
        self.expression_types = {
            Number: self.type_of_number,
            Variable: self.type_of_variable,
            BinaryOp: self.type_of_binary_op,
            Call: self.type_of_call,
        }

    def check(self, program: Program) -> None:
        for function in program.functions:
            self.register_function(function)
        # Funções são verificadas antes do programa principal, cujas variáveis ainda não
        # existem: assim uma função só enxerga seus parâmetros e variáveis.
        for function in program.functions:
            self.check_function(function)
        self.check_block(program.statements)

    def register_function(self, function: Function) -> None:
        if function.name in self.functions:
            raise self.error(function, f"função '{function.name}' já declarada")
        function.c_name = f"sw_f{len(self.functions)}"
        self.functions[function.name] = function

    def check_function(self, function: Function) -> None:
        self.current_function = function
        self.symbols.push()
        for param in function.params:
            self.check_new_name(param.name, param)
            param.c_name = self.symbols.declare(param.name, param.type_name).c_name
        self.check_block(function.body)
        self.symbols.pop()
        self.current_function = None
        if function.return_type is not None and not always_returns(function.body):
            raise self.error(function, f"a função '{function.name}' pode terminar sem 'Palpatine retornou'")

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

    def check_new_name(self, name: str, node: Positioned) -> None:
        if self.symbols.declared_here(name):
            raise self.error(node, f"variável '{name}' já declarada neste escopo")
        if name in self.functions:
            raise self.error(node, f"'{name}' já é o nome de uma função")

    def check_declaration(self, node: Declaration) -> None:
        self.check_new_name(node.name, node)
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
        self.check_new_name(node.name, node)
        node.c_name = self.symbols.declare(node.name, INT, read_only=True).c_name
        node.limit_c_name = self.symbols.new_c_name()
        self.check_block(node.body)
        self.symbols.pop()

    def check_call_statement(self, node: CallStatement) -> None:
        self.check_call(node.call)

    def check_return(self, node: Return) -> None:
        function = self.current_function
        if function is None:
            raise self.error(node, "'Palpatine retornou' só pode ser usado dentro de uma função")
        if function.return_type is None:
            if node.value is not None:
                raise self.error(node, f"a função '{function.name}' não retorna valor")
            return
        if node.value is None:
            raise self.error(node, f"a função '{function.name}' deve retornar um valor do tipo "
                                   f"{function.return_type}")
        if self.type_of(node.value) == FLOAT and function.return_type == INT:
            raise self.error(node, "incompatibilidade de tipos: "
                                   f"a função '{function.name}' deve retornar int")

    def check_call(self, node: Call) -> Optional[str]:
        function = self.functions.get(node.name)
        if function is None:
            raise self.error(node, f"função '{node.name}' não declarada")
        expected, received = len(function.params), len(node.args)
        if expected != received:
            raise self.error(node, f"a função '{node.name}' espera {count_arguments(expected)}, "
                                   f"mas recebeu {received}")
        for position, (arg, param) in enumerate(zip(node.args, function.params), start=1):
            if self.type_of(arg) == FLOAT and param.type_name == INT:
                raise self.error(arg, "incompatibilidade de tipos: "
                                      f"o argumento {position} de '{node.name}' deve ser int")
        node.c_name = function.c_name
        return function.return_type

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

    def type_of_call(self, node: Call) -> str:
        return_type = self.check_call(node)
        if return_type is None:
            raise self.error(node, f"a função '{node.name}' não retorna valor "
                                   "e não pode ser usada em expressões")
        return return_type

    @staticmethod
    def error(node: Positioned, message: str) -> CompilerError:
        return CompilerError(ErrorKind.SEMANTIC, message, node.line, node.column)


def always_returns(statements: List[Statement]) -> bool:
    return any(statement_always_returns(statement) for statement in statements)


def statement_always_returns(statement: Statement) -> bool:
    if isinstance(statement, Return):
        return True
    if isinstance(statement, If) and statement.else_block is not None:
        return always_returns(statement.then_block) and always_returns(statement.else_block)
    return False


def count_arguments(count: int) -> str:
    return f"{count} argumento" if count == 1 else f"{count} argumentos"
