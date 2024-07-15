import unittest
from parser.lexer import Lexer


class TestLexer(unittest.TestCase):
    def test_lex(self):
        prog: str = "(A & B) | !C"
        tokens: list[str] = Lexer.lex(prog)
        self.assertEqual(tokens, ["(", "A", "&", "B", ")", "|", "!", "C"])

        prog = "A|B"
        tokens = Lexer.lex(prog)
        self.assertEqual(tokens, ["A", "|", "B"])

        prog = "!(A & C)"
        tokens = Lexer.lex(prog)
        self.assertEqual(tokens, ["!", "(", "A", "&", "C", ")"])
