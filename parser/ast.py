from __future__ import annotations
from enum import Enum


class Var:
    """
    A class to represent a variable from A-Z.

    Attributes
    ----------
    name : str
        The name of the variable.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name


class Expr:
    """
    An interface class to represent a full expression.
    """

    pass


class ExprPrime:
    """
    An interface class to represent a prime expression. Used to eliminate left-recursion.
    """

    pass

    # def __init__(self, first: ExprPrime = None):
    #  self.first = first
    # def __str__(self) -> str:
    #  if self.first is None:
    #      return "ε"
    #  return str(self.first)


class AndExpr(ExprPrime):
    """
    A class to represent an AND expression.

    Attributes
    ----------
    first : Expr
        The first part of the AND expression.
    """

    def __init__(self, first: Expr):
        self.first = first

    def __str__(self) -> str:
        return f"& {self.first}"


class OrExpr(ExprPrime):
    """
    A class to represent an OR expression.

    Attributes
    ----------
    first : Expr
        The first part of the OR expression.
    """

    def __init__(self, first: Expr):
        self.first = first

    def __str__(self) -> str:
        return f"| {self.first}"


class VarExpr(Expr):
    """
    A class to represent an expression containing only a Var node.

    Attributes
    ----------
    first : Var
        The variable contained by the VarExpr.

    second : ExprPrime, Optional
        Optional attribute for containing the "AndExpr", "OrExpr", or "None" (for epsilon case).
    """

    def __init__(self, first: Var, second: ExprPrime = None):
        self.first = first
        self.second = second

    def __str__(self) -> str:
        if not self.second:
            return str(self.first)

        return f"{self.first} {self.second}"


class NotExpr(Expr):
    """
    A class to represent a NOT expression.

    Attributes
    ----------
    first : Expr
        The first part of the NOT expression.
    """

    def __init__(self, first: Expr):
        self.first = first

    def __str__(self) -> str:
        return f"!{self.first}"


class ParenExpr(Expr):
    """
    A class to represent a parenthesized expression.

    Attributes
    ----------
    first : Expr
        The first part of the parenthesized expression.
    """

    def __init__(self, first: Expr):
        self.first = first

    def __str__(self) -> str:
        return f"({self.first})"
