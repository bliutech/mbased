from parser import ast


class Visitor:

    def visitNotExpr(self, vex: VarExpr):
        vex.accept(self)

    def visitVarExpr(self, exp: ExprPrime, va: Var):
        exp.accept(self)
        va.accept(self)

    def visitVar():
        return

    def visitExprPrime():
        return

    def visitExpr():
        return

    def visitAndExpr(self, aex: AndExpr):
        return

    def visitOrExpr(self, oex: OrExpr):
        return

    def visitParenExpr(self, pex: ParenExpr):
        return
