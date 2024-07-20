import unittest
from parser.lex import Lexer


class TestLexer(unittest.TestCase):
    def test_or(self) -> None:
        prog = "A|B"
        l: Lexer = Lexer()
        l.lex(prog)
        self.assertEqual(l.getTokens(), ["A", "|", "B", "<EOF>"])

    def test_and(self) -> None:
        prog = "A & C"
        l: Lexer = Lexer()
        l.lex(prog)
        self.assertEqual(l.getTokens(), ["A", "&", "C", "<EOF>"])

    def test_xor(self) -> None:
        prog = "A ^ B"
        l: Lexer = Lexer()
        l.lex(prog)
        self.assertEqual(l.getTokens(), ["A", "^", "B", "<EOF>"])

    def test_not(self) -> None:
        prog = "! A"
        l: Lexer = Lexer()
        l.lex(prog)
        self.assertEqual(l.getTokens(), ["!", "A", "<EOF>"])

    def test_lex(self) -> None:
        prog: str = "(A & B) | !C & t ^ f"
        l: Lexer = Lexer()
        l.lex(prog)
        self.assertEqual(
            l.getTokens(),
            ["(", "A", "&", "B", ")", "|", "!", "C", "&", "t", "^", "f", "<EOF>"],
        )
