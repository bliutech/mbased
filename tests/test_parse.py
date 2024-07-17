from unittest import TestCase
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

        v: Visitor = Visitor()
        tree.accept(v)
