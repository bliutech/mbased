from parser.ast import (
    Var,
    Expr,
    ExprPrime,
    VarExpr,
    NotExpr,
    ParenExpr,
    AndExpr,
    OrExpr,
)
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
        if not vex.second:
            return vex.first.acceptRet(self)

        return vex.second.acceptParamRet(self, vex.first)

    def visitNotExpr(self, nex: "NotExpr") -> R:
        return Not(nex.first.acceptRet(self))

    def visitParenExpr(self, pex: "ParenExpr") -> R:
        pass

    def visitAndExpr(self, aex: "AndExpr", leftOperand: "Expr") -> R:
        return And(leftOperand.acceptRet(self), aex.first.acceptRet(self))

    def visitOrExpr(self, oex: "OrExpr", leftOperand: "Expr") -> R:
        return Or(leftOperand.acceptRet(self), oex.first.acceptRet(self))

    def visitVar(self, var: "Var") -> R:
        varSymbol = self.symbolMap[var.name]
        return varSymbol
