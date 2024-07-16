import unittest
from parser.lexer import Lexer


class TestLexer(unittest.TestCase):
    def test_lex(self):
        prog: str = "(A & B) | !C"
        l: Lexer = Lexer()
        l.lex(prog)
        self.assertEqual(
            l.getTokens(), ["(", "A", "&", "B", ")", "|", "!", "C", "<EOF>"]
        )

        prog = "A|B"
        l2: Lexer = Lexer()
        l2.lex(prog)
        self.assertEqual(l2.getTokens(), ["A", "|", "B", "<EOF>"])

        prog = "!(A & C)"
        l3: Lexer = Lexer()
        l3.lex(prog)
        self.assertEqual(l3.getTokens(), ["!", "(", "A", "&", "C", ")", "<EOF>"])


t = TestLexer()
t.test_lex()
