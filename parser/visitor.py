from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parser.ast import VarExpr, NotExpr, ParenExpr, AndExpr, OrExpr


class Visitor:
    def visitVarExpr(self, vex: "VarExpr") -> None:
        vex.first.accept(self)

    def visitNotExpr(self, nex: "NotExpr") -> None:
        nex.first.accept(self)

    def visitParenExpr(self, pex: "ParenExpr") -> None:
        pex.first.accept(self)

    def visitAndExpr(self, aex: "AndExpr") -> None:
        aex.first.accept(self)

    def visitOrExpr(self, oex: "OrExpr") -> None:
        oex.first.accept(self)

    def visitVar(self, _) -> None:
        pass
