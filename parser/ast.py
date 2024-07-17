"""
    Abstract Syntax Tree (AST) for boolean expressions.
"""

from parser.visitor import Visitor


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

    def accept(self, v: Visitor):
        v.visitVar(self)


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

    def accept(self, v: Visitor):
        v.visitAndExpr(self)


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

    def accept(self, v: Visitor):
        v.visitOrExpr(self)


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

    def accept(self, v: Visitor):
        v.visitVarExpr(self)


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

    def accept(self, v: Visitor):
        v.visitNotExpr(self)


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

    def accept(self, v: Visitor):
        v.visitParenExpr(self)
