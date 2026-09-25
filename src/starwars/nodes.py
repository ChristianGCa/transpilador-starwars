from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
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


@dataclass
class Call:
    name: str
    args: List[Expression]
    line: int
    column: int
    c_name: Optional[str] = None
    type_name: Optional[str] = None


Expression = Union[Number, Variable, BinaryOp, Call]


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


@dataclass
class For:
    name: str
    start: Expression
    stop: Expression
    body: List[Statement]
    line: int
    column: int
    c_name: Optional[str] = None
    limit_c_name: Optional[str] = None


@dataclass
class CallStatement:
    call: Call
    line: int
    column: int


@dataclass
class Return:
    value: Optional[Expression]
    line: int
    column: int


Statement = Union[Declaration, Assignment, Print, Read, If, While, For, CallStatement, Return]


@dataclass
class Parameter:
    name: str
    type_name: str
    line: int
    column: int
    c_name: Optional[str] = None


@dataclass
class Function:
    name: str
    params: List[Parameter]
    return_type: Optional[str]
    body: List[Statement]
    line: int
    column: int
    c_name: Optional[str] = None


@dataclass
class Program:
    statements: List[Statement]
    functions: List[Function] = field(default_factory=list)


def to_dict(value: Any) -> Any:
    if is_dataclass(value):
        return {"node": type(value).__name__,
                **{field.name: to_dict(getattr(value, field.name)) for field in fields(value)}}
    if isinstance(value, list):
        return [to_dict(item) for item in value]
    return value
