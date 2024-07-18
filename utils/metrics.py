from typing import override

from parser.ast import VarExpr, NotExpr, ParenExpr, AndExpr, OrExpr
from parser.visitor import Visitor

class OpCounter(Visitor):

    def __init__(self) -> None:
        self._count = 0

    @override
    def visitVarExpr(self, vex: VarExpr) -> None:
        OpCounter._count += 1

    @override
    def visitNotExpr(self, nex: NotExpr) -> None:
        OpCounter._count += 1

    @override
    def visitParenExpr(self, pex: ParenExpr) -> None:
        OpCounter._count += 1

    @override
    def visitAndExpr(self, aex: AndExpr) -> None:
        OpCounter._count += 1

    @override
    def visitOrExpr(self, oex: OrExpr) -> None:
        OpCounter._count += 1

    @override
    def visitVar(self, _) -> None:
        OpCounter._count += 1

    def getCount(self) -> None:
        return self._count
