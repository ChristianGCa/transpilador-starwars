from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from typing import Any, List, Optional, Union

INT = "int"
FLOAT = "float"


@dataclass
class Number:
    text: str
    line: int
    column: int
    type_name: Optional[str] = None


@dataclass
class StringLiteral:
    text: str
    line: int
    column: int


@dataclass
class Variable:
    name: str
    line: int
    column: int
    c_name: Optional[str] = None
    type_name: Optional[str] = None


@dataclass
class BinaryOp:
    left: Expression
    op: str
    right: Expression
    line: int
    column: int
    type_name: Optional[str] = None


Expression = Union[Number, Variable, BinaryOp]


@dataclass
class Comparison:
    left: Expression
    op: str
    right: Expression
    line: int
    column: int


@dataclass
class Declaration:
    type_name: str
    name: str
    init: Optional[Expression]
    line: int
    column: int
    c_name: Optional[str] = None


@dataclass
class Assignment:
    name: str
    value: Expression
    line: int
    column: int
    c_name: Optional[str] = None
    type_name: Optional[str] = None


@dataclass
class Print:
    items: List[Union[StringLiteral, Expression]]
    line: int
    column: int


@dataclass
class Read:
    name: str
    prompt: Optional[str]
    line: int
    column: int
    c_name: Optional[str] = None
    type_name: Optional[str] = None


@dataclass
class If:
    condition: Comparison
    then_block: List[Statement]
    else_block: Optional[List[Statement]]
    line: int
    column: int


@dataclass
class While:
    condition: Comparison
    body: List[Statement]
    line: int
    column: int


Statement = Union[Declaration, Assignment, Print, Read, If, While]


@dataclass
class Program:
    statements: List[Statement]


def to_dict(value: Any) -> Any:
    if is_dataclass(value):
        return {"node": type(value).__name__,
                **{field.name: to_dict(getattr(value, field.name)) for field in fields(value)}}
    if isinstance(value, list):
        return [to_dict(item) for item in value]
    return value
