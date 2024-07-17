from parser.ast import *


class Visitor:
    def visitVarExpr(self, vex: VarExpr):
        vex.first.accept(self)

    def visitNotExpr(self, nex: NotExpr):
        nex.first.accept(self)

    def visitParenExpr(self, pex: ParenExpr):
        pex.first.accept(self)

    def visitAndExpr(self, aex: AndExpr):
        aex.first.accept(self)

    def visitOrExpr(self, oex: OrExpr):
        oex.first.accept(self)

    def visitVar():
        pass
