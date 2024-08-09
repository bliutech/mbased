"""
Apply mixed-boolean arithmetic (MBA) obfuscation to a given boolean expression.

MBAObfucator takes an approach of apply transformation to the given boolean expression
based on the abstract syntax tree (AST) of the expression. The transformation is applied
based on a few rules which are taken from the Obfuscator LLVM project. The rules are shown
at https://github.com/obfuscator-llvm/obfuscator/wiki/Instructions-Substitution
"""

from typing_extensions import override

from mbased.parser.visitor import RetVisitor

from mbased.parser.ast import (
    Node,
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


class MBAObfuscator(RetVisitor[Node]):
    def obfuscate(self, ast: Expr, n: int = 1):
        """
        Obfuscates the given AST.

        :param ast: The AST to obfuscate.
        :return: The obfuscated AST.
        """
        for _ in range(n):
            ast = ast.acceptRet(self)

        return ast

    @override
    def visitTermExpr(self, node: TermExpr) -> Node:
        first: Node = node.first.acceptRet(self)
        if node.second:
            second: Node = node.second.first.acceptRet(self)
            if isinstance(node.second, OrExpr):
                # a = b | c => a = (b & c) | (b ^ c)
                return TermExpr(
                    ParenTerm(TermExpr(first, AndExpr(second))),
                    OrExpr(ParenTerm(TermExpr(first, XorExpr(second)))),
                )
            elif isinstance(node.second, AndExpr):
                # a = b & c => a = (b ^ ~c) & b
                return TermExpr(
                    ParenTerm(TermExpr(first, XorExpr(NotTerm(second)))), AndExpr(first)
                )
            elif isinstance(node.second, XorExpr):
                # a = a ^ b => a = (~a & b) | (a & ~b)
                return TermExpr(
                    ParenTerm(TermExpr(NotTerm(first), AndExpr(second))),
                    OrExpr(ParenTerm(TermExpr(first, AndExpr(NotTerm(second))))),
                )
        return TermExpr(first)

    @override
    def visitOrExpr(self, node: OrExpr) -> Node:
        first: Node = node.first.acceptRet(self)
        second: Node = node.second.acceptRet(self)
        return OrExpr(first, second)

    @override
    def visitAndExpr(self, node: AndExpr) -> Node:
        first: Node = node.first.acceptRet(self)
        second: Node = node.second.acceptRet(self)
        return AndExpr(first, second)

    @override
    def visitXorExpr(self, node: XorExpr) -> Node:
        first: Node = node.first.acceptRet(self)
        second: Node = node.second.acceptRet(self)
        return XorExpr(first, second)

    @override
    def visitParenTerm(self, node: ParenTerm) -> Node:
        return ParenTerm(node.first.acceptRet(self))

    @override
    def visitNotTerm(self, node: NotTerm) -> Node:
        return NotTerm(node.first.acceptRet(self))

    @override
    def visitVarVar(self, node: VarVar) -> Node:
        return VarVar(node.name)

    @override
    def visitTrueConst(self, node: TrueConst) -> Node:
        return TrueConst()

    @override
    def visitFalseConst(self, node: FalseConst) -> Node:
        return FalseConst()
