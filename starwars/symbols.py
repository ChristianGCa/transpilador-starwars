from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Symbol:
    type_name: str
    c_name: str


class SymbolTable:
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]
        self.next_id = 0

    def push(self) -> None:
        self.scopes.append({})

    def pop(self) -> None:
        self.scopes.pop()

    def declared_here(self, name: str) -> bool:
        return name in self.scopes[-1]

    def declare(self, name: str, type_name: str) -> Symbol:
        symbol = Symbol(type_name, f"sw_v{self.next_id}")
        self.next_id += 1
        self.scopes[-1][name] = symbol
        return symbol

    def lookup(self, name: str) -> Optional[Symbol]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
