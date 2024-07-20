from typing import TYPE_CHECKING, TypeVar, Generic
from abc import abstractmethod

if TYPE_CHECKING:
    from parser.ast import (
        TermExpr,
        OrExpr,
        AndExpr,
        XorExpr,
        ParenTerm,
        NotTerm,
        VarVar,
        TrueConst,
        FalseConst,
    )

R = TypeVar("R")
T = TypeVar("T")


class Visitor:
    """
    A visitor that visits each node in the AST.
    """

    def visitTermExpr(self, node: "TermExpr") -> None:
        node.first.accept(self)
        if node.second:
            node.second.accept(self)

    def visitOrExpr(self, node: "OrExpr") -> None:
        node.first.accept(self)
        if node.second:
            node.second.accept(self)

    def visitAndExpr(self, node: "AndExpr") -> None:
        node.first.accept(self)
        if node.second:
            node.second.accept(self)

    def visitXorExpr(self, node: "XorExpr") -> None:
        node.first.accept(self)
        if node.second:
            node.second.accept(self)

    def visitParenTerm(self, node: "ParenTerm") -> None:
        node.first.accept(self)

    def visitNotTerm(self, node: "NotTerm") -> None:
        node.first.accept(self)

    def visitVarVar(self, node: "VarVar") -> None:
        pass

    def visitTrueConst(self, node: "TrueConst") -> None:
        pass

    def visitFalseConst(self, node: "FalseConst") -> None:
        pass


class ParamVisitor(Generic[T]):
    """
    A visitor that visits each node in the AST and
    passes a parameter.
    """

    def visitTermExpr(self, node: "TermExpr", param: T) -> None:
        node.first.accept(self, param)
        if node.second:
            node.second.accept(self, param)

    def visitOrExpr(self, node: "OrExpr", param: T) -> None:
        node.first.accept(self, param)
        if node.second:
            node.second.accept(self, param)

    def visitAndExpr(self, node: "AndExpr", param: T) -> None:
        node.first.accept(self, param)
        if node.second:
            node.second.accept(self, param)

    def visitXorExpr(self, node: "XorExpr", param: T) -> None:
        node.first.accept(self, param)
        if node.second:
            node.second.accept(self, param)

    def visitParenTerm(self, node: "ParenTerm", param: T) -> None:
        node.first.accept(self, param)

    def visitNotTerm(self, node: "NotTerm", param: T) -> None:
        node.first.accept(self, param)

    def visitVarVar(self, node: "VarVar", param: T) -> None:
        pass

    def visitTrueConst(self, node: "TrueConst", param: T) -> None:
        pass

    def visitFalseConst(self, node: "FalseConst", param: T) -> None:
        pass


class RetVisitor(Generic[R]):
    """
    A visitor that visits each node in the AST and
    returns a value.
    """

    @abstractmethod
    def visitTermExpr(self, node: "TermExpr") -> R:
        pass

    @abstractmethod
    def visitOrExpr(self, node: "OrExpr") -> R:
        pass

    @abstractmethod
    def visitAndExpr(self, node: "AndExpr") -> R:
        pass

    @abstractmethod
    def visitXorExpr(self, node: "XorExpr") -> R:
        pass

    @abstractmethod
    def visitParenTerm(self, node: "ParenTerm") -> R:
        pass

    @abstractmethod
    def visitNotTerm(self, node: "NotTerm") -> R:
        pass

    @abstractmethod
    def visitVarVar(self, node: "VarVar") -> R:
        pass

    @abstractmethod
    def visitTrueConst(self, node: "TrueConst") -> R:
        pass

    @abstractmethod
    def visitFalseConst(self, node: "FalseConst") -> R:
        pass


class RetParamVisitor(Generic[T, R]):
    """
    A visitor that visits each node in the AST and
    returns a value and passes a parameter.
    """

    @abstractmethod
    def visitTermExpr(self, node: "TermExpr", param: T) -> R:
        pass

    @abstractmethod
    def visitOrExpr(self, node: "OrExpr", param: T) -> R:
        pass

    @abstractmethod
    def visitAndExpr(self, node: "AndExpr", param: T) -> R:
        pass

    @abstractmethod
    def visitXorExpr(self, node: "XorExpr", param: T) -> R:
        pass

    @abstractmethod
    def visitParenTerm(self, node: "ParenTerm", param: T) -> R:
        pass

    @abstractmethod
    def visitNotTerm(self, node: "NotTerm", param: T) -> R:
        pass

    @abstractmethod
    def visitVarVar(self, node: "VarVar", param: T) -> R:
        pass

    @abstractmethod
    def visitTrueConst(self, node: "TrueConst", param: T) -> R:
        pass

    @abstractmethod
    def visitFalseConst(self, node: "FalseConst", param: T) -> R:
        pass
