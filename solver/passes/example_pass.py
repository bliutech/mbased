from typing_extensions import override

import sys

from mbased.parser.ast import AndExpr, OrExpr, Expr, NotExpr, ParenExpr, Var, VarExpr
from mbased.parser.visitor import Visitor, RetVisitor


def run_pass(ast: Expr) -> Expr:
    # Does analysis on the AST to find all symbols
    v: SymbolSetBuilder = SymbolSetBuilder()
    ast.accept(v)

    print(v.symbols, file=sys.stderr)

    # Translates the AST to a string
    t: TranslationVisitor = TranslationVisitor()
    p: str = ast.acceptRet(t)

    print(p, file=sys.stderr)

    return ast


class SymbolSetBuilder(Visitor):
    def __init__(self) -> None:
        self.symbols: set[str] = set()

    @override
    def visitVar(self, v: Var) -> None:
        self.symbols.add(v.name)


class TranslationVisitor(RetVisitor[str]):
    @override
    def visitVarExpr(self, vex: VarExpr) -> str:
        first: str = vex.first.acceptRet(self)
        if vex.second:
            return f"{first} {vex.second.acceptRet(self)}"
        else:
            return first

    @override
    def visitNotExpr(self, nex: NotExpr) -> str:
        return f"~{nex.expr.acceptRet(self)}"

    @override
    def visitParenExpr(self, pex: ParenExpr) -> str:
        return f"[{pex.expr.acceptRet(self)}]"

    @override
    def visitAndExpr(self, aex: AndExpr) -> str:
        return f"AND {aex.first.acceptRet(self)}"

    @override
    def visitOrExpr(self, oex: OrExpr) -> str:
        return f"OR {oex.first.acceptRet(self)}"

    @override
    def visitVar(self, v: Var) -> str:
        return v.name.lower()


if __name__ == "__main__":
    from parser.lex import Lexer
    from parser.parse import Parser

    prog: str = "A | B & C"
    l: Lexer = Lexer()
    l.lex(prog)

    p: Parser = Parser()
    ast: Expr = p.parse(l.tokens)

    run_pass(ast)
