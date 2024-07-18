from parser.ast import Var, Expr, VarExpr, NotExpr, ParenExpr, AndExpr, OrExpr
from parser.visitor import Visitor, RetVisitor
from abc import abstractmethod
from typing import TypeVar

from sympy import Symbol, And, Or, Not


def run_pass(ast: Expr) -> Expr:
    # Sympy visitor for mapping variable
    v: SympyMappingVisitor = SympyMappingVisitor()
    ast.accept(v)

    symbolMap = v.getSymbolMap()

    tv: TranslateToSympy = TranslateToSympy(symbolMap)

    return ast.acceptRet(tv)


class SympyMappingVisitor(Visitor):
    """
    A visitor that visits each node in the AST.
    """

    def __init__(self):
        self.symbolMap: dict[str, Symbol] = {}

    def visitVar(self, var: "Var") -> None:
        self.symbolMap[str(var)] = Symbol(str(var))

    def getSymbolMap(self) -> dict[str, Symbol]:
        return self.symbolMap


R = TypeVar("R")


class TranslateToSympy(RetVisitor):
    """
    A visitor that visits each node in the AST and
    returns a value.
    """

    def __init__(self, symbolMap: dict[str, Symbol]):
        self.symbolMap = symbolMap

    def visitVarExpr(self, vex: "VarExpr") -> R:
        print(vex)

        if not vex.second:
            return vex.first.acceptRet(self)

        elif isinstance(vex.second, AndExpr):
            return And(vex.first.acceptRet(self), vex.second.acceptRet(self))

        elif isinstance(vex.second, OrExpr):
            return Or(vex.first.acceptRet(self), vex.second.acceptRet(self))

    def visitNotExpr(self, nex: "NotExpr") -> R:
        return nex.first.acceptRet(self)

    def visitParenExpr(self, pex: "ParenExpr") -> R:
        pass

    def visitAndExpr(self, aex: "AndExpr") -> R:
        if isinstance(aex.first, VarExpr):
            return aex.first.acceptRet(self)

        elif isinstance(aex.first, NotExpr):
            return Not(aex.first.acceptRet(self))

        # add parenExpr case

    def visitOrExpr(self, oex: "OrExpr") -> R:
        if isinstance(oex.first, VarExpr):
            return oex.first.acceptRet(self)

        elif isinstance(oex.first, NotExpr):
            return Not(oex.first.acceptRet(self))

        # add parenExpr case

    def visitVar(self, var: "Var") -> R:
        varSymbol = self.symbolMap[var.name]
        return varSymbol
