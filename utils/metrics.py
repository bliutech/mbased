from typing import override

from parser.ast import VarExpr, NotExpr, ParenExpr, AndExpr, OrExpr
from parser.visitor import Visitor


class OpCounter(Visitor):
    """Counts the number of boolean operators visited"""

    _count: int = 0

    @override
    def visitNotExpr(self, nex: NotExpr) -> None:
        OpCounter._count += 1
        nex.first.accept(self)

    @override
    def visitAndExpr(self, aex: AndExpr) -> None:
        OpCounter._count += 1
        aex.first.accept(self)

    @override
    def visitOrExpr(self, oex: OrExpr) -> None:
        OpCounter._count += 1
        oex.first.accept(self)

    def getCount(self) -> int:
        return self._count
