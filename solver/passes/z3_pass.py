from typing_extensions import override

import html, re

from mbased.parser.ast import (
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
from mbased.parser.visitor import Visitor, RetVisitor
from mbased.parser.parse import Parser
from mbased.parser.lex import Lexer

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
    pattern = r"Xor\(([A-Z \|&!\^\(\)]+), ([A-Z \|&!\^\(\)]+)\)"
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
    def visitVarVar(self, node: VarVar) -> None:
        self.symbols[node.name] = z3.Bool(node.name)


class TranslateToZ3(RetVisitor[z3.ExprRef]):

    def __init__(self, symbols: dict[str, z3.Bool]) -> None:
        self.symbols: dict[str, z3.Bool] = symbols

    @override
    def visitTermExpr(self, node: TermExpr) -> z3.ExprRef:
        first: z3.ExprRef = node.first.acceptRet(self)
        if node.second:
            second: z3.ExprRef = node.second.acceptRet(self)
            if isinstance(node.second, OrExpr):
                return z3.Or(first, second)
            elif isinstance(node.second, AndExpr):
                return z3.And(first, second)
            elif isinstance(node.second, XorExpr):
                return z3.Xor(first, second)
        return first

    @override
    def visitOrExpr(self, node: OrExpr) -> z3.ExprRef:
        first: z3.ExprRef = node.first.acceptRet(self)
        if node.second:
            second: z3.ExprRef = node.second.acceptRet(self)
            if isinstance(node.second, OrExpr):
                return z3.Or(first, second)
            elif isinstance(node.second, AndExpr):
                return z3.And(first, second)
            elif isinstance(node.second, XorExpr):
                return z3.Xor(first, second)
        return first

    @override
    def visitAndExpr(self, node: AndExpr) -> z3.ExprRef:
        first: z3.ExprRef = node.first.acceptRet(self)
        if node.second:
            second: z3.ExprRef = node.second.acceptRet(self)
            if isinstance(node.second, OrExpr):
                return z3.Or(first, second)
            elif isinstance(node.second, AndExpr):
                return z3.And(first, second)
            elif isinstance(node.second, XorExpr):
                return z3.Xor(first, second)
        return first

    @override
    def visitXorExpr(self, node: XorExpr) -> z3.ExprRef:
        first: z3.ExprRef = node.first.acceptRet(self)
        if node.second:
            second: z3.ExprRef = node.second.acceptRet(self)
            if isinstance(node.second, OrExpr):
                return z3.Or(first, second)
            elif isinstance(node.second, AndExpr):
                return z3.And(first, second)
            elif isinstance(node.second, XorExpr):
                return z3.Xor(first, second)
        return first

    @override
    def visitParenTerm(self, node: ParenTerm) -> z3.ExprRef:
        return node.first.acceptRet(self)

    @override
    def visitNotTerm(self, node: NotTerm) -> z3.ExprRef:
        return z3.Not(node.first.acceptRet(self))

    @override
    def visitVarVar(self, node: VarVar) -> z3.ExprRef:
        return self.symbols[node.name]

    @override
    def visitTrueConst(self, node: TrueConst) -> z3.ExprRef:
        return z3.BoolVal(True)

    @override
    def visitFalseConst(self, node: FalseConst) -> z3.ExprRef:
        return z3.BoolVal(False)


if __name__ == "__main__":

    prog: str = "!(!(B | !C))"
    l: Lexer = Lexer()
    l.lex(prog)

    p: Parser = Parser()
    ast: Expr = p.parse(l.tokens)

    ast = run_pass(ast)

    assert str(ast) == "B | !C"
