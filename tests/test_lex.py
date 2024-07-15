import unittest
from parser.lexer import Lexer


class TestLexer(unittest.TestCase):
    def test_lex(self):
        prog: str = "(A & B) | !C"
        l: Lexer = Lexer()
        l.lex(prog)
        self.assertEqual(
            l.getTokens(), ["(", "A", "&", "B", ")", "|", "!", "C", "EOF"]
        )

        prog = "A|B"
        l.lex(prog)
        self.assertEqual(l.getTokens(), ["A", "|", "B", "EOF"])

        prog = "!(A & C)"
        l.lex(prog)
        self.assertEqual(l.getTokens(), ["!", "(", "A", "&", "C", ")", "EOF"])
