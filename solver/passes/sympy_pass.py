from typing import override

from parser.ast import (
    Expr,
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
from parser.visitor import Visitor, RetVisitor
from parser.parse import Parser
from parser.lex import Lexer

import sympy
from sympy.logic.boolalg import Or, And, Xor, Not


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
    A visitor that visits each node in the AST and adds Var nodes to the symbols.
    """

    def __init__(self) -> None:
        self.symbols: dict[str, sympy.Symbol] = {}

    @override
    def visitVarVar(self, node: VarVar) -> None:
        self.symbols[node.name] = sympy.Symbol(node.name)


class TranslateToSympy(RetVisitor[sympy.Basic]):
    """
    A visitor that visits each node in the AST and
    returns an expression translated to Sympy logic.
    """

    def __init__(self, symbols: dict[str, sympy.Symbol]) -> None:
        self.symbols = symbols

    @override
    def visitTermExpr(self, node: TermExpr) -> sympy.Basic:
        first: sympy.Basic = node.first.acceptRet(self)
        if node.second:
            second: sympy.Basic = node.second.acceptRet(self)
            if isinstance(node.second, OrExpr):
                return Or(first, second)
            elif isinstance(node.second, AndExpr):
                return And(first, second)
            elif isinstance(node.second, XorExpr):
                return Xor(first, second)
        return first

    @override
    def visitOrExpr(self, node: OrExpr) -> sympy.Basic:
        first: sympy.Basic = node.first.acceptRet(self)
        if node.second:
            second: sympy.Basic = node.second.acceptRet(self)
            if isinstance(node.second, OrExpr):
                return Or(first, second)
            elif isinstance(node.second, AndExpr):
                return And(first, second)
            elif isinstance(node.second, XorExpr):
                return Xor(first, second)
        return first

    @override
    def visitAndExpr(self, node: AndExpr) -> sympy.Basic:
        first: sympy.Basic = node.first.acceptRet(self)
        if node.second:
            second: sympy.Basic = node.second.acceptRet(self)
            if isinstance(node.second, OrExpr):
                return Or(first, second)
            elif isinstance(node.second, AndExpr):
                return And(first, second)
            elif isinstance(node.second, XorExpr):
                return Xor(first, second)
        return first

    @override
    def visitXorExpr(self, node: XorExpr) -> sympy.Basic:
        first: sympy.Basic = node.first.acceptRet(self)
        if node.second:
            second: sympy.Basic = node.second.acceptRet(self)
            if isinstance(node.second, OrExpr):
                return Or(first, second)
            elif isinstance(node.second, AndExpr):
                return And(first, second)
            elif isinstance(node.second, XorExpr):
                return Xor(first, second)
        return first

    @override
    def visitParenTerm(self, node: ParenTerm) -> sympy.Basic:
        return node.first.acceptRet(self)

    @override
    def visitNotTerm(self, node: NotTerm) -> sympy.Basic:
        return Not(node.first.acceptRet(self))

    @override
    def visitVarVar(self, node: VarVar) -> sympy.Basic:
        return self.symbols[node.name]

    @override
    def visitTrueConst(self, node: TrueConst) -> sympy.Basic:
        return sympy.true

    @override
    def visitFalseConst(self, node: FalseConst) -> sympy.Basic:
        return sympy.false


if __name__ == "__main__":
    prog = "B & A | !A"
    l: Lexer = Lexer()
    l.lex(prog)

    p: Parser = Parser()
    ast: Expr = p.parse(l.tokens)

    simplified_ast: Expr = run_pass(ast)

    assert str(simplified_ast) == "B"
