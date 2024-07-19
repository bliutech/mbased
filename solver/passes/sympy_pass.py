from typing import override
from parser.ast import (
    Var,
    Expr,
    VarExpr,
    NotExpr,
    ParenExpr,
    AndExpr,
    OrExpr,
)
from parser.visitor import Visitor, RetVisitor
from parser.parse import Parser
from parser.lex import Lexer

import sympy
from sympy.logic.boolalg import And, Or, Not


def run_pass(ast: Expr) -> Expr:
    # Sympy visitor for mapping variable
    v: SympyMappingVisitor = SympyMappingVisitor()
    ast.accept(v)

    tv: TranslateToSympy = TranslateToSympy(v.symbols)

    p: sympy.Basic = ast.acceptRet(tv)

    simplifiedExpr: sympy.Basic = sympy.simplify_logic(p)
    simplifiedStr: str = str(simplifiedExpr)

    l: Lexer = Lexer()
    l.lex(simplifiedStr)

    pa: Parser = Parser()
    ast: Expr = pa.parse(l.tokens)

    return ast


class SympyMappingVisitor(Visitor):
    """
    A visitor that visits each node in the AST and adds Var nodes to the symbolMap.
    """

    def __init__(self) -> None:
        self.symbolMap: dict[str, sympy.Symbol] = {}

    @override
    def visitVar(self, va: Var) -> None:
        self.symbolMap[va.name] = sympy.Symbol(va.name)


class TranslateToSympy(RetVisitor[sympy.Basic]):
    """
    A visitor that visits each node in the AST and
    returns an expression translated to Sympy logic.
    """

    def __init__(self, symbols: dict[str, sympy.Symbol]) -> None:
        self.symbols = symbols

    @override
    def visitVarExpr(self, vex: VarExpr) -> sympy.Basic:
        first: sympy.Basic = vex.first.acceptRet(self)
        if vex.second:
            second: sympy.Basic = vex.second.first.acceptRet(self)
            if isinstance(vex.second, AndExpr):
                return And(first, second)
            elif isinstance(vex.second, OrExpr):
                return Or(first, second)
        return first

    @override
    def visitNotExpr(self, nex: NotExpr) -> sympy.Basic:
        return Not(nex.first.acceptRet(self))

    @override
    def visitParenExpr(self, pex: ParenExpr) -> sympy.Basic:
        return pex.first.acceptRet(self)

    @override
    def visitAndExpr(self, aex: AndExpr) -> sympy.Basic:
        pass

    @override
    def visitOrExpr(self, oex: OrExpr) -> sympy.Basic:
        pass

    @override
    def visitVar(self, va: Var) -> sympy.Basic:
        return self.symbols[va.name]


if __name__ == "__main__":
    prog = "B & A | !A"
    l: Lexer = Lexer()
    l.lex(prog)

    p: Parser = Parser()
    ast: Expr = p.parse(l.tokens)

    run_pass(ast)
