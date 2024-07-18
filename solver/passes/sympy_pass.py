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
from parser.parse import Parser
from parser.lex import Lexer
from typing import override

from sympy import Symbol, And, Or, Not, simplify_logic, Expr as SympyExpr


def run_pass(ast: Expr) -> Expr:
    # Sympy visitor for mapping variable
    v: SympyMappingVisitor = SympyMappingVisitor()
    ast.accept(v)

    symbolMap: dict[dict, Symbol] = v.getSymbolMap()

    tv: TranslateToSympy = TranslateToSympy(symbolMap)

    unsimplified: str = str(ast.acceptRet(tv))
    simplified: str = str(simplify_logic(unsimplified))

    parser: Parser = Parser()
    lexer: Lexer = Lexer()

    lexer.lex(simplified.replace("~", "!"))
    tokens: list[str] = lexer.getTokens()

    simplifiedAST: Expr = parser.parse(tokens)

    return simplifiedAST


class SympyMappingVisitor(Visitor):
    """
    A visitor that visits each node in the AST and adds Var nodes to the symbolMap.
    """

    def __init__(self):
        self.symbolMap: dict[str, Symbol] = {}

    def visitVar(self, var: "Var") -> None:
        self.symbolMap[str(var)] = Symbol(str(var))

    def getSymbolMap(self) -> dict[str, Symbol]:
        return self.symbolMap


class TranslateToSympy(RetVisitor[SympyExpr]):
    """
    A visitor that visits each node in the AST and
    returns an expression translated to Sympy logic.
    """

    @override
    def __init__(self, symbolMap: dict[str, Symbol]):
        self.symbolMap = symbolMap

    @override
    def visitVarExpr(self, vex: "VarExpr") -> SympyExpr:
        if not vex.second:
            return vex.first.acceptRet(self)

        return vex.second.acceptParamRet(self, vex.first)

    @override
    def visitNotExpr(self, nex: "NotExpr") -> SympyExpr:
        return Not(nex.first.acceptRet(self))

    @override
    def visitParenExpr(self, pex: "ParenExpr") -> SympyExpr:
        return pex.first.acceptRet(self)

    @override
    def visitAndExpr(self, aex: "AndExpr", leftOperand: "Expr") -> SympyExpr:
        return And(leftOperand.acceptRet(self), aex.first.acceptRet(self))

    @override
    def visitOrExpr(self, oex: "OrExpr", leftOperand: "Expr") -> SympyExpr:
        return Or(leftOperand.acceptRet(self), oex.first.acceptRet(self))

    @override
    def visitVar(self, var: "Var") -> SympyExpr:
        varSymbol = self.symbolMap[var.name]
        return varSymbol
