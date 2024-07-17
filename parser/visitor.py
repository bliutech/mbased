from typing import TYPE_CHECKING, TypeVar, Generic
from abc import abstractmethod

if TYPE_CHECKING:
    from parser.ast import VarExpr, NotExpr, ParenExpr, AndExpr, OrExpr


class Visitor:
    """
    A visitor that visits each node in the AST.
    """

    def visitVarExpr(self, vex: "VarExpr") -> None:
        vex.first.accept(self)
        if vex.second:
            vex.second.accept(self)

    def visitNotExpr(self, nex: "NotExpr") -> None:
        nex.first.accept(self)

    def visitParenExpr(self, pex: "ParenExpr") -> None:
        pex.first.accept(self)

    def visitAndExpr(self, aex: "AndExpr") -> None:
        aex.first.accept(self)

    def visitOrExpr(self, oex: "OrExpr") -> None:
        oex.first.accept(self)

    def visitVar(self, _) -> None:
        pass


T = TypeVar("T")


class ParamVisitor(Generic[T]):
    """
    A visitor that visits each node in the AST and
    passes a parameter.
    """

    def visitVarExpr(self, vex: "VarExpr", param: T) -> None:
        vex.first.accept(self, param)
        if vex.second:
            vex.second.accept(self, param)

    def visitNotExpr(self, nex: "NotExpr", param: T) -> None:
        nex.first.accept(self, param)

    def visitParenExpr(self, pex: "ParenExpr", param: T) -> None:
        pex.first.accept(self, param)

    def visitAndExpr(self, aex: "AndExpr", param: T) -> None:
        aex.first.accept(self, param)

    def visitOrExpr(self, oex: "OrExpr", param: T) -> None:
        oex.first.accept(self, param)

    def visitVar(self, _, param: T) -> None:
        pass


R = TypeVar("R")


class RetVisitor(Generic[R]):
    """
    A visitor that visits each node in the AST and
    returns a value.
    """

    @abstractmethod
    def visitVarExpr(self, vex: "VarExpr") -> R:
        pass

    @abstractmethod
    def visitNotExpr(self, nex: "NotExpr") -> R:
        pass

    @abstractmethod
    def visitParenExpr(self, pex: "ParenExpr") -> R:
        pass

    @abstractmethod
    def visitAndExpr(self, aex: "AndExpr") -> R:
        pass

    @abstractmethod
    def visitOrExpr(self, oex: "OrExpr") -> R:
        pass

    @abstractmethod
    def visitVar(self, _) -> R:
        pass


class RetParamVisitor(Generic[R, T]):
    """
    A visitor that visits each node in the AST and
    returns a value and passes a parameter.
    """

    @abstractmethod
    def visitVarExpr(self, vex: "VarExpr", param: T) -> R:
        pass

    @abstractmethod
    def visitNotExpr(self, nex: "NotExpr", param: T) -> R:
        pass

    @abstractmethod
    def visitParenExpr(self, pex: "ParenExpr", param: T) -> R:
        pass

    @abstractmethod
    def visitAndExpr(self, aex: "AndExpr", param: T) -> R:
        pass

    @abstractmethod
    def visitOrExpr(self, oex: "OrExpr", param: T) -> R:
        pass

    @abstractmethod
    def visitVar(self, _, param: T) -> R:
        pass
