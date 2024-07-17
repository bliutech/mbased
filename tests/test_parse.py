from typing import override
from unittest import TestCase

from parser.ast import NotExpr, OrExpr, ParenExpr, VarExpr, AndExpr
from parser.parse import Parser
from parser.visitor import Visitor


class TestParse(TestCase):
    def test_parse(self) -> None:
        p: Parser = Parser()
        tree = p.parse(["!", "(", "A", "&", "!", "B", "|", "C", ")", "<EOF>"])
        self.assertEqual(
            str(tree),
            "!(A & !B | C)",
        )

    def test_visitor(self) -> None:
        class CountVisitor(Visitor):
            count: int = 0

            def __init__(self):
                self.visited: list[str] = []

            @override
            def visitVarExpr(self, vex: VarExpr) -> None:
                CountVisitor.count += 1
                self.visited.append("VarExpr")
                vex.first.accept(self)
                if vex.second:
                    vex.second.accept(self)

            @override
            def visitNotExpr(self, nex: NotExpr) -> None:
                CountVisitor.count += 1
                self.visited.append("NotExpr")
                nex.first.accept(self)

            @override
            def visitParenExpr(self, pex: ParenExpr) -> None:
                CountVisitor.count += 1
                self.visited.append("ParenExpr")
                pex.first.accept(self)

            @override
            def visitAndExpr(self, aex: AndExpr) -> None:
                CountVisitor.count += 1
                self.visited.append("AndExpr")
                aex.first.accept(self)

            @override
            def visitOrExpr(self, oex: OrExpr) -> None:
                CountVisitor.count += 1
                self.visited.append("OrExpr")
                oex.first.accept(self)

            @override
            def visitVar(self, _) -> None:
                CountVisitor.count += 1
                self.visited.append("Var")

        p: Parser = Parser()
        tree = p.parse(["!", "(", "A", "&", "!", "B", "|", "C", ")", "<EOF>"])
        visitor: CountVisitor = CountVisitor()
        tree.accept(visitor)

        self.assertEqual(visitor.count, 11)
        self.assertEqual(
            visitor.visited,
            [
                "NotExpr",
                "ParenExpr",
                "VarExpr",
                "Var",
                "AndExpr",
                "NotExpr",
                "VarExpr",
                "Var",
                "OrExpr",
                "VarExpr",
                "Var",
            ],
        )
