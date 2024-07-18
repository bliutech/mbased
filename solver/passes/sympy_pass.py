from parser.ast import Var, Expr, VarExpr, NotExpr, ParenExpr, AndExpr, OrExpr
from parser.visitor import Visitor

import sympy


def run_pass(ast: Expr) -> Expr:
    # Sympy visitor for mapping variable
    v: SympyMappingVisitor = SympyMappingVisitor()
    ast.accept(v)

    symbolMap = v.getSymbolMap()

    return ast


class SympyMappingVisitor(Visitor):
    """
    A visitor that visits each node in the AST.
    """

    def __init__(self):
        self.map: dict[str, sympy.Symbol] = {}

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

    def visitVar(self, var: "Var") -> None:
        self.map[str(var)] = sympy.Symbol(str(var))

    def getSymbolMap(self) -> dict[str, sympy.Symbol]:
        return self.map
