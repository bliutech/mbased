from __future__ import annotations
from enum import Enum


class Var:

    def __init__(self, name: str):

        self.name = name

    def __str__(self) -> str:
        return self.name


class Expr:

    def __init__(self, first: Var | Expr, second: ExprPrime = None):

        self.first = first
        self.second = second

    def __str__(self) -> str:

        if self.second is None:
            return str(self.first)  # when ExprPrime is not needed or nullable

        return f"{self.first} {self.second}"  # when Expr = Var ExprPrime and ExprPrime is not nullable


class ExprPrime:

    def __init__(self, first: ExprPrime):
        self.first = first

    def __str__(self) -> str:
        return str(self.first)


class AndExpr(ExprPrime):

    def __init__(self, first: Expr):

        self.first = first

    def __str__(self) -> str:
        return f"& {self.first}"


class OrExpr(ExprPrime):

    def __init__(self, first: Expr):
        self.first = first

    def __str__(self) -> str:
        return f"| {self.first}"


class NotExpr(Expr):

    def __init__(self, first: Expr):
        self.first = first

    def __str__(self) -> str:
        return f"!{self.first}"


class ParenExpr(Expr):
    def __init__(self, first: Expr):
        self.first = first

    def __str__(self) -> str:
        return f"({self.first})"
