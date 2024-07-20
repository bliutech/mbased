from typing import override

from parser.ast import OrExpr, AndExpr, XorExpr, NotTerm
from parser.visitor import Visitor


class OpCounter(Visitor):
    """Counts the number of boolean operators visited"""

    def __init__(self) -> None:
        self._count: int = 0

    def getCount(self) -> int:
        return self._count

    @override
    def visitOrExpr(self, node: OrExpr) -> None:
        self._count += 1
        node.first.accept(self)
        if node.second:
            node.second.accept(self)

    @override
    def visitAndExpr(self, node: AndExpr) -> None:
        self._count += 1
        node.first.accept(self)
        if node.second:
            node.second.accept(self)

    @override
    def visitXorExpr(self, node: XorExpr) -> None:
        self._count += 1
        node.first.accept(self)
        if node.second:
            node.second.accept(self)

    @override
    def visitNotTerm(self, node: NotTerm) -> None:
        self._count += 1
        node.first.accept(self)
