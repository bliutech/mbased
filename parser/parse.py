import re
import sys


def error(msg: str, pos: int):
    print(f"Parse error: {msg} at position {pos}", file=sys.stderr)
    exit(1)


class Parser:
    """Parser object for analyzing tokens for errors"""

    def __init__(self) -> None:
        """Initializes the parser with attributes to be used"""
        self.pos: int = 0

    def parse(self, tokens: list[str]) -> None:
        """Parses given tokens"""

        self.tokens: list[str] = tokens
        self.advance()  # Initializes the first token
        rv = self.expr()
        self.assert_end()
        print("Successfully completed parsing")
        return rv

    def assert_end(self) -> None:
        if self.next_token != "<EOF>":
            error(f"Expected end '<EOF>' but found {self.next_token}", self.pos)

    def eat(self, expected: str) -> None:
        """Skips a token"""
        if self.next_token == expected:
            self.advance()
        else:
            error(f"Expected '{expected}' but found '{self.next_token}'", self.pos)

    def advance(self) -> None:
        """Moves to the next token"""
        self.pos += 1
        self.next_token: str = self.tokens[self.pos]
        
    def expr(self) -> None:
        """Parses an expression"""
        if self.var():
            self.eat(self.next_token)
            self.expr_prime()
        elif self.next_token == "!":
            self.eat("!")
            self.expr()
        elif self.next_token == "(":
            self.eat("(")
            self.expr()
            if self.next_token == ")":
                self.eat(")")
            else:
                error(f"Expected ')' but found '{self.next_token}'", self.pos)
        else:
            error(f"Expected [var, !, (] but found '{self.next_token}'", self.pos)

    def expr_prime(self) -> None:
        """Parses an expression prime (explain what this is later)"""
        if self.next_token == "&":
            self.eat("&")
            self.expr()
        elif self.next_token == "|":
            self.eat("|")
            self.expr()

    def var(self) -> None:
        """Parses a variable that represents a boolean expression"""
        if re.match("[A-Z]+", self.next_token):
            return True
