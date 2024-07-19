from typing import override

import html, re

from parser.ast import AndExpr, OrExpr, Expr, NotExpr, ParenExpr, Var, VarExpr
from parser.visitor import Visitor, RetVisitor
from parser.lex import Lexer
from parser.parse import Parser

import z3


def run_pass(ast: Expr) -> Expr:
    v: Z3MappingVisitor = Z3MappingVisitor()
    ast.accept(v)

    t: TranslateToZ3 = TranslateToZ3(v.symbols)
    p: z3.ExprRef = ast.acceptRet(t)
    simplifiedExpr: z3.ExprRef = z3.simplify(p)

    # Quick hack to force z3 into html mode
    # so we can parse the simplified expression
    # https://ericpony.github.io/z3py-tutorial/advanced-examples.htm
    z3.set_option(html_mode=True)

    simplifiedStr: str = str(simplifiedExpr)
    simplifiedStr = (
        html.unescape(simplifiedStr)
        .replace(chr(8744), "|")
        .replace(chr(8743), "&")
        .replace(chr(172), "!")
    )
    # z3's XOR pretty print does not print cleanly so
    # this is a hack to fix that

    # Pattern to match "Xor(A, B)"
    pattern = r"Xor\(([A-Z \|&\^\(\)]+), ([A-Z \|&\^\(\)]+)\)"
    # Replacement string using backreferences to capture groups
    replacement = r"\1 ^ \2"
    # Performing the replacement. Loop to catch nested Xor calls
    while re.match(pattern, simplifiedStr):
        simplifiedStr = re.sub(pattern, replacement, simplifiedStr)

    l: Lexer = Lexer()
    l.lex(simplifiedStr)

    pa: Parser = Parser()
    ast: Expr = pa.parse(l.tokens)

    return ast


class Z3MappingVisitor(Visitor):
    def __init__(self) -> None:
        self.symbols: dict[str, z3.Bool] = {}

    @override
    def visitVar(self, va: Var):
        self.symbols[va.name] = z3.Bool(va.name)


class TranslateToZ3(RetVisitor[z3.ExprRef]):

    def __init__(self, symbols: dict[str, z3.Bool]) -> None:
        self.symbols = symbols

    @override
    def visitVarExpr(self, vex: VarExpr) -> z3.ExprRef:
        first: z3.ExprRef = vex.first.acceptRet(self)
        if vex.second:
            second: z3.ExprRef = vex.second.first.acceptRet(self)
            if isinstance(vex.second, AndExpr):
                return z3.And(first, second)
            elif isinstance(vex.second, OrExpr):
                return z3.Or(first, second)
        return first

    @override
    def visitNotExpr(self, nex: NotExpr) -> z3.ExprRef:
        return z3.Not(nex.first.acceptRet(self))

    @override
    def visitParenExpr(self, pex: ParenExpr) -> z3.ExprRef:
        return pex.first.acceptRet(self)

    @override
    def visitAndExpr(self) -> None:
        pass

    @override
    def visitOrExpr(self) -> None:
        pass

    @override
    def visitVar(self, va: Var) -> z3.ExprRef:
        return self.symbols[va.name]


if __name__ == "__main__":

    prog: str = "!(!(B | !C))"
    l: Lexer = Lexer()
    l.lex(prog)

    p: Parser = Parser()
    ast: Expr = p.parse(l.tokens)

    ast = run_pass(ast)

    assert str(ast) == "B | !C"
