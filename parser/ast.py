"""
    Abstract Syntax Tree (AST) for boolean expressions.
"""

from typing import TypeVar
from parser.visitor import Visitor, ParamVisitor, RetVisitor, RetParamVisitor

T = TypeVar("T")
R = TypeVar("R")


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

    def accept(self, v: Visitor) -> None:
        v.visitVar(self)

    def acceptParam(self, v: ParamVisitor, param: T) -> None:
        v.visitVar(self, param)

    def acceptRet(self, v: RetVisitor) -> R:
        return v.visitVar(self)

    def acceptParamRet(self, v: RetParamVisitor, param: T) -> R:
        return v.visitVar(self, param)


class Node:
    """
    An interface class to represent a node in the AST.
    """

    pass


class Expr(Node):
    """
    An interface class to represent a full expression.
    """

    pass


class ExprPrime(Node):
    """
    An interface class to represent a prime expression. Used to eliminate left-recursion.
    """

    pass


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

    def accept(self, v: Visitor) -> None:
        v.visitAndExpr(self)

    def acceptParam(self, v: ParamVisitor, param: T) -> None:
        v.visitAndExpr(self, param)

    def acceptRet(self, v: RetVisitor) -> R:
        return v.visitAndExpr(self)

    def acceptParamRet(self, v: RetParamVisitor, param: T) -> R:
        return v.visitAndExpr(self, param)


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

    def accept(self, v: Visitor) -> None:
        v.visitOrExpr(self)

    def acceptParam(self, v: ParamVisitor, param: T) -> None:
        v.visitOrExpr(self, param)

    def acceptRet(self, v: RetVisitor) -> R:
        return v.visitOrExpr(self)

    def acceptParamRet(self, v: RetParamVisitor, param: T) -> R:
        return v.visitOrExpr(self, param)


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

    def accept(self, v: Visitor) -> None:
        v.visitVarExpr(self)

    def acceptParam(self, v: ParamVisitor, param: T) -> None:
        v.visitVarExpr(self, param)

    def acceptRet(self, v: RetVisitor) -> R:
        return v.visitVarExpr(self)

    def acceptParamRet(self, v: RetParamVisitor, param: T) -> R:
        return v.visitVarExpr(self, param)


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

    def accept(self, v: Visitor) -> None:
        v.visitNotExpr(self)

    def acceptParam(self, v: ParamVisitor, param: T) -> None:
        v.visitNotExpr(self, param)

    def acceptRet(self, v: RetVisitor) -> R:
        return v.visitNotExpr(self)

    def acceptParamRet(self, v: RetParamVisitor, param: T) -> R:
        return v.visitNotExpr(self, param)


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

    def accept(self, v: Visitor) -> None:
        v.visitParenExpr(self)

    def acceptParam(self, v: ParamVisitor, param: T) -> None:
        v.visitParenExpr(self, param)

    def acceptRet(self, v: RetVisitor) -> R:
        return v.visitParenExpr(self)

    def acceptParamRet(self, v: RetParamVisitor, param: T) -> R:
        return v.visitParenExpr(self, param)
