from __future__ import annotations

from typing import Callable, List, Tuple, Union

from .errors import CompilerError, ErrorKind
from .nodes import (FLOAT, INT, Assignment, BinaryOp, Call, CallStatement, Comparison, Declaration,
                    Expression, For, Function, If, Number, Parameter, Print, Program, Read, Return,
                    Statement, StringLiteral, Variable, While)
from .tokens import ARITHMETIC_OPERATORS, COMPARISON_OPERATORS, Token, TokenKind

TYPE_KEYWORDS = {TokenKind.INT_TYPE: INT, TokenKind.FLOAT_TYPE: FLOAT}
ADDITIVE = (TokenKind.PLUS, TokenKind.MINUS)
MULTIPLICATIVE = (TokenKind.STAR, TokenKind.SLASH)


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.statement_parsers = {
            TokenKind.ID: self.parse_assignment_or_call,
            TokenKind.PRINT: self.parse_print,
            TokenKind.INPUT: self.parse_read,
            TokenKind.IF: self.parse_if,
            TokenKind.WHILE: self.parse_while,
            TokenKind.FOR: self.parse_for,
            TokenKind.RETURN: self.parse_return,
            TokenKind.FUNCTION: self.reject_late_function,
        }

    def current(self) -> Token:
        return self.tokens[self.pos]

    def peek(self) -> Token:
        return self.tokens[min(self.pos + 1, len(self.tokens) - 1)]

    def check(self, *kinds: TokenKind) -> bool:
        return self.current().kind in kinds

    def advance(self) -> Token:
        token = self.current()
        self.pos += 1
        return token

    def found(self) -> str:
        token = self.current()
        if token.kind is TokenKind.EOF:
            return TokenKind.EOF.value
        if token.kind is TokenKind.STRING:
            return token.lexeme
        return f"'{token.lexeme}'"

    def expect(self, kind: TokenKind) -> Token:
        if not self.check(kind):
            raise self.error(f"esperado {kind.value}, encontrado {self.found()}")
        return self.advance()

    def error(self, message: str) -> CompilerError:
        token = self.current()
        return CompilerError(ErrorKind.SYNTAX, message, token.line, token.column)

    def parse_program(self) -> Program:
        self.expect(TokenKind.BEGIN)
        functions = []
        while self.check(TokenKind.FUNCTION):
            functions.append(self.parse_function())
        statements = self.parse_block(TokenKind.END)
        self.expect(TokenKind.END)
        self.expect(TokenKind.EOF)
        return Program(statements, functions)

    def parse_function(self) -> Function:
        keyword = self.expect(TokenKind.FUNCTION)
        name = self.expect(TokenKind.ID)
        self.expect(TokenKind.LPAREN)
        params = []
        if not self.check(TokenKind.RPAREN):
            params.append(self.parse_parameter())
            while self.check(TokenKind.COMMA):
                self.advance()
                params.append(self.parse_parameter())
        self.expect(TokenKind.RPAREN)
        return_type = None
        if self.check(TokenKind.COLON):
            self.advance()
            return_type = self.parse_type()
        body = self.parse_block(TokenKind.END)
        self.expect(TokenKind.END)
        return Function(name.lexeme, params, return_type, body, keyword.line, keyword.column)

    def parse_parameter(self) -> Parameter:
        name = self.expect(TokenKind.ID)
        self.expect(TokenKind.COLON)
        return Parameter(name.lexeme, self.parse_type(), name.line, name.column)

    def parse_type(self) -> str:
        if not self.check(*TYPE_KEYWORDS):
            raise self.error(f"esperado tipo inteiro ou real, encontrado {self.found()}")
        return TYPE_KEYWORDS[self.advance().kind]

    def reject_late_function(self) -> Statement:
        raise self.error("funções devem ser definidas logo após o início do programa")

    def parse_block(self, *terminators: TokenKind) -> List[Statement]:
        statements = []
        while not self.check(*terminators, TokenKind.EOF):
            if self.at_declaration():
                statements.append(self.parse_declaration())
            else:
                statements.append(self.parse_statement())
        return statements

    def at_declaration(self) -> bool:
        if self.check(*TYPE_KEYWORDS):
            return True
        return self.check(TokenKind.ID) and self.peek().kind is TokenKind.COLON

    def parse_declaration(self) -> Declaration:
        start = self.current()
        if self.check(TokenKind.ID):
            name = self.advance()
            self.expect(TokenKind.COLON)
            type_name = self.parse_type()
        else:
            type_name = self.parse_type()
            name = self.expect(TokenKind.ID)
        init = None
        if self.check(TokenKind.ASSIGN):
            self.advance()
            init = self.parse_expression()
        self.expect(TokenKind.SEMI)
        return Declaration(type_name, name.lexeme, init, start.line, start.column)

    def parse_statement(self) -> Statement:
        parse = self.statement_parsers.get(self.current().kind)
        if parse is None:
            raise self.error(f"comando inválido começando com '{self.current().lexeme}'")
        return parse()

    def parse_assignment_or_call(self) -> Statement:
        if self.peek().kind is TokenKind.LPAREN:
            call = self.parse_call()
            self.expect(TokenKind.SEMI)
            return CallStatement(call, call.line, call.column)
        return self.parse_assignment()

    def parse_return(self) -> Return:
        keyword = self.expect(TokenKind.RETURN)
        value = None
        if not self.check(TokenKind.SEMI):
            value = self.parse_expression()
        self.expect(TokenKind.SEMI)
        return Return(value, keyword.line, keyword.column)

    def parse_call(self) -> Call:
        name = self.expect(TokenKind.ID)
        self.expect(TokenKind.LPAREN)
        args = []
        if not self.check(TokenKind.RPAREN):
            args.append(self.parse_expression())
            while self.check(TokenKind.COMMA):
                self.advance()
                args.append(self.parse_expression())
        self.expect(TokenKind.RPAREN)
        return Call(name.lexeme, args, name.line, name.column)

    def parse_assignment(self) -> Assignment:
        name = self.expect(TokenKind.ID)
        self.expect(TokenKind.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenKind.SEMI)
        return Assignment(name.lexeme, value, name.line, name.column)

    def parse_print(self) -> Print:
        keyword = self.expect(TokenKind.PRINT)
        self.expect(TokenKind.LPAREN)
        items = [self.parse_print_item()]
        while self.check(TokenKind.COMMA):
            self.advance()
            items.append(self.parse_print_item())
        self.expect(TokenKind.RPAREN)
        self.expect(TokenKind.SEMI)
        return Print(items, keyword.line, keyword.column)

    def parse_print_item(self) -> Union[StringLiteral, Expression]:
        if self.check(TokenKind.STRING):
            token = self.advance()
            return StringLiteral(token.lexeme, token.line, token.column)
        return self.parse_expression()

    def parse_read(self) -> Read:
        keyword = self.expect(TokenKind.INPUT)
        self.expect(TokenKind.LPAREN)
        prompt = None
        if self.check(TokenKind.STRING):
            prompt = self.advance().lexeme
            self.expect(TokenKind.ARROW)
        name = self.expect(TokenKind.ID)
        self.expect(TokenKind.RPAREN)
        self.expect(TokenKind.SEMI)
        return Read(name.lexeme, prompt, keyword.line, keyword.column)

    def parse_if(self) -> If:
        keyword = self.expect(TokenKind.IF)
        condition = self.parse_condition()
        then_block = self.parse_block(TokenKind.ELSE, TokenKind.END)
        else_block = None
        if self.check(TokenKind.ELSE):
            self.advance()
            else_block = self.parse_block(TokenKind.END)
        self.expect(TokenKind.END)
        return If(condition, then_block, else_block, keyword.line, keyword.column)

    def parse_while(self) -> While:
        keyword = self.expect(TokenKind.WHILE)
        condition = self.parse_condition()
        body = self.parse_block(TokenKind.END)
        self.expect(TokenKind.END)
        return While(condition, body, keyword.line, keyword.column)

    def parse_for(self) -> For:
        keyword = self.expect(TokenKind.FOR)
        self.expect(TokenKind.LPAREN)
        name = self.expect(TokenKind.ID)
        self.expect(TokenKind.FROM)
        start = self.parse_expression()
        self.expect(TokenKind.TO)
        stop = self.parse_expression()
        self.expect(TokenKind.RPAREN)
        body = self.parse_block(TokenKind.END)
        self.expect(TokenKind.END)
        return For(name.lexeme, start, stop, body, keyword.line, keyword.column)

    def parse_condition(self) -> Comparison:
        self.expect(TokenKind.LPAREN)
        left = self.parse_expression()
        if not self.check(*COMPARISON_OPERATORS):
            raise self.error(f"esperado operador relacional, encontrado {self.found()}")
        operator = self.advance()
        right = self.parse_expression()
        self.expect(TokenKind.RPAREN)
        return Comparison(left, COMPARISON_OPERATORS[operator.kind], right, operator.line, operator.column)

    def parse_expression(self) -> Expression:
        return self.parse_left_associative(self.parse_term, ADDITIVE)

    def parse_term(self) -> Expression:
        return self.parse_left_associative(self.parse_factor, MULTIPLICATIVE)

    def parse_left_associative(self, parse_operand: Callable[[], Expression],
                               operators: Tuple[TokenKind, ...]) -> Expression:
        node = parse_operand()
        while self.check(*operators):
            operator = self.advance()
            right = parse_operand()
            node = BinaryOp(node, ARITHMETIC_OPERATORS[operator.kind], right, operator.line, operator.column)
        return node

    def parse_factor(self) -> Expression:
        token = self.current()
        if token.kind is TokenKind.ID and self.peek().kind is TokenKind.LPAREN:
            return self.parse_call()
        if token.kind is TokenKind.ID:
            self.advance()
            return Variable(token.lexeme, token.line, token.column)
        if token.kind is TokenKind.NUM:
            self.advance()
            return Number(token.lexeme, token.line, token.column)
        if token.kind is TokenKind.LPAREN:
            self.advance()
            node = self.parse_expression()
            self.expect(TokenKind.RPAREN)
            return node
        raise self.error(f"esperado identificador, número ou '(', encontrado {self.found()}")
