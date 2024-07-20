"""
    Abstract Syntax Tree (AST) for boolean expressions.
"""

from typing import TypeVar, Optional
from parser.visitor import Visitor, ParamVisitor, RetVisitor, RetParamVisitor

T = TypeVar("T")
R = TypeVar("R")


class Node:
    """
    An interface class to represent a node in the AST.
    """

    pass


# =============================================================================


class Expr(Node):
    """
    An interface class to represent a full expression.
    """

    pass


class ExprPrime(Node):
    """
    An interface class to represent an expr prime expression. Used to eliminate left-recursion.
    """

    pass


class Term(Node):
    """
    An interface class to represent a term. Used to add precedence to the grammar.
    """

    pass


class Var(Term):
    """
    An interface class to represent a var. Used for constants and variables.
    """


# =============================================================================


class TermExpr(Expr):
    """
    A class to represent an expression containing only a Term node.

    Attributes
    ----------
    first : Term
        The variable contained by the TermExpr.

    second : Optional[ExprPrime]
    """

    def __init__(self, first: Term, second: Optional[ExprPrime] = None):
        self.first = first
        self.second = second

    def __str__(self) -> str:
        if self.second is not None:
            return f"{self.first} {self.second}"

        return str(self.first)

    def accept(self, v: Visitor) -> None:
        v.visitTermExpr(self)

    def acceptParam(self, v: ParamVisitor[T], param: T) -> None:
        v.visitTermExpr(self, param)

    def acceptRet(self, v: RetVisitor[R]) -> R:
        return v.visitTermExpr(self)

    def acceptParamRet(self, v: RetParamVisitor[T, R], param: T) -> R:
        return v.visitTermExpr(self, param)


# =============================================================================


class OrExpr(ExprPrime):
    """
    A class to represent an OR expression.

    Attributes
    ----------
    first : Term
        The first part of the OR expression.

    second : Optional[ExprPrime]
        The second (or following) part of the OR expression.
    """

    def __init__(self, first: Term, second: Optional[ExprPrime] = None):
        self.first = first
        self.second = second

    def __str__(self) -> str:
        if self.second is not None:
            return f"| {self.first} {self.second}"

        return f"| {self.first}"

    def accept(self, v: Visitor) -> None:
        v.visitOrExpr(self)

    def acceptParam(self, v: ParamVisitor[T], param: T) -> None:
        v.visitOrExpr(self, param)

    def acceptRet(self, v: RetVisitor[R]) -> R:
        return v.visitOrExpr(self)

    def acceptParamRet(self, v: RetParamVisitor[T, R], param: T) -> R:
        return v.visitOrExpr(self, param)


class AndExpr(ExprPrime):
    """
    A class to represent an AND expression.

    Attributes
    ----------
    first : Term
        The first part of the AND expression.

    second : Optional[ExprPrime]
        The second (or following) part of the AND expression.
    """

    def __init__(self, first: Term, second: Optional[ExprPrime] = None):
        self.first = first
        self.second = second

    def __str__(self) -> str:
        if self.second is not None:
            return f"& {self.first} {self.second}"

        return f"& {self.first}"

    def accept(self, v: Visitor) -> None:
        v.visitAndExpr(self)

    def acceptParam(self, v: ParamVisitor[T], param: T) -> None:
        v.visitAndExpr(self, param)

    def acceptRet(self, v: RetVisitor[R]) -> R:
        return v.visitAndExpr(self)

    def acceptParamRet(self, v: RetParamVisitor[T, R], param: T) -> R:
        return v.visitAndExpr(self, param)


class XorExpr(ExprPrime):
    """
    A class to represent an XOR expression.

    Attributes
    ----------
    first : Term
        The first part of the XOR expression.

    second : Optional[ExprPrime]
        The second (or following) part of the XOR expression.
    """

    def __init__(self, first: Term, second: Optional[ExprPrime] = None):
        self.first = first
        self.second = second

    def __str__(self) -> str:
        if self.second is not None:
            return f"^ {self.first} {self.second}"

        return f"^ {self.first}"

    def accept(self, v: Visitor) -> None:
        v.visitXorExpr(self)

    def acceptParam(self, v: ParamVisitor[T], param: T) -> None:
        v.visitXorExpr(self, param)

    def acceptRet(self, v: RetVisitor[R]) -> R:
        return v.visitXorExpr(self)

    def acceptParamRet(self, v: RetParamVisitor[T, R], param: T) -> R:
        return v.visitXorExpr(self, param)


# =============================================================================


class ParenTerm(Term):
    """
    A class to represent a parenthesized term.

    Attributes
    ----------
    first : Expr
        The first part of the parenthesized term.
    """

    def __init__(self, first: Expr):
        self.first = first

    def __str__(self) -> str:
        return f"({self.first})"

    def accept(self, v: Visitor) -> None:
        v.visitParenTerm(self)

    def acceptParam(self, v: ParamVisitor[T], param: T) -> None:
        v.visitParenTerm(self, param)

    def acceptRet(self, v: RetVisitor[R]) -> R:
        return v.visitParenTerm(self)

    def acceptParamRet(self, v: RetParamVisitor[T, R], param: T) -> R:
        return v.visitParenTerm(self, param)


class NotTerm(Term):
    """
    A class to represent a NOT term.

    Attributes
    ----------
    first : Term
        The first part of the NOT term.
    """

    def __init__(self, first: Term):
        self.first = first

    def __str__(self) -> str:
        return f"!{self.first}"

    def accept(self, v: Visitor) -> None:
        v.visitNotTerm(self)

    def acceptParam(self, v: ParamVisitor[T], param: T) -> None:
        v.visitNotTerm(self, param)

    def acceptRet(self, v: RetVisitor[R]) -> R:
        return v.visitNotTerm(self)

    def acceptParamRet(self, v: RetParamVisitor[T, R], param: T) -> R:
        return v.visitNotTerm(self, param)


# =============================================================================


class VarVar(Term):
    """
    A class to represent a variable from A-Z.

    Attributes
    ----------
    name : str
        The name of the variable.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def accept(self, v: Visitor) -> None:
        v.visitVarVar(self)

    def acceptParam(self, v: ParamVisitor[T], param: T) -> None:
        v.visitVarVar(self, param)

    def acceptRet(self, v: RetVisitor[R]) -> R:
        return v.visitVarVar(self)

    def acceptParamRet(self, v: RetParamVisitor[T, R], param: T) -> R:
        return v.visitVarVar(self, param)


class TrueConst(Var):
    """
    Represents the constant TRUE
    """

    def __str__(self) -> str:
        return "t"

    def accept(self, v: Visitor) -> None:
        v.visitTrueConst(self)

    def acceptParam(self, v: ParamVisitor[T], param: T) -> None:
        v.visitTrueConst(self, param)

    def acceptRet(self, v: RetVisitor[R]) -> R:
        return v.visitTrueConst(self)

    def acceptParamRet(self, v: RetParamVisitor[T, R], param: T) -> R:
        return v.visitTrueConst(self, param)


class FalseConst(Var):
    """
    Represents the constant FALSE.
    """

    def __str__(self) -> str:
        return "f"

    def accept(self, v: Visitor) -> None:
        v.visitFalseConst(self)

    def acceptParam(self, v: ParamVisitor[T], param: T) -> None:
        v.visitFalseConst(self, param)

    def acceptRet(self, v: RetVisitor[R]) -> R:
        return v.visitFalseConst(self)

    def acceptParamRet(self, v: RetParamVisitor[T, R], param: T) -> R:
        return v.visitFalseConst(self, param)
