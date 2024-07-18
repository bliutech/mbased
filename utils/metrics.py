from typing import override

from parser.ast import VarExpr, NotExpr, ParenExpr, AndExpr, OrExpr
from parser.visitor import Visitor


class OpCounter(Visitor):

    _count = 0

    def __init__(self):
        self._count: int = 0

    @override
    def visitVarExpr(self, vex: VarExpr) -> None:
        vex.first.accept(self)
        if vex.second:
            vex.second.accept(self)

    @override
    def visitNotExpr(self, nex: NotExpr) -> None:
        self.updateCount()
        nex.first.accept(self)

    @override
    def visitParenExpr(self, pex: ParenExpr) -> None:
        pex.first.accept(self)

    @override
    def visitAndExpr(self, aex: AndExpr) -> None:
        self.updateCount()
        aex.first.accept(self)

    @override
    def visitOrExpr(self, oex: OrExpr) -> None:
        self.updateCount()
        oex.first.accept(self)

    @override
    def visitVar(self, _) -> None:
        pass

    def updateCount(self) -> None:
        self._count += 1

    def getCount(self) -> None:
        return self._count
