from unittest import TestCase

from parser.ast import Expr
from parser.parse import Parser


class TestParse(TestCase):
    def test_or(self) -> None:
        tokens: list[str] = ["A", "|", "B", "<EOF>"]
        p: Parser = Parser()
        ast: Expr = p.parse(tokens)
        self.assertEqual(
            str(ast),
            "A | B",
        )

    def test_and(self) -> None:
        tokens: list[str] = ["A", "&", "B", "<EOF>"]
        p: Parser = Parser()
        ast: Expr = p.parse(tokens)
        self.assertEqual(
            str(ast),
            "A & B",
        )

    def test_xor(self) -> None:
        tokens: list[str] = ["A", "^", "B", "<EOF>"]
        p: Parser = Parser()
        ast: Expr = p.parse(tokens)
        self.assertEqual(
            str(ast),
            "A ^ B",
        )

    def test_not(self) -> None:
        tokens: list[str] = ["!", "A", "<EOF>"]
        p: Parser = Parser()
        ast: Expr = p.parse(tokens)
        self.assertEqual(
            str(ast),
            "!A",
        )

    def test_parse(self) -> None:
        tokens: list[str] = [
            "!",
            "(",
            "A",
            "&",
            "!",
            "B",
            "|",
            "f",
            ")",
            "^",
            "t",
            "<EOF>",
        ]
        p: Parser = Parser()
        ast: Expr = p.parse(tokens)
        self.assertEqual(
            str(ast),
            "!(A & !B | f) ^ t",
        )
